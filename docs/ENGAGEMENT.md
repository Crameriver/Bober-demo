# What an engagement looks like

The short version: we measure your repository first, and the measurement is the thing you
are buying even in the case where it tells you not to buy the rest.

```
1. ESTIMATE        your file count and line count            free, minutes
       │           → a band, and whether it is worth measuring
       ▼
2. MEASURE         tickets from your own history, both arms  the baseline
       │           → your number, or "not established"
       ▼
3. INSTALL + FIT   the package, fitted to this repository
       │           → each piece of the fitting measured on your tickets
       ▼
4. RE-MEASURE      the same tickets, the same instrument
       │           → the difference, with the same verdicts as every page here
       ▼
5. HAND OVER       the package, the benchmark, the cases, the audit trail
                   → you can re-run all of it without us
```

## 1. Estimate — before any conversation

```
python tools/estimate.py --scan /path/to/your/checkout
```

Standard library Python, no network. It gives a band, states what the band is worth, and
says plainly when your repository is the shape where we have measured the least.

If the band is narrow and low, that is the end of it and it cost you nothing.
→ [How to read the estimate](ESTIMATE.md)

## 2. Measure — the baseline, on your tickets

We build cases from your own history: defects whose fix is in the repository, so there is an
answer key nobody can argue with. The agent runs with nothing installed, twice. That is your
baseline, and it is also the first useful deliverable — most teams have never measured what
their agent sessions actually cost per ticket, or how often one runs away.

We check that each case is still well-formed before it is scored, and we tell you how many
cases we could build. Fewer than about ten and the instrument will mostly say *not
established*; we say that up front rather than afterwards.

## 3. Install and fit

Installing is an afternoon. Fitting is the work, and it is where the engagement's time goes:
finding what is ambiguous in this repository and wiring it so the package acts at the right
moment. [What gets installed](WHAT-IT-DOES.md) describes the pieces.

Each piece of the fitting is measured against the same package without it. A piece that does
not earn its place is removed, not shipped. We have removed more pieces than we have kept —
the landing page lists six mechanisms we threw away, one of which had been in the product
for a month.

## 4. Re-measure

The same tickets, the same instrument, the same four guards, the same verdict vocabulary you
can read on any page in this repository. You get the full table, including the rows that did
not clear the bar and the rows the replicate check vetoed.

**If it comes back flat, we say so.** That is not a courtesy; it is the only thing that makes
the other numbers worth anything. On [jq](../jq/) our answer was that a codebase that size
should not buy the package, and that page is in the same table as the 52% one.

## 5. Hand over

You keep:

* **the package**, installed and fitted, running beside the agent you already use;
* **the benchmark**: the cases from your history, the runner, the analysis with its guards;
* **the audit trail** — what was drafted for your fitting, what was dropped, and why. On the
  codebases here that ratio was about 123 facts kept of 211 drafted;
* **the numbers**, yours to re-run when the repository moves or the model changes.

Nothing in the hand-over needs us. That is deliberate: a context infrastructure you cannot
re-measure is a context infrastructure you cannot maintain.

## What we will not do

* quote from a size estimate alone — the estimate is calibrated on five codebases and says so;
* claim a per-component number, because when we measured components one at a time, several of
  the obvious ones were worth nothing;
* claim better answers. The package makes an agent cheaper and far more predictable. Quality
  was a tie across 56 tickets and every page here says so;
* invoice against a result our own instrument calls *unread*.

---

[What gets installed](WHAT-IT-DOES.md) · [Why these numbers can be believed](EVIDENCE.md) ·
[Estimate your own repository](ESTIMATE.md)
