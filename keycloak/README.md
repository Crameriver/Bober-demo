# Keycloak

**Java · 6,326 source files · 764,287 lines of code · [https://github.com/keycloak/keycloak](https://github.com/keycloak/keycloak) · Apache-2.0**

A large Java product with a conventional build and an unconventional amount of
indirection: service provider interfaces, generated code, and several modules whose names differ
from the concepts they implement. Model turns fell by more than half here and held up under every
check — on a codebase this size, the saving is mostly the search your agent no longer has to
do.

## What we measured here

11 real defect tickets from this project's own history. Each ticket ran twice with nothing
installed and twice with our setup in place, in runs placed at opposite ends of the day:
44 agent sessions. The patch the agent produced is compared by script against the one the
maintainers wrote.

| Per ticket | without us | with us | |
|---|---|---|---|
| Tokens | 631,468 | **393,966** | **−37.6%** |
| Cost | $0.731 | **$0.454** | **−37.9%** |
| Model turns | 28.0 | **12.9** | **−54.0%** ✓ |
| Tool calls | 29.3 | **22.2** | **−24.3%** |
| Fix landed on the right file, of 11 | 7.5 | 8.5 | up, too small to claim |
| Sessions past 40 tool calls | 3 of 22 | 3 of 22 | |

✓ marks a row that cleared [the bar](../docs/EVIDENCE.md#the-bar) — ten resamplings, both
replicates, and the arm quiet against itself. A row without one is the measurement as taken on
11 tickets; the figure we stand behind across all five codebases is a **−40.5%** token
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
| Cost | $0.238 | **$0.231** | **−2.9%** |
| Tool calls | 16.6 | **15.9** | **−4.3%** |
| Model turns | 7.4 | **7.2** | **−2.8%** |
| Answer completeness | 0.839 | 0.904 | +7.9% |

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
python ../tools/estimate.py --files 6326 --loc 764287
```

---

[How we measure](../docs/EVIDENCE.md) ·
[What we set up](../docs/WHAT-IT-DOES.md) ·
[How an engagement runs](../docs/ENGAGEMENT.md) ·
[What will it save on your codebase?](../docs/ESTIMATE.md)
