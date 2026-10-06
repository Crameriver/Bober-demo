# Estimate your own repository

```
python tools/estimate.py --scan /path/to/your/checkout
python tools/estimate.py --files 4797 --loc 914599 --monthly-spend 12000
python tools/estimate.py --table
python tools/estimate.py --files 4797 --loc 914599 --json
```

Python 3, standard library, no dependencies and **no network**. With `--scan` it reads file
names and counts lines; it never reads file contents and nothing leaves your machine.

## What it tells you

```
  ESTIMATED TOKEN REDUCTION PER TICKET

      34% to 55%        central estimate 45%

  your codebase    4,797 source files, 914,599 lines (191 per file)
  which is         large: several teams, or one long-lived product

  at 12,000 a month in agent spend, that is 4,080 to 6,600 a month back,
  or 5,400 at the central estimate.
```

The money line is the printed percentage applied to the spend you gave it, in whatever
currency you gave it. Multiply it by hand and you will get our figure — we made that a test.

## Why a band and not a number

The model is fitted on five codebases we measured end to end. Five points is five points,
and the tool is built to say so rather than to look confident:

```
  codebase      language       files  measured     fit
  Rocket.Chat   TypeScript     7,454       52%     48%
  Keycloak      Java           6,326       38%     47%
  SuiteCRM      PHP            4,797       46%     45%
  mitmproxy     Python           472       37%     30%
  jq            C                 48       12%     16%

  R2 0.83 on 5 codebases, typical miss 5.6 points.
```

The band printed for your repository is the fit plus and minus two of those typical misses.
Three further honesty rules are built in:

* **it will not print above 55%**, because 52% is the largest reduction we have ever
  measured and extrapolating past it would be arithmetic rather than evidence;
* **above 7,454 files it stops climbing** and holds at our largest measured codebase. Below
  our smallest it keeps falling, because that direction errs against us, not against you;
* **of the five points it is fitted on**, one is established on its own, three are
  directional and one is *unread* under [our own replicate rule](EVIDENCE.md). What **is**
  established is the pooled reduction over all 56 tickets: **40.5% of tokens**. Dropping the
  unread point from the fit moves any estimate by at most 2.3 points, against a band 11
  points wide — so keeping it changes nothing you would notice, and we checked that with a
  test rather than asserting it.

## Why the file count does not have to be exact

Whether you count tests, generated files and vendored code changes a typical repository's
file count by tens of percent. Every run prints what a miscount that large would do:

```
  Miscounting your files by 40% moves this by 5 points against a band 22 points wide,
  so the exact count is not worth arguing about.
```

If you use `--scan`, you are measured by exactly the scanner that produced the five file
counts above — which is the reason that scanner ships with the estimator instead of being
described in a document.

## What lines of code are for

They do not drive the estimate. They are used to turn a percentage into a volume you
recognise, and to flag a repository whose average file is far outside the 65–560 line range
of the five we calibrated on. Outside that range a file count stops meaning what it meant
here, and the tool says so instead of answering anyway.

## Bands to quote from

```
    source files           range   central
              50       5% to 27%       16%
             150      12% to 34%       23%
             500      19% to 42%       31%
           1,500      26% to 49%       38%
           5,000      34% to 55%       45%
           7,454      37% to 55%       48%
```

Every row is the same package. What changes is how much an agent has to rule out before it
can start — which is also why a tidy fifty-file utility is a codebase we would tell you not
to buy for. See [jq](../jq/), where we did.

## What it is not

It is not a quote, and it is not a promise. An engagement
[opens by running the real measurement](ENGAGEMENT.md) on your repository — the same
instrument, the same guards, the same verdict vocabulary — which replaces this band with a
number. Including when that number comes back flat.

And whatever the band says: **quality is unchanged**. Across 56 tickets the fix landed on the
right file 40.5 times without the package and 42.5 times with it, a difference inside what
the benchmark produces by chance. This work makes an agent cheaper and far more predictable.
It does not make it cleverer.

---

[What gets installed](WHAT-IT-DOES.md) · [Why these numbers can be believed](EVIDENCE.md) ·
[What an engagement looks like](ENGAGEMENT.md)
