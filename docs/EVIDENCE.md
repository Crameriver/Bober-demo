# How we measure

Short version: we run your own tickets both ways, four times each, and we only quote a figure that
clears a bar most vendors do not set. The instrument that produced every number in this repository
[ships with the codebases](../README.md#the-measurement-is-a-service-not-a-hand-off), so you can
re-run it yourself.

## The design

```
one ticket from the project's own history
        │
        ├── run 1   nothing installed       ─┐
        ├── run 2   our setup in place       ├─ early in the day
        │                                    │
        ├── run 3   our setup in place      ─┤
        └── run 4   nothing installed       ─┘  late in the day

        fresh checkout at the parent commit every time
        the maintainers' own fix removed, and kept as the answer key
```

* **The tickets are real.** Each one is a defect from that project's history. We take the commit
  that fixed it, revert it, and hand the agent the issue as the maintainers received it. We check
  with `git apply` that their fix would still apply to the tree we hand over, so we are never
  scoring against a fix that no longer fits.
* **Fresh checkout every session.** No session inherits another's state.
* **Both ways, twice, at opposite ends of the day.** The second pair is not redundancy. It
  measures the day's own drift, and we use it against ourselves — see the bar below.
* **Grading is by script, not by opinion.** The patch your agent produces is compared to the patch
  the maintainers wrote. "Landed on the right file" means it changed a file their fix also changed.
* **Both arms get the same tools and the same output contract**, checked before a round is read.
* **The agent's configuration is isolated per session**, so nothing on the measuring machine
  leaks into either arm.

## The bar

A figure is **established** only when:

1. the 95% bootstrap interval excludes zero **on all ten resamplings**, not a lucky one;
2. the same contrast holds **inside each of the two replicates** separately, where the two arms
   ran back to back;
3. and the difference between an arm and **itself** — its two runs of the same ticket — stays
   quiet on that metric. If an arm differs from itself by more than the effect, the instrument was
   noisier than the thing being measured that day, and the row is left unread rather than
   explained away.

Anything that moves but does not clear all three is printed as what it is: a measurement this many
cases could not resolve. **Not established does not mean small — it means no answer.**

Two more rules keep the instrument honest:

* **a mechanism is counted by an event it logs itself**, never by its own installation. A file
  written into a session is not a file read, so everything we install writes a line when it
  actually fires, and a round whose fidelity line is wrong is not read at all;
* **a session that returns one turn and no answer is an error, not a score of zero**, because
  scoring it silently credits the other arm.

## What each row means, exactly

| | |
|---|---|
| **Tokens** | the agent CLI's own usage record, summed over input, output, cache-write and cache-read. Not an estimate from text length |
| **Cost** | those four token classes at list prices |
| **Model turns** | assistant messages in the transcript — how many times the model had to think again |
| **Tool calls** | tool-use blocks in the transcript |
| **Runaway session** | a session that passed forty tool calls |
| **Right file** | your agent's patch touched a file the maintainers' patch touched |
| **Answer completeness** | on question-shaped tickets, how much of the reference answer the reply covered |

We report *model turns* rather than the CLI's own turn counter, because the two count different
things and we would rather name the quantity precisely than pick the flattering one.

## What is established, and where

Pooled over all 56 tickets on five codebases, 224 sessions: tokens **−40.5%**, cost **−30.0%**,
model turns **−42.9%**, all clearing the bar. Tool calls −26.7%, which held pooled and in one
replicate. The fix landed on the right file 40.5 times of 56 without us and 42.5 with us — a tie,
and we say so first.

For the tuning measured on its own: pooled over nine codebases and 344 sessions, tool calls
**−10.6%** and cost **−8.9%**, both clearing the bar. Per codebase it clears it on
[jq](../jq/) and [Polly](../polly/); elsewhere the effect is smaller than ten or so cases can
separate from noise, which is why the pooled figure is the one we quote.

Each codebase page shows that codebase's own table, with a tick on the rows that cleared the bar.

## Running it yourself

Every codebase here ships the instrument: [jq](../jq/kit/), [mitmproxy](../mitmproxy/kit/),
[Polly](../polly/kit/), [Hugo](../hugo/kit/), [bat](../bat/kit/), [Phoenix](../phoenix/kit/),
[Rocket.Chat](../rocketchat/kit/), [SuiteCRM](../suitecrm/kit/), [Keycloak](../keycloak/kit/).
Python standard library, no dependency on anything of ours, and it runs against your own checkout.
Each one also carries the record of what we kept while tuning that codebase and what we discarded.

This repository checks itself too:

```
python tools/check_repo.py       # the pages, the headline table and the estimator must agree
python tools/test_estimate.py    # the estimator's own tests
```

---

[What we set up](WHAT-IT-DOES.md) · [How an engagement runs](ENGAGEMENT.md) ·
[What will it save on your codebase?](ESTIMATE.md)
