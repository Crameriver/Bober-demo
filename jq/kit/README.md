# Your benchmark — jq (C)

This measures whether a piece of context infrastructure actually helps an AI coding agent
**on this codebase**. It is the instrument, not the infrastructure: it answers a question
rather than making a claim, and it is yours to keep and re-run.

## Why we hand over a measuring tool

Because a context setup that you cannot re-measure is one you cannot maintain. Your
repository moves, your model changes, and the number we quoted on day one stops being
the number. With this you produce it again yourself, in an afternoon, without us.

It also tells you which case you are in. Across 9 open-source codebases
and 344 sessions, the piece of tuning this kit isolates cut tool calls
10.6% and cost 8.9% — but it pays most
where a codebase's build and verification are hard to guess, and least where they answer
to a command an agent works out by itself. Your repository decides which, and this tells
you which.

## Running it

Python 3.11+, no dependencies. Your agent CLI must be on your PATH and authenticated.

```
export KIT_TREE=/path/to/a/clean/checkout/of/this/repo
python bench/run.py --arm bare  --rep r1
python bench/run.py --arm facts --rep r1
python bench/run.py --arm bare  --rep r2
python bench/run.py --arm facts --rep r2
python bench/analyse.py
```

`--arm bare` installs **nothing at all**; `--arm facts` injects the fact sheet beside this
file. So this kit compares that sheet against a plain agent — a wider baseline than the
one our own figures in `RESULTS.md` use, and that page explains the difference.

Run **both replicates of both arms**. They are not redundancy: the difference between an
arm and itself is that day's noise floor, and `analyse.py` uses it as a veto. A row where
an arm differs from itself is left unread. There are 10 cases here, so a full run
is 40 sessions.

`run.py` is resume-safe: a row already written is not re-run. If a session fails, delete
its row and run again.

## What is measured

**Architecture questions** (10 cases). A question about this codebase with an
answer key of files. The score is how much of the key the reply names, over the subset of
the key the fact sheet does **not** itself contain — otherwise the arm carrying the sheet
would score free marks. That subset was fixed before any run.

## What it cannot tell you

The answer keys were built by reading this codebase, then put through three independent
passes: one checked that every keyed path exists and belongs, one was required to state
what makes a reply right and to name the weakest questions, and one repaired the keys the
second judged incomplete. A fourth swept every question for a second defensible answer and
narrowed the ones that had one. They compare two arms fairly — the same key for both,
derived from neither — but the absolute level still means little.

One codebase, one task shape, and the number of cases here. An effect smaller than the
noise floor reads as *not established*, which means this run could not tell — not that the
effect is small.

## Extending it

Add a case: a directory under `cases/` with `prompt.md` and a `gold.json` carrying
`files`. Add a fact: see `facts-audit.md`, which records what we kept while tuning this
codebase, what we discarded, and the check used for each.
