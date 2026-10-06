# Hugo

**Go · 555 source files · 133,887 lines · [https://github.com/gohugoio/hugo](https://github.com/gohugoio/hugo) · Apache-2.0**

A large Go static site generator with a conventional build: `go test ./...` is
guessed on the first try. Nothing in the second study cleared the bar here, which is the
expected result and the reason the table is printed in full.

This codebase was measured in the **second study only**. The package was installed
on it, and what is compared below is one piece of the fitting against the rest of
the package: there is no with-package-against-nothing number for this repository.

## Fitting the package to this repository, measured on its own

One piece of the fitting, measured against the same package without it. 8 tickets,
32 sessions, both arms run twice.

These are a different, question-shaped set of tasks from the table above, graded on how much
of a reference answer the agent covered. The absolute figures are therefore **not comparable
between the two tables** -- only the contrast inside each table is.

| Per ticket | package | package + that piece | |
|---|---|---|---|
| Cost | $0.225 | **$0.206** | **−8.4%** |
| Tool calls | 13.6 | **11.5** | **−15.2%** |
| Model turns | 6.9 | **6.7** | **−3.6%** |
| Answer completeness | 0.504 | 0.516 | +2.4% |

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
python ../tools/estimate.py --files 555 --loc 133887
```

---

[Why these numbers can be believed](../docs/EVIDENCE.md) ·
[What gets installed](../docs/WHAT-IT-DOES.md) ·
[What an engagement looks like](../docs/ENGAGEMENT.md) ·
[Estimate your own repository](../docs/ESTIMATE.md)
