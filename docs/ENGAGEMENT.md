# How an engagement runs

Five steps. The first is free, the second is the one that decides whether the rest is worth doing,
and the last one is why you are not buying a black box.

```
1. ESTIMATE        your file count and line count            free, one minute
       │           → a range, and whether it is worth measuring
       ▼
2. MEASURE         tickets from your own history, both ways  your baseline
       │           → your number, on your codebase
       ▼
3. SET UP + TUNE   installed, then fitted to this repository
       │           → each piece of the tuning measured on your own tickets
       ▼
4. RE-MEASURE      the same tickets, the same instrument
       │           → the difference, against the same bar as every page here
       ▼
5. HAND OVER       the setup, the instrument, the cases, the record
                   → you can produce the number again without us
```

## 1. Estimate — before we have a conversation

```
python tools/estimate.py --scan /path/to/your/checkout
```

Standard-library Python, no network, and it never reads the contents of your code. It prints a
range and says plainly when your codebase is the shape where we have measured the least.

If the range is low, that is the end of it and it cost you nothing.
→ [What will it save on your codebase?](ESTIMATE.md)

## 2. Measure — your baseline, on your tickets

We build cases from your own history: defects whose fix is already in the repository, so there is
an answer key nobody can argue with. Your agent runs those tickets with nothing installed, twice.

That is your baseline, and it is the first thing you get out of this. Most teams have never
measured what an agent session actually costs them per ticket, or how often one runs away. You
will know both before we change anything.

We tell you up front how many cases we could build. Below about ten, the instrument will mostly
say *we cannot tell from this*, and we would rather you heard that now than after the invoice.

## 3. Set up and tune

Setting up is an afternoon. The tuning is where the engagement's time goes: finding what is
ambiguous in your codebase and wiring it so your agent is told the right thing at the right
moment. → [What we set up](WHAT-IT-DOES.md)

Each piece of the tuning is measured against the same setup without it. A piece that does not earn
its keep comes out rather than shipping — and we have taken more out than we have kept.

## 4. Re-measure

The same tickets, the same instrument, the same bar you can read on any page here. You get the
whole table, and the figures we quote back to you are the ones that cleared it.

**If it comes back flat, we say so.** That is not a courtesy; it is the only thing that makes the
other numbers worth anything. On [jq](../jq/) our answer was that a codebase that size should not
buy this, and that page sits in the same table as the 52% one.

## 5. Hand over

You keep:

* **the setup**, installed and tuned, running beside the agent your team already uses;
* **the instrument** — the cases drawn from your history, the runner, the analysis;
* **the record** of what we wrote into the tuning, what we discarded, and the check used for each;
* **the number**, yours to produce again whenever the repository moves or the model changes.

Nothing in the hand-over needs us, and that is deliberate. A context setup you cannot re-measure
is a context setup you cannot maintain — and in twelve months you should be able to tell whether
it is still paying without picking up the phone.

## What we will not do

* **quote from a size estimate alone.** The estimate is fitted on five codebases and says so;
* **claim better answers.** Quality was a tie across 56 tickets, and we put that on every page;
* **bill against a result our own instrument cannot read.** If a run cannot tell, it cannot tell.

---

[What we set up](WHAT-IT-DOES.md) · [How we measure](EVIDENCE.md) ·
[What will it save on your codebase?](ESTIMATE.md)
