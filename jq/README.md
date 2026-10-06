# jq

**C · 48 source files · 26,655 lines · [https://github.com/jqlang/jq](https://github.com/jqlang/jq) · MIT**

Forty-eight source files. An agent finds its own way, and the honest result is a
gain too small to claim on any metric. It is published here rather than left out, because a
claim about where something helps is worth what the claim about where it does not is worth.
**At this size, our advice is not to buy the package.** The second study below is the
interesting one for jq: a project this small can still be expensive to verify.

## What was measured here

12 real defect tickets from this project's own history. Each ticket was run twice with
nothing installed and twice with the package installed, in runs placed at opposite ends of the
day: 48 agent sessions. The agent's patch is compared by script against the one the
maintainers actually wrote.

| Per ticket | without | with the package | |
|---|---|---|---|
| Tokens | 348,264 | **308,143** | **−11.5%** |
| Cost | $0.366 | **$0.312** | **−14.8%** |
| Model turns | 15.9 | **13.1** | **−17.8%** |
| Tool calls | 17.5 | **15.9** | **−9.5%** |
| Fix landed on the right file, of 12 | 10.5 | 11.0 | a tie |
| Sessions past 40 tool calls | 0 of 24 | 0 of 24 | |

✓ marks a difference that held on all ten resamplings and in both replicates. A row without
one moved but did not clear that bar, and is printed anyway.

## Fitting the package to this repository, measured on its own

One piece of the fitting, measured against the same package without it. 10 tickets,
40 sessions, both arms run twice.

These are a different, question-shaped set of tasks from the table above, graded on how much
of a reference answer the agent covered. The absolute figures are therefore **not comparable
between the two tables** -- only the contrast inside each table is.

| Per ticket | package | package + that piece | |
|---|---|---|---|
| Cost | $0.223 | **$0.186** | **−16.6%** |
| Tool calls | 15.8 | **10.2** | **−35.6%** ✓ |
| Model turns | 6.6 | **5.3** | **−18.9%** ✓ |
| Answer completeness | 0.633 | 0.680 | +7.5% |

Across the six codebases in this study, two showed an established reduction and they are the
two whose verification is hard to guess. Answer completeness improved on none of the six: the
fitting makes the work cheaper where it works, it does not make the answers better.

## The benchmark, yours to keep

[`kit/`](kit/) is the instrument that produced the second table, self-contained: the cases,
the runner, the analysis with its guards, and the audit trail of what was dropped from this
page and why. Python standard library, no dependency on anything of ours, and it runs against
your own checkout.

```
python kit/bench/run.py --arm bare  --rep r1
python kit/bench/run.py --arm facts --rep r1
python kit/bench/run.py --arm bare  --rep r2
python kit/bench/run.py --arm facts --rep r2
python kit/bench/analyse.py
```

Both replicates of both arms. They are not redundancy: the difference between an arm and
itself is that day's noise floor, and the analysis uses it as a veto.

## Estimate it for a repository this size

```
python ../tools/estimate.py --files 48 --loc 26655
```

---

[Why these numbers can be believed](../docs/EVIDENCE.md) ·
[What gets installed](../docs/WHAT-IT-DOES.md) ·
[What an engagement looks like](../docs/ENGAGEMENT.md) ·
[Estimate your own repository](../docs/ESTIMATE.md)
