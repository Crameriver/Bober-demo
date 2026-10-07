# What we measured on this codebase (C#)

The rest of the infrastructure WITHOUT the fact sheet in this kit, against the same
infrastructure WITH it. Each arm ran twice, at opposite ends of the day, on
10 cases — 40 sessions.

| Per case | our infrastructure | + the fact sheet | |
|---|---|---|---|
| tool calls | 15.15 | 12.65 | -16.5% |
| cost per case | $0.2170 | $0.1730 | -20.3% |
| model turns | 6.45 | 5.90 | -8.5% |
| answer completeness | 0.594 | 0.509 | -0.084 |

**This one clears the bar.** Tool calls 16.5% lower, cost per case 20.3% lower, holding across ten resamplings and in both replicates — a figure we quote. Model turns 8.5% lower, moving the same way but by less than 10 cases can separate from noise.

## Your own run uses a wider baseline, on purpose

Read this before comparing your number to ours.

The table above isolates one piece of the tuning: both arms had the rest of the
infrastructure in place and only the fact sheet differed. That is the right comparison
for deciding whether that piece earns its keep, which is the decision we had to make.

`bench/run.py` answers a more useful question for you. `--arm bare` installs **nothing at
all**, so your comparison is the fact sheet against a plain agent on your own machine.
That baseline is wider than ours, so your number will usually be larger — and it answers
what you actually want to know: *does this help my team today*.

Neither run tells you what the whole infrastructure would do on your codebase. That takes
a measurement on tickets from your own history, which is where an engagement starts.

## What we quote, across all 9 codebases

The same piece of tuning, measured the same way on 9 open-source codebases and 344 agent sessions:

| Over all 86 tickets | without it | with it | |
|---|---|---|---|
| tool calls | 15.13 | **13.52** | **-10.6%** |
| cost per case | $0.2322 | **$0.2116** | **-8.9%** |

Both clear the bar: the 95% interval excludes zero on all ten resamplings and in each of
two independent replicates. And both are measured **on top of** everything else already
in place, so this is what one piece of the tuning adds by itself.

It pays most where a codebase's build and verification are hard to guess, and least where
they answer to a command an agent works out by itself. Which case you are in is what this
kit is for.

### How the completeness row is scored

A key file whose name the fact sheet already contains is struck off before scoring, so
the arm carrying the sheet is never credited for naming a file the sheet handed it. That
subset is identical for both arms, and it is the one the completeness row uses.
