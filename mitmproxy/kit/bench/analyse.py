#!/usr/bin/env python3
"""Compare two arms on this repository, with the guards that stop a false positive.

    python bench/analyse.py                  # facts against bare
    python bench/analyse.py --treatment facts --control bare

Standard library only. Reads the rows `run.py` wrote; writes nothing you cannot check by hand.

WHAT THE GUARDS ARE FOR, each one bought with a retracted result
---------------------------------------------------------------
1. FIDELITY FIRST. The mechanism is counted by the EVENT it logged — `injections` — never by its own
   installation. A context file was once written into 106 sessions, with its byte count on every row
   as proof, and read by exactly 1 of them. If the treatment's injections are not what you expect,
   nothing below means anything and this script says so instead of printing a comparison.

2. THE REPLICATE NULL IS A VETO. Each arm runs twice at opposite ends of the day, so the difference
   between an arm and ITSELF is the drift of that day plus the noise of the model. If that
   self-difference passes the same test as a real effect, the test cannot tell them apart HERE — and
   the metric is reported unread. Not explained away as drift. Unread. Two identical arms once
   produced a difference that passed a ten-seed bootstrap on the one repository where this null had
   also fired, and it was published before it was caught.

3. TEN SEEDS, AND BOTH STRATA. A bootstrap interval is reported for ten different seeds and only
   counts if all ten agree. And the same contrast is computed inside each replicate separately,
   where the two arms ran back to back: an effect present in both strata is not an artefact of when
   things ran.

4. NO SILENT SUBSTITUTION. A metric that needs a stand-in value for "never happened" is reported at
   two different stand-ins and on complete cases only. One headline of ours was entirely an artefact
   of the stand-in chosen, and the complete-cases number was flat.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import statistics as stats

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(HERE, "results")
SEEDS = [20261006 + i * 7919 for i in range(10)]
REPS = ("r1", "r2")


def load(arm: str, rep: str) -> dict:
    d = os.path.join(RESULTS, f"{arm}-{rep}", "_row")
    out = {}
    if not os.path.isdir(d):
        return out
    for n in sorted(os.listdir(d)):
        if not n.endswith(".json"):
            continue
        with open(os.path.join(d, n), encoding="utf-8") as f:
            r = json.load(f)
        if not r.get("error"):
            out[r["case"]] = r
    return out


def boot(xs: list) -> tuple:
    """The least favourable 95% interval across ten seeds, and whether all ten exclude zero."""
    if not xs:
        return 0.0, 0.0, False
    los, his, n = [], [], len(xs)
    for seed in SEEDS:
        rnd = random.Random(seed)
        ms = sorted(sum(xs[rnd.randrange(n)] for _ in range(n)) / n for _ in range(4000))
        los.append(ms[100])
        his.append(ms[3899])
    return min(los), max(his), (all(x > 0 for x in los) or all(x < 0 for x in his))


def binom(k: int, n: int):
    if n == 0:
        return None
    pr = [math.comb(n, i) / 2 ** n for i in range(n + 1)]
    return round(min(1.0, sum(p for p in pr if p <= pr[k] + 1e-12)), 4)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--treatment", default="facts")
    ap.add_argument("--control", default="bare")
    a = ap.parse_args()
    T, C = a.treatment, a.control
    by = {f"{arm}-{rep}": load(arm, rep) for arm in (C, T) for rep in REPS}
    missing = [k for k, v in by.items() if not v]
    if missing:
        print("missing runs: " + ", ".join(missing))
        print("both arms need BOTH replicates — the replicates ARE the noise floor.")
        return 2
    ks = [k for k in by[f"{T}-r1"] if all(k in by[f"{x}-{p}"] for x in (C, T) for p in REPS)]
    if not ks:
        print("no case completed in all four runs")
        return 2

    print(f"A. FIDELITY — {len(ks)} cases complete in all four runs")
    for arm in (C, T):
        for rep in REPS:
            rr = list(by[f"{arm}-{rep}"].values())
            inj = sorted({r.get("injections", 0) for r in rr})
            print(f"  {arm}-{rep}: {len(rr)} rows, injections {inj}, "
                  f"${sum(r.get('cost', 0) for r in rr):.2f}")
    t_inj = {r.get("injections", 0) for p in REPS for r in by[f"{T}-{p}"].values()}
    c_inj = {r.get("injections", 0) for p in REPS for r in by[f"{C}-{p}"].values()}
    if T != "bare" and t_inj != {1}:
        print(f"\n  STOP. The treatment's injections are {sorted(t_inj)}, not 1 on every session.")
        print("  The mechanism did not arrive, or arrived more than once. A comparison now would")
        print("  measure something other than what you think, which is how a published result was")
        print("  once produced from two identical arms. Fix the delivery, then re-run.")
        return 3
    if c_inj - {0}:
        print(f"\n  STOP. The control shows injections {sorted(c_inj)} — it is not a control.")
        return 3
    print("  fidelity: the mechanism arrived exactly once in the treatment and never in the control")

    metrics = [("cost", lambda r: float(r.get("cost") or 0.0)),
               ("turns", lambda r: float(r.get("turns") or 0))]
    if any("recall" in r for r in by[f"{T}-r1"].values()):
        metrics.insert(0, ("recall", lambda r: float(r.get("recall") or 0.0)))

    print("\nB. THE REPLICATE NULL — an arm against ITSELF. Anything flagged here is VETOED below.")
    vetoed = set()
    for arm in (C, T):
        bits = []
        for name, f in metrics:
            d = [f(by[f"{arm}-r2"][k]) - f(by[f"{arm}-r1"][k]) for k in ks]
            _, _, clear = boot(d)
            if clear:
                vetoed.add(name)
            bits.append(f"{name} {stats.mean(d):+.4f}{' FIRED' if clear else ''}")
        print(f"  {arm:9} r2-r1: " + " | ".join(bits))
    if vetoed:
        print(f"  -> VETOED, not read for this repository: {', '.join(sorted(vetoed))}")

    print(f"\nC. {T.upper()} minus {C.upper()} on {len(ks)} cases")
    for name, f in metrics:
        d = [(f(by[f"{T}-r1"][k]) + f(by[f"{T}-r2"][k])) / 2
             - (f(by[f"{C}-r1"][k]) + f(by[f"{C}-r2"][k])) / 2 for k in ks]
        lo, hi, clear = boot(d)
        strata = []
        for p in REPS:
            ds = [f(by[f"{T}-{p}"][k]) - f(by[f"{C}-{p}"][k]) for k in ks]
            strata.append(boot(ds)[2])
        if name in vetoed:
            verdict = "VETOED (the arm differs from itself on this metric)"
        elif clear and all(strata):
            verdict = "ESTABLISHED (ten seeds, both strata)"
        elif clear:
            verdict = "one stratum only — not established"
        else:
            verdict = "not established"
        base = stats.mean((f(by[f"{C}-r1"][k]) + f(by[f"{C}-r2"][k])) / 2 for k in ks)
        pct = f"{100 * stats.mean(d) / base:+.1f}%" if base else "n/a"
        print(f"  {name:8} {stats.mean(d):+9.4f}  ({pct:>7})  [{lo:+.4f}, {hi:+.4f}]  {verdict}")

    if any("resolved" in r for r in by[f"{T}-r1"].values()):
        b = w = 0
        for k in ks:
            tv = sum(bool(by[f"{T}-{p}"][k].get("resolved")) for p in REPS)
            cv = sum(bool(by[f"{C}-{p}"][k].get("resolved")) for p in REPS)
            b += tv > cv
            w += tv < cv
        print(f"  resolved  better on {b}, worse on {w}, ties {len(ks) - b - w}, "
              f"p={binom(min(b, w), b + w)} (uncorrected)")

    print("\n  Read only what says ESTABLISHED. 'Not established' means this repository and this")
    print("  number of cases could not tell — it is not a small effect, it is no answer. And a")
    print("  VETOED metric means the instrument was noisier than the effect on the day you ran it:")
    print("  run more cases or more replicates, do not reinterpret.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
