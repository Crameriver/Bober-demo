# Rocket.Chat

**TypeScript · 7,454 source files · 503,665 lines of code · [https://github.com/RocketChat/Rocket.Chat](https://github.com/RocketChat/Rocket.Chat) · MIT**

One feature wears two names across a monorepo, and a second tree inside it
holds components named like the ones in the main application — so a plausible-looking edit can
land in an embedded widget nobody asked about. A frozen legacy tree still looks alive. This is the
largest reduction we have ever measured, and it is the shape of codebase where we are most
useful: the more a newcomer has to rule out, the more there is to save.

## What we measured here

12 real defect tickets from this project's own history. Each ticket ran twice with nothing
installed and twice with our setup in place, in runs placed at opposite ends of the day:
48 agent sessions. The patch the agent produced is compared by script against the one the
maintainers wrote.

| Per ticket | without us | with us | |
|---|---|---|---|
| Tokens | 873,703 | **419,059** | **−52.0%** |
| Cost | $0.631 | **$0.403** | **−36.1%** |
| Model turns | 29.8 | **14.6** | **−51.0%** |
| Tool calls | 30.5 | **20.7** | **−32.0%** |
| Fix landed on the right file, of 12 | 11.5 | 11.0 | a tie |
| Sessions past 40 tool calls | 7 of 24 | 2 of 24 | |

✓ marks a row that cleared [the bar](../docs/EVIDENCE.md#the-bar) — ten resamplings, both
replicates, and the arm quiet against itself. A row without one is the measurement as taken on
12 tickets; the figure we stand behind across all five codebases is a **−40.5%** token
reduction over 56 tickets, which did clear it.

## What one piece of the tuning adds, on its own

The rest of the setup WITHOUT one piece of the tuning, against the same setup WITH it — so this is
what that piece is worth by itself, on top of everything else already in place. 12 tickets,
48 sessions, both arms run twice.

These are question-shaped tasks rather than the defect tickets above, graded on how much of a
reference answer the reply covers, so the two tables are not comparable to each other — only the
contrast inside each one is.

| Per ticket | our setup | + that piece | |
|---|---|---|---|
| Cost | $0.237 | **$0.218** | **−7.8%** |
| Tool calls | 16.5 | **16.5** | **−0.3%** |
| Model turns | 7.0 | **7.1** | **+1.2%** |
| Answer completeness | 0.703 | 0.743 | +5.7% |

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
python ../tools/estimate.py --files 7454 --loc 503665
```

---

[How we measure](../docs/EVIDENCE.md) ·
[What we set up](../docs/WHAT-IT-DOES.md) ·
[How an engagement runs](../docs/ENGAGEMENT.md) ·
[What will it save on your codebase?](../docs/ESTIMATE.md)
