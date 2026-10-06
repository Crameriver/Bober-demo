# Benchmark kit — bat (Rust)

This measures whether a piece of context infrastructure actually helps an AI coding agent
**on this repository**. It is the instrument, not the infrastructure: it answers a question
rather than making a claim.

## Why you are being given a measuring tool

Across our own measurement campaigns on nine open-source repositories we measured most of
the things people push at coding agents. A ranked list of candidate files, right on half the cases,
**lost** six cases of eighteen and won none, because an agent follows a confident wrong
answer and does not recover. A hand-written page of advice and guard rules cost 16% more
for no gain. A set of tools granted over MCP was called zero times in 205 sessions. A
command naming itself in the agent's context was never run, even on tasks where the agent
used a shell five times.

One thing worked, on two repositories of six: a short page of facts that cannot go stale —
how this project is built and tested, what each directory is for, which files change
together — injected into the session rather than left in a file to be opened.

So the useful deliverable is the one that tells you which case you are in.

## Running it

Python 3.11+, no dependencies. The agent CLI must be on your PATH and authenticated.

```
export KIT_TREE=/path/to/a/clean/checkout/of/this/repo
python bench/run.py --arm bare  --rep r1
python bench/run.py --arm facts --rep r1
python bench/run.py --arm bare  --rep r2
python bench/run.py --arm facts --rep r2
python bench/analyse.py
```

Run **both replicates of both arms**. They are not redundancy: the difference between an
arm and itself is the noise floor of the day, and `analyse.py` uses it as a veto. A metric
where an arm differs from itself is reported unread. There are 8 cases here, so a
full run is 32 sessions.

`run.py` is resume-safe: a row already written is not re-run. If a session fails, delete
its row and run again.

## What is measured

**Architecture questions** (8 cases). A question about this repository with an
answer key of files. The score is how much of the key the reply names, over the subset of
the key that the fact sheet does **not** itself contain — otherwise the arm carrying the
sheet would score free marks. The subset was fixed before any run.

## What is NOT measured, and you should know it

The answer keys were built by reading this repository and were only partly verified. They
compare two arms fairly — the same key for both, derived from neither — but the absolute
level means little. A key with a spurious file adds noise to both arms equally.

One repository, one task shape, and the number of cases here. An effect smaller than the
noise floor will read as 'not established', which means this run could not tell — not that
the effect is small.

## Extending it

Add a case: a directory under `cases/` with `prompt.md` and a `gold.json` carrying
`files`. For a fix task, add `inversion.patch` and `fail_to_pass`. Add a fact: see
`facts-audit.md`, which records what we kept, what we dropped and why — 40% of the first
draft was dropped, and the reasons are the useful part.
