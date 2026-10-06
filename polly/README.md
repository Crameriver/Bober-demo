# Polly

**C# · 485 source files · 42,234 lines · [https://github.com/App-vNext/Polly](https://github.com/App-vNext/Polly) · BSD-3-Clause**

A .NET resilience library with a build and test path driven by a PowerShell
script — the kind of verification an agent does not guess and burns calls discovering. The
strongest result of the second study: cost fell a fifth and tool calls a sixth, both holding
up under every check.

This codebase was measured in the **second study only**. The package was installed
on it, and what is compared below is one piece of the fitting against the rest of
the package: there is no with-package-against-nothing number for this repository.

## Fitting the package to this repository, measured on its own

One piece of the fitting, measured against the same package without it. 10 tickets,
40 sessions, both arms run twice.

These are a different, question-shaped set of tasks from the table above, graded on how much
of a reference answer the agent covered. The absolute figures are therefore **not comparable
between the two tables** -- only the contrast inside each table is.

| Per ticket | package | package + that piece | |
|---|---|---|---|
| Cost | $0.217 | **$0.173** | **−20.3%** ✓ |
| Tool calls | 15.2 | **12.7** | **−16.5%** ✓ |
| Model turns | 6.5 | **5.9** | **−8.5%** |
| Answer completeness | 0.594 | 0.509 | −14.2% |

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
python ../tools/estimate.py --files 485 --loc 42234
```

---

[Why these numbers can be believed](../docs/EVIDENCE.md) ·
[What gets installed](../docs/WHAT-IT-DOES.md) ·
[What an engagement looks like](../docs/ENGAGEMENT.md) ·
[Estimate your own repository](../docs/ESTIMATE.md)
