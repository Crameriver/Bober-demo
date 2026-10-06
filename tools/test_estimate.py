#!/usr/bin/env python3
"""Tests for the estimator. Standard library only, no pytest needed.

    python tools/test_estimate.py

Each test below exists because the estimator is shown to prospects: a defect here is a
number quoted at somebody. The ones that matter most are the honesty guards -- the fit must
not extrapolate past the codebases it was fitted on, and it must never print a reduction
larger than the largest one we have measured.
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import estimate as E  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


class Fit(unittest.TestCase):
    def test_fit_reproduces_each_measured_codebase_within_its_spread(self):
        """The fit is useless if it misses the points it was fitted on."""
        m = E.fit()
        for name, _lang, files, measured in E.CALIBRATION:
            got = E.central(files, m)
            self.assertLess(abs(got - measured), 3 * m["spread"],
                            f"{name}: fit {got:.1f}% against measured {measured}%")

    def test_fit_is_monotone_in_size(self):
        last = -1.0
        for files in (10, 100, 500, 2000, 9000):
            got = E.central(files)
            self.assertGreaterEqual(got, last, f"reduction fell at {files} files")
            last = got

    def test_dropping_the_unread_point_barely_moves_the_fit(self):
        """The calibration keeps a point our own veto calls unread. That has to be harmless."""
        keep = [(f, p) for name, _l, f, p in E.CALIBRATION if name != "Rocket.Chat"]
        without = E.fit(keep)
        full = E.fit()
        for files in (50, 500, 5000, E.CALIB_MAX_FILES):
            a = E.central(files, full)
            b = min(E.CEILING_PCT, max(0.0, without["intercept"]
                                       + without["slope"] * __import__("math").log10(files)))
            self.assertLess(abs(a - b), 2 * full["spread"],
                            f"at {files} files the unread point moves the fit by "
                            f"{abs(a - b):.1f} points")

    def test_calibration_counts_are_what_the_scanner_would_produce(self):
        """Not a scan of those repositories -- a guard that nobody edits one set and not the
        other. The nine counts live on the evidence page; these five must match it."""
        got = {name: files for name, _l, files, _p in E.CALIBRATION}
        self.assertEqual(got, {"Rocket.Chat": 7454, "Keycloak": 6326, "SuiteCRM": 4797,
                               "mitmproxy": 472, "jq": 48})

    def test_r2_and_spread_are_what_the_pages_quote(self):
        m = E.fit()
        self.assertEqual(round(m["r2"], 2), 0.83)
        self.assertAlmostEqual(m["spread"], 5.6, places=1)


class HonestyGuards(unittest.TestCase):
    def test_never_prints_more_than_the_largest_measured_reduction_plus_ceiling(self):
        for files in (10_000, 100_000, 10_000_000):
            self.assertLessEqual(E.band(files)[2], E.CEILING_PCT)

    def test_does_not_extrapolate_above_the_largest_measured_codebase(self):
        """A million-file repo must get the same answer as our largest, not a bigger one."""
        at_max = E.central(E.CALIB_MAX_FILES)
        self.assertAlmostEqual(E.central(1_000_000), at_max, places=6)
        r = E.report(1_000_000, None)
        self.assertEqual(r.get("held_at_files"), E.CALIB_MAX_FILES)
        self.assertTrue(any("HELD" in w for w in r["warnings"]),
                        "an extrapolated size must say so")

    def test_small_repo_gets_the_do_not_buy_warning(self):
        r = E.report(90, 50_000)
        self.assertTrue(any("rather tell you that than sell into it" in w
                            for w in r["warnings"]))

    def test_unusual_average_file_size_is_flagged(self):
        flagged = E.report(1000, 4_000_000)          # 4000 lines a file
        self.assertTrue(any("outside the" in w for w in flagged["warnings"]))
        quiet = E.report(1000, 300_000)              # 300 lines a file, in range
        self.assertFalse(any("outside the" in w for w in quiet["warnings"]))

    def test_band_is_wide_enough_to_swallow_a_miscount(self):
        """The claim printed on every run has to hold for every realistic size."""
        for files in (100, 500, 1000, 5000, 9000):
            moved, width = E.sensitivity(files, swing=0.4)
            self.assertLess(moved, width, f"at {files} files a 40% miscount exceeds the band")
            self.assertTrue(E.report(files, None)["count_sensitivity"]
                            ["count_matters_less_than_band"])

    def test_reduction_never_goes_negative(self):
        self.assertGreaterEqual(E.central(1), 0.0)
        self.assertGreaterEqual(E.band(1)[0], 0.0)

    def test_quality_note_is_on_every_report(self):
        for files in (50, 800, 9000):
            self.assertIn("not cleverer", E.report(files, None)["quality_note"])


class Money(unittest.TestCase):
    def test_the_printed_percentage_applied_by_hand_gives_the_printed_money(self):
        """A client who multiplies the band on the page by their spend must land on our
        figure. It did not, when the band was rounded for display and the money was not."""
        r = E.report(4797, 914_599, monthly_spend=12_000)
        for k, m in (("low", "saving_low"), ("central", "saving_central"),
                     ("high", "saving_high")):
            self.assertEqual(r["monthly"][m], round(12_000 * r["estimate_pct"][k] / 100, 2))
        for k in ("low", "central", "high"):
            self.assertEqual(r["estimate_pct"][k], int(r["estimate_pct"][k]),
                             "percentages are printed as whole points, so store them so")

    def test_monthly_saving_is_the_percentage_of_the_spend(self):
        r = E.report(4903, 700_000, monthly_spend=10_000)
        lo, mid, hi = (r["estimate_pct"][k] for k in ("low", "central", "high"))
        self.assertAlmostEqual(r["monthly"]["saving_low"], 10_000 * lo / 100, places=1)
        self.assertAlmostEqual(r["monthly"]["saving_central"], 10_000 * mid / 100, places=1)
        self.assertAlmostEqual(r["monthly"]["saving_high"], 10_000 * hi / 100, places=1)

    def test_sessions_times_cost_equals_a_spend(self):
        a = E.report(800, None, monthly_spend=400 * 0.5)
        b = E.report(800, None, sessions=400, cost_per_session=0.5)
        self.assertEqual(a["monthly"], b["monthly"])

    def test_no_money_section_without_money_input(self):
        self.assertNotIn("monthly", E.report(800, None))


class Scan(unittest.TestCase):
    def test_scan_counts_source_and_skips_tests_and_vendored(self):
        def write(d, rel, body):
            path = os.path.join(d, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(body)

        with tempfile.TemporaryDirectory() as d:
            w = lambda rel, body: write(d, rel, body)
            w("src/a.py", "one\ntwo\nthree\n")
            w("src/b.go", "one\ntwo\n")
            w("src/test_a.py", "x\n")               # test file by name
            w("tests/c.py", "x\n")                  # test file by directory
            w("node_modules/d.js", "x\n")           # vendored
            w("README.md", "x\n")                   # not code
            files, lines, skipped = E.scan(d)
            self.assertEqual(files, 2, "counted something other than a.py and b.go")
            self.assertEqual(lines, 5)
            self.assertEqual(skipped, 1, "the test file by name should be counted as skipped")

    def test_scan_of_a_missing_directory_fails_loudly(self):
        with self.assertRaises(SystemExit):
            E.scan(os.path.join(HERE, "no-such-directory-here"))


class CommandLine(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, os.path.join(HERE, "estimate.py"), *args],
                              capture_output=True, text=True)

    def test_table_runs_and_lists_every_calibration_codebase(self):
        p = self.run_cli("--table")
        self.assertEqual(p.returncode, 0, p.stderr)
        for name, _l, _f, _p in E.CALIBRATION:
            self.assertIn(name, p.stdout)

    def test_json_is_valid_and_carries_the_band(self):
        import json
        p = self.run_cli("--files", "4200", "--loc", "610000", "--json")
        self.assertEqual(p.returncode, 0, p.stderr)
        got = json.loads(p.stdout)
        self.assertLess(got["estimate_pct"]["low"], got["estimate_pct"]["central"])
        self.assertLess(got["estimate_pct"]["central"], got["estimate_pct"]["high"])

    def test_r2_is_printed_the_same_in_the_table_and_in_a_report(self):
        """Two code paths printed 0.82 and 0.81 for the same fit. Never again."""
        t = self.run_cli("--table").stdout
        r = self.run_cli("--files", "4200").stdout
        import re
        self.assertEqual(re.search(r"R2 (\d\.\d+)", t).group(1),
                         re.search(r"R2 (\d\.\d+)", r).group(1))

    def test_no_arguments_is_an_error_not_a_made_up_number(self):
        p = self.run_cli()
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("--files", p.stderr)

    def test_one_half_of_the_money_input_is_refused(self):
        p = self.run_cli("--files", "800", "--sessions-per-month", "400")
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("together", p.stderr)

    def test_scan_of_this_repository_produces_an_estimate(self):
        p = self.run_cli("--scan", os.path.dirname(HERE))
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("ESTIMATED TOKEN REDUCTION", p.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
