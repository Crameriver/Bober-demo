# mitmproxy

**Python · 472 source files · 68,824 lines · [https://github.com/mitmproxy/mitmproxy](https://github.com/mitmproxy/mitmproxy) · MIT**

A mid-sized Python codebase with a clean layout and an addon system that
spreads one behaviour across several files. Model turns and tool calls both fell by a third and
held up. Tokens fell 37% without clearing the bar on nine tickets. Every session that had run
away stopped running away.

## What was measured here

9 real defect tickets from this project's own history. Each ticket was run twice with
nothing installed and twice with the package installed, in runs placed at opposite ends of the
day: 36 agent sessions. The agent's patch is compared by script against the one the
maintainers actually wrote.

| Per ticket | without | with the package | |
|---|---|---|---|
| Tokens | 738,974 | **464,192** | **−37.2%** |
| Cost | $0.560 | **$0.450** | **−19.7%** |
| Model turns | 27.1 | **17.1** | **−37.0%** ✓ |
| Tool calls | 29.2 | **19.2** | **−34.1%** ✓ |
| Fix landed on the right file, of 9 | 4.5 | 4.0 | a tie |
| Sessions past 40 tool calls | 4 of 18 | 0 of 18 | |

✓ marks a difference that held on all ten resamplings and in both replicates. A row without
one moved but did not clear that bar, and is printed anyway.

## Fitting the package to this repository, measured on its own

One piece of the fitting, measured against the same package without it. 9 tickets,
36 sessions, both arms run twice.

These are a different, question-shaped set of tasks from the table above, graded on how much
of a reference answer the agent covered. The absolute figures are therefore **not comparable
between the two tables** -- only the contrast inside each table is.

| Per ticket | package | package + that piece | |
|---|---|---|---|
| Cost | $0.206 | **$0.202** | **−1.9%** |
| Tool calls | 12.8 | **12.3** | **−4.3%** |
| Model turns | 5.6 | **6.1** | **+10.0%** |
| Answer completeness | 0.766 | 0.789 | +2.9% |

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
python ../tools/estimate.py --files 472 --loc 68824
```

---

[Why these numbers can be believed](../docs/EVIDENCE.md) ·
[What gets installed](../docs/WHAT-IT-DOES.md) ·
[What an engagement looks like](../docs/ENGAGEMENT.md) ·
[Estimate your own repository](../docs/ESTIMATE.md)
