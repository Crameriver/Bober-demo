# What we set up

## The problem we are hired to fix

Ask an AI coding agent to fix a defect in a codebase it does not know, and most of what you pay
for is not the fix. It is the search: listing directories, grepping for a word that turns out to
mean something else here, reading a whole file to learn it was the wrong file, and occasionally
following a confident wrong guess for forty tool calls.

That cost is not a property of the model you chose. It is a property of **how much a newcomer has
to rule out before they can start** — which is a property of your codebase, and therefore
something we can work on.

```
your team today                                            after we have been in
────────────────────────────────────────────────────       ──────────────────────────
ls · grep · read · grep · read · wrong file · read         orient · read · read
grep · read · read · ls · grep · read · right file         right file · fix · verify
fix · guess how to test · guess again · verify
                                                            ~40% fewer tokens
26 tool calls, 1 session in 7 past forty                    1 session in 22 past forty
```

## What we install

One infrastructure, set up inside your repository and then fitted to it:

**A context engine.** It decides what your agent is told, and when. It is the part that makes
everything else arrive at the moment it is useful rather than sitting in the agent's context
costing money on every turn.

**An index of your code**, built over your repository and kept current as the repository moves.

**Project memory.** What your team — human or agent — has already established, carried from one
session to the next instead of rediscovered every morning.

**Retrieval tuned to your repository.** Not a generic search over a generic corpus: it knows your
vocabulary, your conventions, and which of your names are misleading.

**Delivery at the moment it matters.** We act when an agent is about to go the wrong way, rather
than by filling its context up front. This is what most distinguishes the work from a document
somebody writes and hopes gets read — and we have measured the difference between the two.

**The measurement**, run before and after, and then left with you.
→ [How we measure](EVIDENCE.md)

## The tuning is the work

Setting it up is an afternoon. Fitting it is what you are paying for: finding what is ambiguous in
*your* codebase — which concept wears two names, which directory is frozen, which file looks like
the one you want and is not, how the project is actually built and verified — and wiring that in so
it arrives at the right moment.

And the tuning is measured, not asserted. Across nine codebases and 344 agent sessions, one piece
of it on its own cut **tool calls by 10.6% and cost by 8.9%** — both clearing the bar, both on top
of everything else already in place. On [jq](../jq/) that piece alone cut tool calls by 36%; on
[Polly](../polly/) it cut cost by 20%.

It pays most where a codebase's build and verification are hard to guess, and least where they
answer to a command an agent works out by itself. **Your codebase decides which, so we measure
before we promise.**

## What we do not claim

**We do not make your agent cleverer.** Across 56 tickets the fix landed on the right file 40.5
times without us and 42.5 times with us — a difference inside what the benchmark produces by
chance. We say this before you ask, because the first thing a careful engineer on your side will
do is look for the quality row. If a vendor offers you cheaper *and* smarter from a context layer,
ask them for theirs.

**We do not change your code.** Nothing we install is compiled into your product. It is
configuration, context and tooling that sit beside the repository.

**Your code does not leave your machine.** Everything runs locally, beside the agent you already
use. The estimator in this repository has no network access at all.

**We are not tied to one model or one vendor.** We shape what your agent is told; we do not care
which agent it is, and when you change model you re-measure rather than re-buy.

**It does not always pay.** On an eighty-file utility the measured gain was 12% of tokens, and our
advice was not to buy — [that page is still here](../jq/). You get the same answer about your own
codebase before you spend anything with us.

---

[How we measure](EVIDENCE.md) · [How an engagement runs](ENGAGEMENT.md) ·
[What will it save on your codebase?](ESTIMATE.md)
