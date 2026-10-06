#!/usr/bin/env python3
"""Check that this repository does not contradict itself.

    python tools/check_repo.py

Every number here lives in more than one place: a codebase page, the landing table, and the
estimator's calibration. This fails if any of them drift apart, and it is the reason a
figure can be trusted to mean the same thing on whichever page you read it.

It also refuses anything that should never have been published: an absolute path from a
working machine, an internal project name, a reference to a private checkout.

Standard library only. Exit code 0 means every check passed.
"""
from __future__ import annotations

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import estimate as E  # noqa: E402

# The nine codebases and what their pages must say. Source files and lines are what
# `estimate.py --scan` produces on each checkout; the token figure is the measured
# reduction for the five in the first study and absent for the other four.
EXPECTED = {
    "rocketchat": dict(files=7454, loc=503665, tokens=-52.0),
    "keycloak":   dict(files=6326, loc=764287, tokens=-37.6),
    "suitecrm":   dict(files=4797, loc=914599, tokens=-45.6),
    "mitmproxy":  dict(files=472, loc=68824, tokens=-37.2),
    "jq":         dict(files=48, loc=26655, tokens=-11.5),
    "polly":      dict(files=485, loc=42234, tokens=None),
    "hugo":       dict(files=555, loc=133887, tokens=None),
    "bat":        dict(files=50, loc=12594, tokens=None),
    "phoenix":    dict(files=108, loc=32609, tokens=None),
}
KITS = ("jq", "mitmproxy", "polly", "hugo", "bat", "phoenix")

# Published once, on the landing page, and nowhere else allowed to disagree.
POOLED = {"tokens": -40.5, "cost": -30.0, "replies": -42.9, "calls": -26.7}

FORBIDDEN = [
    (r"[A-Za-z]:[\\/]Users", "an absolute path from a working machine"),
    (r"\bKontext\b", "an internal project name"),
    (r"\bstackbench\b", "an internal benchmark path"),
    (r"\bcrame\b", "a machine account name"),
    (r"\bbober\b", "an internal package name"),
    (r"\bAppData\b", "a temporary working directory"),
]
MINUS = chr(8722)


def render_lines(files: int, loc: int, spend: float) -> list:
    """The first block of a real estimate run -- the part the estimate page quotes."""
    text = E.render(E.report(files, loc, monthly_spend=spend))
    out = []
    for line in text.splitlines():
        if line.strip().startswith("HOW MUCH TO TRUST IT"):
            break
        out.append(line)
    return out


def read(*parts) -> str:
    p = os.path.join(ROOT, *parts)
    if not os.path.exists(p):
        return ""
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def main() -> int:
    fails = []
    note = fails.append

    # 1. every codebase has a page, and the page states the size we calibrated on
    for stack, exp in EXPECTED.items():
        page = read(stack, "README.md")
        if not page:
            note(f"{stack}: no page")
            continue
        for label, value in (("source files", exp["files"]), ("lines", exp["loc"])):
            if f"{value:,} {label}" not in page:
                note(f"{stack}: page does not state {value:,} {label}")
        if exp["tokens"] is not None:
            want = f"{MINUS}{abs(exp['tokens']):.1f}%"
            if want not in page:
                note(f"{stack}: page does not state its token reduction {want}")
        elif "second study only" not in page:
            note(f"{stack}: has no first-study number and does not say so")

    # 2. the estimator's calibration IS the first study, not a copy that drifted
    calib = {n: (f, p) for n, _l, f, p in E.CALIBRATION}
    names = {"rocketchat": "Rocket.Chat", "keycloak": "Keycloak", "suitecrm": "SuiteCRM",
             "mitmproxy": "mitmproxy", "jq": "jq"}
    for stack, nice in names.items():
        exp = EXPECTED[stack]
        if nice not in calib:
            note(f"estimator: {nice} missing from the calibration")
            continue
        files, pct = calib[nice]
        if files != exp["files"]:
            note(f"estimator: {nice} calibrated on {files} files, page says {exp['files']}")
        if abs(pct - abs(exp["tokens"])) > 0.6:
            note(f"estimator: {nice} calibrated on {pct}%, page says {abs(exp['tokens'])}%")
    if len(calib) != 5:
        note(f"estimator: calibrated on {len(calib)} codebases, the first study has 5")

    # 3. the landing page carries the pooled result, which is the only headline claim
    land = read("README.md")
    for name, value in POOLED.items():
        if f"{MINUS}{abs(value):.1f}%" not in land:
            note(f"landing page: missing the pooled {name} figure {value}%")
    for stack in EXPECTED:
        if f"({stack}/" not in land:
            note(f"landing page: does not link to {stack}/")

    # 4. the fit must still be insensitive to the point our own veto calls unread
    full, without = E.fit(), E.fit([(f, p) for n, _l, f, p in E.CALIBRATION
                                    if n != "Rocket.Chat"])
    import math
    for files in (50, 500, 5000, E.CALIB_MAX_FILES):
        a = E.central(files, full)
        b = min(E.CEILING_PCT, max(0.0, without["intercept"]
                                   + without["slope"] * math.log10(min(files,
                                                                       E.CALIB_MAX_FILES))))
        if abs(a - b) >= 2 * full["spread"]:
            note(f"estimator: dropping the unread point moves {files} files by {abs(a-b):.1f}")

    # 5. the tool output quoted in the estimate page must be the tool's actual output
    table = E.table().splitlines()
    page = read("docs", "ESTIMATE.md")
    for line in table:
        if not line.strip() or line.strip().startswith(("WHAT WE", "BANDS", "Every row",
                                                        "out before", "Of those", "File counts",
                                                        "the same way", "What IS")):
            continue
        if line.rstrip() not in page:
            note(f"docs/ESTIMATE.md: quotes the estimator's table wrongly, missing "
                 f"{line.strip()!r}")
    worked = render_lines(4797, 914599, 12000)
    for line in worked:
        if line.rstrip() and line.rstrip() not in page:
            note(f"docs/ESTIMATE.md: the worked example does not match the tool, missing "
                 f"{line.strip()!r}")

    # 5b. every relative link resolves. A page once pointed at a file that did not exist.
    link = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__")]
        for name in filenames:
            if not name.endswith(".md"):
                continue
            src = os.path.join(dirpath, name)
            rel = os.path.relpath(src, ROOT).replace(os.sep, "/")
            with open(src, encoding="utf-8") as fh:
                body = fh.read()
            for target in link.findall(body):
                target = target.split("#")[0].strip()
                if not target or target.startswith(("http://", "https://", "mailto:")):
                    continue
                if not os.path.exists(os.path.normpath(os.path.join(dirpath, target))):
                    note(f"{rel}: dead link to {target!r}")

    # 6. a kit and its codebase page publish the same numbers, to their own precision
    row = re.compile(r"\|\s*(tool calls|cost per case)\s*\|\s*\$?([\d.]+)\s*\|\s*\$?([\d.]+)\s*\|")
    for stack in KITS:
        kit, page = read(stack, "kit", "RESULTS.md"), read(stack, "README.md")
        if not kit:
            note(f"{stack}: kit has no RESULTS.md")
            continue
        found = {m.group(1): (float(m.group(2)), float(m.group(3)))
                 for m in row.finditer(kit)}
        for label in ("tool calls", "cost per case"):
            if label not in found:
                note(f"{stack}/kit/RESULTS.md: no '{label}' row")
                continue
            c, t = found[label]
            # the page rounds to one decimal for calls and three for cost
            want = (f"| {c:.1f} | **{t:.1f}** |" if label == "tool calls"
                    else f"| ${c:.3f} | **${t:.3f}** |")
            if want not in page:
                note(f"{stack}: page and kit disagree on {label} "
                     f"(kit says {c} -> {t}, page has no {want!r})")

    # 7. a kit is promised only where a kit exists, and exists only where promised
    for stack in KITS:
        if not os.path.isfile(os.path.join(ROOT, stack, "kit", "bench", "run.py")):
            note(f"{stack}: promised a kit, but kit/bench/run.py is missing")
        if "kit/" not in read(stack, "README.md"):
            note(f"{stack}: ships a kit its page never mentions")
    for stack in EXPECTED:
        if stack not in KITS and os.path.isdir(os.path.join(ROOT, stack, "kit")):
            note(f"{stack}: ships a kit that is not in the promised set")

    # 6. nothing that should never have left a working machine
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__", "results")]
        for name in filenames:
            if not name.endswith((".md", ".py", ".json", ".txt")):
                continue
            rel = os.path.relpath(os.path.join(dirpath, name), ROOT).replace(os.sep, "/")
            if rel.startswith("tools/check_repo.py"):
                continue          # this file names the patterns on purpose
            try:
                with open(os.path.join(dirpath, name), encoding="utf-8") as fh:
                    body = fh.read()
            except (OSError, UnicodeDecodeError):
                note(f"{rel}: cannot be read as text")
                continue
            for pat, why in FORBIDDEN:
                hit = re.search(pat, body, re.IGNORECASE)
                if hit:
                    note(f"{rel}: contains {why} ({hit.group(0)!r})")

    if fails:
        print(f"FAIL — {len(fails)} problem(s):")
        for f in fails:
            print("  " + f)
        return 1
    print(f"OK — {len(EXPECTED)} codebase pages, {len(KITS)} kits, the landing table and the "
          f"estimator all agree,\n     and nothing private is published.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
