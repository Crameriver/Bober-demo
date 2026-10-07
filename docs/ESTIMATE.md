# What will it save on your codebase?

One command, about a minute, no install and no network.

## 1. Point it at a checkout

```
python tools/estimate.py --scan /path/to/your/checkout
```

It counts your source files and lines — it never reads the contents of your code — and prints
the percentage of tokens you can expect to save:

```
  ESTIMATED TOKEN REDUCTION PER TICKET

      33% to 55%        central estimate 44%

  your codebase    4,200 source files, 610,000 lines (145 per file)
  which is         large: several teams, or one long-lived product
```

Safe to run on a private repository, including during a call with us.

## 2. Or just give it two numbers

If you already know roughly how big the codebase is:

```
python tools/estimate.py --files 4200 --loc 610000
```

## 3. Add your spend to see it in money

```
python tools/estimate.py --files 4200 --loc 610000 --monthly-spend 9000
```

```
  at 9,000 a month in agent spend, that is 2,970 to 4,950 a month back,
  or 3,960 at the central estimate.
```

Any currency — it applies the percentage to the number you give it. Multiply the band by hand and
you will get our figure; we made that a test.

## Want the whole picture at once?

```
python tools/estimate.py --table
```

prints what we measured and what it predicts at every size, which is the page to have open when
someone asks "and for a codebase of about *this* size?"

```
    source files           range   central
              50       5% to 27%       16%
             150      12% to 34%       23%
             500      19% to 42%       31%
           1,500      26% to 49%       38%
           5,000      34% to 55%       45%
           7,454      37% to 55%       48%
```

Add `--json` for a machine-readable version if you want to put it in a spreadsheet.

## Why a range and not a single number

The model is fitted on five codebases we measured end to end — 56 tickets, 224 agent sessions,
each ticket run twice with our infrastructure in place and twice without:

| Codebase | Language | Source files | Lines of code | Measured | Fit |
|---|---|---|---|---|---|
| Rocket.Chat | TypeScript | 7,454 | 503,665 | 52% | 48% |
| Keycloak | Java | 6,326 | 764,287 | 38% | 47% |
| SuiteCRM | PHP | 4,797 | 914,599 | 46% | 45% |
| mitmproxy | Python | 472 | 68,824 | 37% | 30% |
| jq | C | 48 | 26,655 | 12% | 16% |

Five codebases is five codebases, so the band is the fit plus and minus two typical misses, and
three limits are built in rather than left to the reader:

* **it will not print above 55%**, because 52% is the largest reduction we have ever measured and
  going past it would be arithmetic rather than evidence;
* **above 7,454 files it stops climbing** and holds at our largest measured codebase;
* **what we stand behind is the pooled figure** — a 40.5% token reduction across all 56 tickets,
  which clears the bar described in [how we measure](EVIDENCE.md). The five rows above are the
  single measurements it is fitted to.

## Why the file count does not have to be exact

Whether you count tests, generated files and vendored code moves a typical codebase's file count
by tens of percent. Every run tells you what a miscount that large would do:

```
  Miscounting your files by 40% moves this by 5 points against a band 22 points wide,
  so the exact count is not worth arguing about.
```

If you use `--scan`, you are counted by exactly the scanner that produced the five file counts
above — which is why that scanner ships with the tool instead of being described in a document.

Lines of code do not drive the estimate. They turn the percentage into a volume you recognise, and
they flag a codebase whose average file is far outside the 65–560 line range of the five we
calibrated on, where a file count stops meaning what it meant here.

## What the estimate is not

It is not a quote. An engagement [starts by running the real measurement](ENGAGEMENT.md) on your
own repository — the same instrument, the same bar — which replaces this band with a number, and
you keep the instrument that produced it.

And whatever the band says: **the quality of the answer does not change.** Across 56 tickets the
fix landed on the right file 40.5 times without us and 42.5 times with us, a difference inside
what the benchmark produces by chance. This makes your agent cheaper and far more predictable. It
does not make it cleverer, and we would rather you heard that from us.

---

[What we set up](WHAT-IT-DOES.md) · [How we measure](EVIDENCE.md) ·
[How an engagement runs](ENGAGEMENT.md)
