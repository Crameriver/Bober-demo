# What gets installed

## The problem it addresses

Ask an AI coding agent to fix a defect in a codebase it does not know, and most of what you
pay for is not the fix. It is the search: listing directories, grepping for a word that turns
out to mean something else here, reading a whole file to learn it was the wrong file, and
occasionally following a confident wrong guess for forty tool calls.

That cost is not a property of the model. It is a property of **how much a newcomer has to
rule out before they can start** — and that is a property of your repository.

```
without                                                    with the package
────────────────────────────────────────────────────       ──────────────────────────
ls · grep · read · grep · read · wrong file · read         orient · read · read
grep · read · read · ls · grep · read · right file         right file · fix · verify
fix · guess how to test · guess again · verify
                                                            ~40% fewer tokens
26 tool calls, 1 session in 7 past forty                    1 session in 22 past forty
```

## What the package is

One package, installed into your repository and then fitted to it:

**A context engine.** It decides what the agent is told and when. It is the part that makes
the rest arrive at the moment it is useful rather than sitting in the agent's context
costing money on every turn.

**An index of your code.** Built over your repository, kept current as the repository moves.

**Project memory.** What the team — human or agent — has already established, carried from
one session to the next instead of rediscovered.

**Retrieval tuned to your repository.** Not a generic search over a generic corpus: the
retrieval knows this repository's vocabulary, its conventions, and which of its names are
misleading.

**Delivery at the moment it matters.** The package acts when an agent is about to go the
wrong way, rather than by filling its context up front. This is the part that most
distinguishes it from a document you write and hope gets read — and we have measured the
difference between the two.

**The benchmark.** The instrument that measured all of the above, left with you, so the
next person can check the claim instead of trusting it. See
[the kits](../README.md#the-benchmark-is-part-of-the-deliverable).

## What the fitting is

Installing is an afternoon. Fitting is the work: finding what is ambiguous in *this*
repository — which concept wears two names, which directory is frozen, which file looks like
the one you want and is not, how this project is actually built and verified — and wiring
that into the package so it arrives at the right moment.

Fitting is measured, not asserted. Each piece of it is run against the same package without
it, on tickets from your own history, and a piece that does not earn its place is removed
rather than shipped. The second study on the landing page is one such measurement, published
with the four codebases where the answer was *no effect*.

## What it does not do

**It does not make the agent cleverer.** Across 56 tickets the fix landed on the right file
40.5 times without the package and 42.5 times with it — a difference inside what the
benchmark produces by chance. Every page here says so. If someone offers you both cheaper
*and* smarter from a context layer, ask to see the quality row.

**It does not change your code.** Nothing it installs is compiled into your product. It is
configuration, context and tooling that sit beside the repository.

**It does not send your code anywhere.** The package runs locally, beside the agent you
already use. The estimator in this repository reads file names and counts lines and has no
network access at all.

**It does not depend on one model or one vendor.** It shapes what the agent is told; it does
not care which agent.

**It does not always pay.** On an eighty-file utility, the measured gain was 12% of tokens
and nothing we could establish. That codebase has [its own page](../jq/) saying so.

## Why there are no per-component numbers

The numbers published here belong to the package as a whole. That is a deliberate choice,
and it is the honest one: when we measured components individually, several of the obvious
ones turned out to be worth nothing or worse — a ranked list of likely files *lost* six
tickets of eighteen, an index exposed as tools the agent could call was never called in 205
sessions, and a command named in the agent's own context was never run in 212. Those are on
the landing page under *what we measured and threw away*.

A vendor who gives you a number per component is either measuring at a level that cannot
support it, or has not tried to refute any of them.

---

[Why these numbers can be believed](EVIDENCE.md) ·
[What an engagement looks like](ENGAGEMENT.md) ·
[Estimate your own repository](ESTIMATE.md)
