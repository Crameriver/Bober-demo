# SuiteCRM

**PHP · 4,797 source files · 914,599 lines of code · [https://github.com/salesagility/SuiteCRM](https://github.com/salesagility/SuiteCRM) · AGPL-3.0**

A long-lived PHP application where the same concept appears as a module, a bean,
a metadata array and a database table, and where the file you want is often not the file the name
suggests. The clearest result of the five: tokens, cost and model turns all fell and all held up
across twelve tickets.

## What we measured here

12 real defect tickets from this project's own history. Each ticket ran twice with nothing
installed and twice with our setup in place, in runs placed at opposite ends of the day:
48 agent sessions. The patch the agent produced is compared by script against the one the
maintainers wrote.

| Per ticket | without us | with us | |
|---|---|---|---|
| Tokens | 716,261 | **389,848** | **−45.6%** ✓ |
| Cost | $0.574 | **$0.393** | **−31.5%** ✓ |
| Model turns | 23.4 | **13.4** | **−42.8%** ✓ |
| Tool calls | 25.0 | **18.0** | **−28.2%** |
| Fix landed on the right file, of 12 | 6.5 | 8.0 | up, too small to claim |
| Sessions past 40 tool calls | 2 of 24 | 0 of 24 | |

✓ marks a row that cleared [the bar](../docs/EVIDENCE.md#the-bar) — ten resamplings, both
replicates, and the arm quiet against itself. A row without one is the measurement as taken on
12 tickets; the figure we stand behind across all five codebases is a **−40.5%** token
reduction over 56 tickets, which did clear it.

## What one piece of the tuning adds, on its own

The rest of the setup WITHOUT one piece of the tuning, against the same setup WITH it — so this is
what that piece is worth by itself, on top of everything else already in place. 9 tickets,
36 sessions, both arms run twice.

These are question-shaped tasks rather than the defect tickets above, graded on how much of a
reference answer the reply covers, so the two tables are not comparable to each other — only the
contrast inside each one is.

| Per ticket | our setup | + that piece | |
|---|---|---|---|
| Cost | $0.274 | **$0.278** | **+1.5%** |
| Tool calls | 15.9 | **16.4** | **+3.1%** |
| Model turns | 6.9 | **6.9** | **+0.0%** |
| Answer completeness | 0.766 | 0.911 | +19.0% |

Across all nine codebases and 344 sessions, that piece cut tool calls **−10.6%** and
cost **−8.9%**, both clearing the bar. It pays most where a codebase's build and verification
are hard to guess, and least where they answer to a command an agent works out by itself — which
is why we measure your codebase before quoting it.

## The instrument stays with you

[`kit/`](kit/) is the measuring tool we used here, self-contained: the cases drawn from this
project's history, the runner, the analysis, and the record of what we kept while tuning this
codebase and what we discarded. Python standard library, no dependency on anything of ours, and it
runs against your own checkout.

```
python kit/bench/run.py --arm bare  --rep r1
python kit/bench/run.py --arm facts --rep r1
python kit/bench/run.py --arm bare  --rep r2
python kit/bench/run.py --arm facts --rep r2
python kit/bench/analyse.py
```

Both replicates of both arms — the difference between an arm and itself is that day's noise floor,
and the analysis uses it as a veto. This is what lets you check the number in twelve months, when
your repository has moved and your model has changed, without picking up the phone.

## What would it save on a codebase this size?

```
python ../tools/estimate.py --files 4797 --loc 914599
```

---

[How we measure](../docs/EVIDENCE.md) ·
[What we set up](../docs/WHAT-IT-DOES.md) ·
[How an engagement runs](../docs/ENGAGEMENT.md) ·
[What will it save on your codebase?](../docs/ESTIMATE.md)
