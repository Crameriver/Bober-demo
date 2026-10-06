# Why these numbers can be believed

Short version: the benchmark is pointed at our own work at least as hard as at the control,
four specific guards exist because each one caught us publishing something false, and the
instrument that produced the per-codebase numbers [ships with the
codebases](../README.md#the-benchmark-is-part-of-the-deliverable) so you can re-run it.

## The design

```
one ticket from the project's own history
        │
        ├── run 1   nothing installed      ─┐
        ├── run 2   package installed       ├─ early in the day
        │                                   │
        ├── run 3   package installed      ─┤
        └── run 4   nothing installed      ─┘  late in the day

        fresh checkout at the parent commit every time
        the maintainers' own fix is removed and kept as the answer key
```

* **The tickets are real.** Each one is a defect from that project's history. We take the
  commit that fixed it, revert it, and hand the agent the issue as the maintainers received
  it. We check with `git apply` that the maintainers' fix would still apply to the tree we
  hand over — otherwise we would be scoring against a fix that no longer fits, which is
  scoring a fiction.
* **Fresh checkout every session.** No session inherits another's state.
* **Both arms run twice, at opposite ends of the day, in opposite order.** The second pair
  is not redundancy. It is the measurement of the day's own drift, and it is used against
  us — see the veto below.
* **Grading is by script, not by judgement.** The patch the agent produces is compared to
  the patch the maintainers wrote. "Landed on the right file" means the agent changed a file
  their fix also changed.
* **Both arms are given the same output contract and the same tools.** We once ran a control
  arm that tried to edit files and was refused permission, which manufactured the five
  largest wins in that round. Arm symmetry is now checked before a round is read.
* **The agent's configuration is isolated per session.** This machine has other context
  tooling installed; a session that inherited it would not be a control. A control that does
  not do the work makes the treatment look free, which is the worst defect an instrument can
  have.

## What each metric means, exactly

| | |
|---|---|
| **Tokens** | the agent CLI's own usage record, summed over input, output, cache-write and cache-read. Not an estimate from text length |
| **Cost** | those four token classes at their list prices |
| **Model turns** | assistant messages in the transcript — how many times the model had to think again |
| **Tool calls** | tool-use blocks in the transcript |
| **Runaway session** | a session that passed forty tool calls |
| **Right file** | the agent's patch touched a file the maintainers' patch touched |
| **Answer completeness** | on question-shaped tickets, how much of the reference answer the agent's answer covered |

We publish *model turns* and not the CLI's own turn counter, because the two disagree in
sign on one codebase and we would rather name the quantity precisely than pick the flattering
one. Both are in the data.

## The four guards, each bought with a retracted result

**1. A mechanism is counted by an event it logs itself, never by its own installation.**
We once read a result out of a context file that was written into 106 sessions, with its
byte count on every row as proof — and opened by exactly one of them. Every mechanism now
writes a line when it fires, and a round whose fidelity line is not what we expect is not
read at all.

**2. The difference between an arm and itself is a veto.** Each arm runs twice. If that
self-difference passes the same test as a real effect, then on that day, on that repository,
the test cannot tell the two apart — and the metric is reported **unread**. Not explained
away as drift. Unread. This rule costs us the largest number we have ever measured: 52% of
tokens on [Rocket.Chat](../rocketchat/), printed there and not claimed.

**3. Ten bootstrap seeds, and both replicate strata.** An interval is computed for ten
different seeds and counts only if all ten agree, and the same contrast is computed inside
each replicate separately, where the two arms ran back to back. Two identical arms once
cleared a single-seed bar.

**4. A session that returns one turn and no answer is an error, not a score of zero.**
Scoring it silently credits the other arm. We found this in our own control arm, where it
was making the treatment look free.

## The verdict vocabulary

| | |
|---|---|
| **established** | the interval excluded zero on all ten seeds **and** in both replicates |
| *one stratum only* | cleared pooled, cleared in one replicate — printed, not claimed |
| *not established* | this repository and this number of tickets could not tell. **Not** "a small effect": no answer |
| **unread** | the veto fired. The instrument was noisier than the effect on the day it ran. Run more cases or more replicates; do not reinterpret |

Twelve tickets per codebase is enough to establish a pooled effect across five codebases and
often not enough to establish a per-repository one. Both of those facts are on the landing
table rather than only the convenient one.

## What is established, and what is not

Pooled over all 56 tickets, five codebases, 224 sessions: tokens **−40.5%**, cost
**−30.0%**, model turns **−42.9%**, all established. Tool calls −26.7%, one stratum only.
Quality 40.5 → 42.5 of 56, a tie.

Per codebase, only [SuiteCRM](../suitecrm/) establishes its own token reduction;
[Keycloak](../keycloak/) and [mitmproxy](../mitmproxy/) establish other metrics;
[jq](../jq/) establishes nothing; [Rocket.Chat](../rocketchat/) is unread. Each page says
which.

## Things we published and then withdrew

* a 52% token reduction, withdrawn as a claim by guard 2 — and still printed;
* a result read from a file that one session in 106 had opened, withdrawn by guard 1;
* a headline that turned out to be an artefact of the stand-in value chosen for "never
  happened": +5.9 at one stand-in, +1.3 at another, −0.2 on complete cases only. Metrics
  that need a stand-in are now reported at two of them and on complete cases;
* a cost saving against a drifting control arm, withdrawn once the control was re-run.

## Re-running it yourself

Six codebases here ship the instrument: [jq](../jq/kit/), [mitmproxy](../mitmproxy/kit/),
[Polly](../polly/kit/), [Hugo](../hugo/kit/), [bat](../bat/kit/),
[Phoenix](../phoenix/kit/). Python standard library, no dependency on anything of ours, and
it runs against your own checkout. Each kit also carries the audit trail of what was dropped
from its own page and why.

This repository also checks itself:

```
python tools/check_repo.py       # the pages, the landing table and the estimator must agree
python tools/test_estimate.py    # the estimator's own tests
```

---

[What gets installed](WHAT-IT-DOES.md) · [What an engagement looks like](ENGAGEMENT.md) ·
[Estimate your own repository](ESTIMATE.md)
