# Rocket.Chat

**TypeScript · 7,454 source files · 503,665 lines · [https://github.com/RocketChat/Rocket.Chat](https://github.com/RocketChat/Rocket.Chat) · MIT**

One feature carries two names across a monorepo, and a second tree inside
it holds components named like the ones in the main application — so a plausible-looking edit
can land in an embedded widget nobody asked about. A frozen legacy tree still looks alive.
This produced the largest reduction we have ever measured, 52% of tokens, **and we do not
claim it**: the treatment arm's two runs differed from each other by more than our test could
absorb, so by our own rule every number on this page is reported unread. The direction was the
same in both runs and on every metric. It is still not a claim, and it is still printed.

## What was measured here

12 real defect tickets from this project's own history. Each ticket was run twice with
nothing installed and twice with the package installed, in runs placed at opposite ends of the
day: 48 agent sessions. The agent's patch is compared by script against the one the
maintainers actually wrote.

| Per ticket | without | with the package | |
|---|---|---|---|
| Tokens | 873,703 | **419,059** | **−52.0%** **unread** |
| Cost | $0.631 | **$0.403** | **−36.1%** **unread** |
| Model turns | 29.8 | **14.6** | **−51.0%** **unread** |
| Tool calls | 30.5 | **20.7** | **−32.0%** **unread** |
| Fix landed on the right file, of 12 | 11.5 | 11.0 | a tie |
| Sessions past 40 tool calls | 7 of 24 | 2 of 24 | |

✓ marks a difference that held on all ten resamplings and in both replicates. A row without
one moved but did not clear that bar, and is printed anyway. A row marked **unread** is one our replicate check vetoed: not a small effect, no answer.

## Why there is no benchmark kit here

Six of the nine codebases in this repository ship one. This is not one of them: the second
study was not run on this codebase, and we do not hand over an instrument we have not run
against it ourselves. What is published above is the first study, which is the measurement
that matters most — the package against nothing at all.

An engagement builds the kit for your repository, from your own history, and you keep it.
See [what an engagement leaves behind](../docs/ENGAGEMENT.md).

## Estimate it for a repository this size

```
python ../tools/estimate.py --files 7454 --loc 503665
```

---

[Why these numbers can be believed](../docs/EVIDENCE.md) ·
[What gets installed](../docs/WHAT-IT-DOES.md) ·
[What an engagement looks like](../docs/ENGAGEMENT.md) ·
[Estimate your own repository](../docs/ESTIMATE.md)
