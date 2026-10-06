#!/usr/bin/env python3
"""Estimate what the package returns on a codebase, from its size.

    python tools/estimate.py --files 4200 --loc 610000
    python tools/estimate.py --files 4200 --loc 610000 --monthly-spend 9000
    python tools/estimate.py --scan /path/to/checkout
    python tools/estimate.py --table
    python tools/estimate.py --files 4200 --loc 610000 --json

Python standard library only. No network, nothing written, nothing sent anywhere: with
`--scan` it reads file names and counts lines, never file contents.

WHAT THIS IS, AND WHAT IT IS NOT
--------------------------------
It is a BAND, fitted on five codebases we measured end to end -- 56 tickets, 224 agent
sessions, each ticket run twice with the package installed and twice without it. Five points is five points, so the
band is wide on purpose and this tool prints its own uncertainty rather than hiding it.

It is NOT a quote and not a promise. An engagement opens with that same measurement run on
your repository, which replaces this estimate with a number. If the number comes back flat,
that is the honest answer for your codebase and we say so.

WHY SIZE, AND WHY THE COUNT DOES NOT HAVE TO BE EXACT
-----------------------------------------------------
What the package returns tracks how much of a codebase an agent has to rule out before it
can start. That scales with the number of places a change could live, not with the
language, so the fit below is on file count.

The count is deliberately forgiving. Whether you include tests, generated files and
vendored code moves a typical repository's file count by tens of percent, and every run of
this tool prints what a miscount that large would do to the answer: less than the width of
the band. Count however your tooling counts.

Lines of code do not drive the estimate. They do two things: turn a percentage into a
volume you recognise, and flag a codebase whose average file is far outside the range we
calibrated on, where a file count means something different from what it meant here.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import statistics
import sys

# ---------------------------------------------------------------------------
# The calibration. Five public codebases, measured with the package and without it on
# tickets taken from each project's own history. The per-codebase pages in this repository
# hold the full result for each one, including the one where the answer was "do not buy".
# ---------------------------------------------------------------------------
CALIBRATION = [
    # name,         language,     source files, token reduction %
    ("Rocket.Chat", "TypeScript", 7454, 52.0),
    ("Keycloak",    "Java",       6326, 38.0),
    ("SuiteCRM",    "PHP",        4797, 46.0),
    ("mitmproxy",   "Python",      472, 37.0),
    ("jq",          "C",            48, 12.0),
]

# Every file count above was produced by this tool's own `--scan`, so a prospect who scans
# their checkout is measured the same way the calibration was. That is the whole reason the
# scanner ships with the estimator.
#
# What each of those five reductions is worth, under the rules on the evidence page: one is
# established on its own (SuiteCRM), three are directional, and one -- the largest, 52% --
# is reported UNREAD, because that arm differed from itself by more than the test could
# absorb. What IS established is the reduction pooled over all 56 tickets: 40.5% of tokens.
# Dropping the unread point from the fit moves this estimate by at most 2.3 points, against
# a band 11 points wide, so the decision to keep it changes nothing a client would notice.
CALIBRATION_NOTE = (
    "one point is established on its own, three are directional and one is unread."
    + chr(10) + "    What IS established is the reduction pooled over all 56 tickets: "
    "40.5% of tokens.")

# Average lines per file across the calibration checkouts, from the same scan. Outside this
# range a file count stops meaning what it meant above, and the tool says so.
CALIBRATED_AVG_LINES = (65, 560)

# A reduction this tool will not print above, whatever the fit says. The largest reduction
# we have ever measured is 52%; extrapolating past it would be arithmetic, not evidence.
CEILING_PCT = 55.0

# The largest codebase in the calibration. Above it the fit keeps climbing and we have no
# evidence that the real curve does, so the estimate is HELD at this size rather than
# extrapolated. Below the smallest, the fit is allowed to keep falling: that direction
# errs against us, not against the client.
CALIB_MAX_FILES = max(f for _, _, f, _ in CALIBRATION)


def fit(points=None) -> dict:
    """Least squares of reduction against log10(file count), with the spread it leaves."""
    pts = points or [(f, p) for _, _, f, p in CALIBRATION]
    xs = [math.log10(f) for f, _ in pts]
    ys = [p for _, p in pts]
    mx, my = statistics.mean(xs), statistics.mean(ys)
    denom = sum((x - mx) ** 2 for x in xs)
    if denom == 0:
        raise ValueError("calibration needs codebases of different sizes")
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / denom
    intercept = my - slope * mx
    resid = [y - (intercept + slope * x) for x, y in zip(xs, ys)]
    ss_res = sum(r * r for r in resid)
    ss_tot = sum((y - my) ** 2 for y in ys)
    return {
        "slope": slope,
        "intercept": intercept,
        "spread": statistics.pstdev(resid),
        "r2": 1 - ss_res / ss_tot if ss_tot else 0.0,
        "n": len(pts),
    }


def central(files: int, model: dict | None = None) -> float:
    """The fitted reduction for a file count, held at our largest measured codebase."""
    if files < 1:
        raise ValueError("file count must be at least 1")
    m = model or fit()
    held = min(files, CALIB_MAX_FILES)
    return min(CEILING_PCT, max(0.0, m["intercept"] + m["slope"] * math.log10(held)))


def band(files: int, model: dict | None = None) -> tuple:
    """The central estimate with two residual spreads either side -- the honest range."""
    m = model or fit()
    c = central(files, m)
    w = 2 * m["spread"]
    return max(0.0, c - w), c, min(CEILING_PCT, c + w)


def sensitivity(files: int, model: dict | None = None, swing: float = 0.4) -> tuple:
    """How far a miscount of +/- `swing` moves the estimate, against the band's own width."""
    m = model or fit()
    lo = central(max(1, int(round(files * (1 - swing)))), m)
    hi = central(max(1, int(round(files * (1 + swing)))), m)
    return abs(hi - lo), 4 * m["spread"]


# ---------------------------------------------------------------------------
# Counting a checkout, for prospects who would rather point at the repository than count.
# ---------------------------------------------------------------------------
SKIP_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "vendor", "third_party", "thirdparty",
    "build", "dist", "out", "target", "_build", "deps", ".venv", "venv", "env",
    "__pycache__", ".tox", ".mypy_cache", ".pytest_cache", ".gradle", ".idea",
    ".vscode", "bower_components", "Pods", "coverage", "site-packages",
}
TEST_PAT = re.compile(
    r"(^|[/_.-])(tests?|spec|specs|testdata|fixtures?|mocks?|e2e|__tests__|__mocks__)([/_.-]|$)",
    re.IGNORECASE)
CODE_EXTS = {
    ".py", ".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".java", ".kt", ".kts", ".go",
    ".rs", ".rb", ".php", ".c", ".h", ".cc", ".cpp", ".cxx", ".hpp", ".hh", ".cs",
    ".swift", ".m", ".mm", ".scala", ".ex", ".exs", ".erl", ".hrl", ".sh", ".bash",
    ".ps1", ".pl", ".pm", ".lua", ".dart", ".vue", ".svelte", ".sql", ".r", ".jl",
    ".hs", ".clj", ".cljs", ".groovy", ".f90", ".zig", ".nim", ".elm", ".ml", ".vb",
}


def scan(root: str) -> tuple:
    """Count source files and lines under `root`, skipping tests, vendored code and output."""
    if not os.path.isdir(root):
        raise SystemExit("not a directory: " + root)
    files = lines = skipped = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames
                       if d not in SKIP_DIRS and not d.startswith(".")
                       and not TEST_PAT.search(d)]
        rel = os.path.relpath(dirpath, root).replace(os.sep, "/")
        if rel != "." and TEST_PAT.search(rel):
            continue
        for name in filenames:
            if os.path.splitext(name)[1].lower() not in CODE_EXTS:
                continue
            if TEST_PAT.search(name):
                skipped += 1
                continue
            try:
                with open(os.path.join(dirpath, name), "rb") as fh:
                    lines += sum(1 for _ in fh)
                files += 1
            except OSError:
                skipped += 1
    return files, lines, skipped


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------
def size_class(files: int) -> str:
    if files < 150:
        return ("small enough that an agent can hold most of it at once, which is the shape "
                "where we have measured the least return")
    if files < 1200:
        return "mid-sized: one team's service or application"
    if files < 6000:
        return "large: several teams, or one long-lived product"
    return "monorepo scale, the shape where we have measured the most return"


def report(files, loc=None, monthly_spend=None, sessions=None,
           cost_per_session=None, swing=0.4) -> dict:
    m = fit()
    lo, mid, hi = band(files, m)
    moved, width = sensitivity(files, m, swing)
    out = {
        "input": {"source_files": files, "lines_of_code": loc},
        # Whole points: the band is plus and minus two residual spreads, so a tenth of a
        # point is noise dressed up. Rounding here also means the money below is exactly
        # what a client gets by applying the printed percentage to their own spend.
        "estimate_pct": {"low": round(lo), "central": round(mid), "high": round(hi)},
        "size_class": size_class(files),
        "model": {"n_codebases": m["n"], "r_squared": round(m["r2"], 2),
                  "residual_spread_pts": round(m["spread"], 1),
                  "ceiling_pct": CEILING_PCT, "note": CALIBRATION_NOTE},
        "count_sensitivity": {"swing_pct": int(round(swing * 100)),
                              "estimate_moves_pts": round(moved, 1),
                              "band_width_pts": round(width, 1),
                              "count_matters_less_than_band": moved < width},
        "quality_note": ("unchanged -- this makes an agent cheaper and far more predictable, "
                         "not cleverer"),
        "warnings": [],
    }
    if loc:
        avg = loc / files
        out["input"]["avg_lines_per_file"] = round(avg, 1)
        if not CALIBRATED_AVG_LINES[0] <= avg <= CALIBRATED_AVG_LINES[1]:
            out["warnings"].append(
                "the average file is {:.0f} lines, outside the {}-{} line range of the five "
                "codebases this was fitted on. A file count may not mean here what it meant "
                "there, so read the band as wider than printed.".format(
                    avg, *CALIBRATED_AVG_LINES))
    if monthly_spend is None and sessions and cost_per_session:
        monthly_spend = sessions * cost_per_session
    if monthly_spend:
        # Against the percentages as PRINTED, not the unrounded fit: a client who redoes the
        # arithmetic from the band on the page has to land on the same figure.
        pr = out["estimate_pct"]
        out["monthly"] = {
            "spend_today": round(monthly_spend, 2),
            "saving_low": round(monthly_spend * pr["low"] / 100, 2),
            "saving_central": round(monthly_spend * pr["central"] / 100, 2),
            "saving_high": round(monthly_spend * pr["high"] / 100, 2),
        }
    if files < 150:
        out["warnings"].append(
            "at this size the one codebase we hold of this shape returned 12%, and we would "
            "rather tell you that than sell into it.")
    if files > CALIB_MAX_FILES:
        out["held_at_files"] = CALIB_MAX_FILES
        out["warnings"].append(
            "{:,} files is larger than the largest codebase we have measured ({:,}). The fit "
            "keeps climbing above that and we have no evidence the real curve does, so this "
            "estimate is HELD at our largest measured shape rather than extrapolated.".format(
                files, CALIB_MAX_FILES))
    return out


def render(r: dict) -> str:
    e, m, s, i = r["estimate_pct"], r["model"], r["count_sensitivity"], r["input"]
    L = []
    L.append("")
    L.append("  ESTIMATED TOKEN REDUCTION PER TICKET")
    L.append("")
    L.append("      {}% to {}%".format(e["low"], e["high"])
             + "        central estimate {}%".format(e["central"]))
    L.append("")
    size = "  your codebase    {:,} source files".format(i["source_files"])
    if i.get("lines_of_code"):
        size += ", {:,} lines ({:.0f} per file)".format(
            i["lines_of_code"], i["avg_lines_per_file"])
    L.append(size)
    L.append("  which is         " + r["size_class"])
    L.append("")
    if "monthly" in r:
        mo = r["monthly"]
        L.append("  at {:,.0f} a month in agent spend, that is {:,.0f} to {:,.0f} a month "
                 "back,".format(mo["spend_today"], mo["saving_low"], mo["saving_high"]))
        L.append("  or {:,.0f} at the central estimate.".format(mo["saving_central"]))
        L.append("")
    L.append("  HOW MUCH TO TRUST IT")
    L.append("    Fitted on {} codebases measured end to end. R2 {:.2f}, typical miss {:.0f} "
             "points.".format(m["n_codebases"], m["r_squared"], m["residual_spread_pts"]))
    L.append("    Of those five, " + CALIBRATION_NOTE)
    L.append("    Five points is five points: the range above is the fit plus and minus two "
             "of those misses.")
    L.append("    Held under {:.0f}% whatever the fit says, because 52% is the largest "
             "reduction we".format(m["ceiling_pct"]))
    L.append("    have ever measured and extrapolating past it would be arithmetic, not "
             "evidence.")
    L.append("    Miscounting your files by {}% moves this by {:.0f} points against a band "
             "{:.0f} points wide,".format(s["swing_pct"], s["estimate_moves_pts"],
                                          s["band_width_pts"]))
    L.append("    so the exact count is not worth arguing about."
             if s["count_matters_less_than_band"] else
             "    so at this size the count does matter: use --scan rather than a guess.")
    L.append("")
    L.append("  WHAT DOES NOT CHANGE")
    L.append("    Quality: " + r["quality_note"] + ".")
    L.append("")
    for w in r["warnings"]:
        L.append("  NOTE  " + w)
    if r["warnings"]:
        L.append("")
    L.append("  An estimate, not a quote. An engagement opens by running the same measurement")
    L.append("  on your repository, which replaces this with a number -- including if that")
    L.append("  number comes back flat.")
    L.append("")
    return "\n".join(L)


def table() -> str:
    m = fit()
    L = ["", "  WHAT WE MEASURED, AND WHAT THE FIT MAKES OF IT", ""]
    L.append("  {:14}{:12}{:>8}{:>10}{:>8}".format(
        "codebase", "language", "files", "measured", "fit"))
    for name, lang, files, pct in sorted(CALIBRATION, key=lambda row: -row[2]):
        L.append("  {:14}{:12}{:>8,}{:>9.0f}%{:>7.0f}%".format(
            name, lang, files, pct, central(files, m)))
    L += ["", "  R2 {:.2f} on {} codebases, typical miss {:.1f} points.".format(
        m["r2"], m["n"], m["spread"]),
        "  Of those five, " + CALIBRATION_NOTE.replace(chr(10) + "    ", chr(10) + "  "),
        "  File counts are this tool's own --scan, so a scan of your checkout is measured",
        "  the same way.", "", "  BANDS TO QUOTE FROM", ""]
    L.append("  {:>14}{:>16}{:>10}".format("source files", "range", "central"))
    for f in (50, 150, 500, 1500, 5000, 7454):
        lo, mid, hi = band(f, m)
        L.append("  {:>14,}{:>16}{:>9.0f}%".format(
            f, "{:.0f}% to {:.0f}%".format(lo, hi), mid))
    L += ["", "  Every row is the same package. What changes is how much an agent has to rule",
          "  out before it can start. Quality is unchanged at every size.", ""]
    return "\n".join(L)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--files", type=int, help="source files, excluding tests and vendored code")
    ap.add_argument("--loc", type=int, help="lines of code in those files")
    ap.add_argument("--scan", metavar="PATH", help="count a checkout instead of passing numbers")
    ap.add_argument("--monthly-spend", type=float, metavar="N",
                    help="what the team spends on agent sessions a month, any currency")
    ap.add_argument("--sessions-per-month", type=int, metavar="N")
    ap.add_argument("--cost-per-session", type=float, metavar="N")
    ap.add_argument("--swing", type=float, default=0.4, metavar="F",
                    help="the miscount to test the estimate against (default 0.4, i.e. 40%%)")
    ap.add_argument("--table", action="store_true", help="the calibration and quotable bands")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    if a.table:
        print(table())
        return 0
    if a.swing <= 0 or a.swing >= 1:
        ap.error("--swing must be a fraction between 0 and 1, e.g. 0.4")
    if bool(a.sessions_per_month) != bool(a.cost_per_session) and not a.monthly_spend:
        ap.error("--sessions-per-month and --cost-per-session are only useful together; "
                 "pass both, or pass --monthly-spend instead")
    files, loc = a.files, a.loc
    if a.scan:
        files, loc, skipped = scan(a.scan)
        if not a.json:
            print("\n  scanned {}: {:,} source files, {:,} lines ({:,} test or unreadable "
                  "files skipped)".format(a.scan, files, loc, skipped))
        if files < 1:
            raise SystemExit("found no source files to count -- pass --files instead")
    if not files:
        ap.error("pass --files (and ideally --loc), or --scan PATH, or --table")
    if files < 1:
        ap.error("--files must be at least 1")

    r = report(files, loc, a.monthly_spend, a.sessions_per_month,
               a.cost_per_session, a.swing)
    print(json.dumps(r, indent=2) if a.json else render(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
