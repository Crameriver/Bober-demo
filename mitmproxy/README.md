# mitmproxy

**Python · 472 source files · 68,824 lines of code · [https://github.com/mitmproxy/mitmproxy](https://github.com/mitmproxy/mitmproxy) · MIT**

A mid-sized Python codebase with a clean layout and an addon system that
spreads one behaviour across several files. Model turns and tool calls both fell by a third and
held up. Every session that had been running away stopped running away.

## What we measured here

9 real defect tickets from this project's own history. Each ticket ran twice with nothing
installed and twice with our setup in place, in runs placed at opposite ends of the day:
36 agent sessions. The patch the agent produced is compared by script against the one the
maintainers wrote.

| Per ticket | without us | with us | |
|---|---|---|---|
| Tokens | 738,974 | **464,192** | **−37.2%** |
| Cost | $0.560 | **$0.450** | **−19.7%** |
| Model turns | 27.1 | **17.1** | **−37.0%** ✓ |
| Tool calls | 29.2 | **19.2** | **−34.1%** ✓ |
| Fix landed on the right file, of 9 | 4.5 | 4.0 | a tie |
| Sessions past 40 tool calls | 4 of 18 | 0 of 18 | |

✓ marks a row that cleared [the bar](../docs/EVIDENCE.md#the-bar) — ten resamplings, both
replicates, and the arm quiet against itself. A row without one is the measurement as taken on
9 tickets; the figure we stand behind across all five codebases is a **−40.5%** token
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
| Cost | $0.206 | **$0.202** | **−1.9%** |
| Tool calls | 12.8 | **12.3** | **−4.3%** |
| Model turns | 5.6 | **6.1** | **+10.0%** |
| Answer completeness | 0.766 | 0.789 | +2.9% |

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
python ../tools/estimate.py --files 472 --loc 68824
```

---

[How we measure](../docs/EVIDENCE.md) ·
[What we set up](../docs/WHAT-IT-DOES.md) ·
[How an engagement runs](../docs/ENGAGEMENT.md) ·
[What will it save on your codebase?](../docs/ESTIMATE.md)
