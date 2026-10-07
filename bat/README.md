# bat

**Rust · 50 source files · 12,594 lines of code · [https://github.com/sharkdp/bat](https://github.com/sharkdp/bat) · MIT OR Apache-2.0**

A Rust command-line tool with the most guessable verification there is: `cargo
test`. A codebase this conventional is where a fact sheet has least to tell an agent, and the
table below shows it.

## What one piece of the tuning adds, on its own

The rest of the setup WITHOUT one piece of the tuning, against the same setup WITH it — so this is
what that piece is worth by itself, on top of everything else already in place. 8 tickets,
32 sessions, both arms run twice.

These are question-shaped tasks rather than the defect tickets above, graded on how much of a
reference answer the reply covers, so the two tables are not comparable to each other — only the
contrast inside each one is.

| Per ticket | our setup | + that piece | |
|---|---|---|---|
| Cost | $0.226 | **$0.210** | **−6.9%** |
| Tool calls | 14.6 | **12.2** | **−16.2%** |
| Model turns | 6.2 | **6.0** | **−3.0%** |
| Answer completeness | 0.509 | 0.530 | +4.0% |

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
python ../tools/estimate.py --files 50 --loc 12594
```

---

[How we measure](../docs/EVIDENCE.md) ·
[What we set up](../docs/WHAT-IT-DOES.md) ·
[How an engagement runs](../docs/ENGAGEMENT.md) ·
[What will it save on your codebase?](../docs/ESTIMATE.md)
