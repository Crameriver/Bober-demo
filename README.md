# Make an AI coding agent cheaper and predictable on *your* codebase

We install a context infrastructure into your repository and then measure what it changed,
on tickets from your own history, against the same agent with nothing installed. Nine public
codebases are worked through here in the open — including the ones where our answer was
"this will not pay".

**Across 56 tickets on five codebases, 224 agent sessions: 40% fewer tokens, 30% lower cost
per ticket, 43% fewer model turns. Two thirds fewer sessions that run away. Answer quality
unchanged.**

| Over all 56 tickets | without | with the package | | |
|---|---|---|---|---|
| Tokens per ticket | 658,137 | **391,356** | **−40.5%** | established |
| Cost per ticket | $0.57 | **$0.40** | **−30.0%** | established |
| Model turns | 24.6 | **14.1** | **−42.9%** | established |
| Tool calls | 26.1 | **19.1** | −26.7% | one stratum only |
| Fix landed on the right file | 40.5 of 56 | 42.5 of 56 | a tie | |
| Sessions past 40 tool calls | 16 of 112 | **5 of 112** | | |

*"Established"* means the 95% interval excluded zero on all ten resamplings **and** in each
of the two independent replicates. Rows that moved but did not clear that bar are printed
anyway, labelled.

## The runaway session is the number to plan around

Without the infrastructure, sixteen sessions of a hundred and twelve went past forty tool
calls, one of them reaching a hundred and sixty-one. With it, five. The cost saving is the
average; this is the variance, and it is what makes an agent's behaviour something you can
put in a sprint. It is also the thing nobody else publishes.

## What it returns depends on your codebase, not on your language

| Codebase | Language | Source files | Tokens | What is established on this repository alone |
|---|---|---|---|---|
| [Rocket.Chat](rocketchat/) | TypeScript | 7,454 | −52% | **nothing — reported unread.** The arm differed from itself by more than the test could absorb, so we do not read this repository's numbers, including the largest one we have ever measured |
| [Keycloak](keycloak/) | Java | 6,326 | −38% | model turns −54% |
| [SuiteCRM](suitecrm/) | PHP | 4,797 | −46% | tokens −46%, cost −32%, model turns −43% |
| [mitmproxy](mitmproxy/) | Python | 472 | −37% | model turns −37%, tool calls −34% |
| [jq](jq/) | C | 48 | −12% | nothing — and at this size our advice is not to buy |

Twelve tickets per codebase is enough to establish a pooled effect and often not enough to
establish a per-repository one. Both facts are on the table above rather than only the
convenient one.

**The pattern that holds:** what the package returns scales with how much a newcomer has to
rule out before they can start. A big product with two names for one feature returns a lot.
A tidy eighty-file utility returns little, and we say so.

## Estimate it for your own repository, before talking to us

```
python tools/estimate.py --scan /path/to/your/checkout
python tools/estimate.py --files 4200 --loc 610000 --monthly-spend 9000
python tools/estimate.py --table
```

Standard library Python, no network, and it reads file names and line counts — never file
contents. It prints a band rather than a number, states what the band is worth, and shows
that miscounting your files by 40% moves the answer less than the band's own width. The
same scanner produced the file counts above, so a scan of your repository is measured the
way the calibration was.

→ [How to read the estimate, and what it is not](docs/ESTIMATE.md)

## What gets installed

One package, fitted to the repository in front of us:

* **a context engine** that decides what the agent is told, and when;
* **an index of your code**, built over your repository and kept current;
* **project memory** — what has already been established, carried from session to session
  instead of rediscovered;
* **retrieval tuned to your repository**, not a generic search;
* **delivery at the moment it matters**, so the package acts when an agent is about to go
  the wrong way rather than by filling its context up front;
* **the benchmark**, which stays with you.

The numbers on this page belong to the package as a whole. We do not publish
per-component claims, because when we measured components one at a time, several of the
obvious ones turned out to be worth nothing — and those are listed below rather than
quietly included.

→ [What it does, in more detail](docs/WHAT-IT-DOES.md) ·
[Why these numbers can be believed](docs/EVIDENCE.md) ·
[What an engagement looks like](docs/ENGAGEMENT.md)

## Fitting the package to a repository, and knowing when it landed

Installing is not the work; fitting is. And fitting is measured the same way as everything
else — each piece of it against the same package without it. A second study, six codebases
and 212 sessions, measured one piece of the fitting on its own:

| Codebase | effect of that one piece, on top of the rest of the package |
|---|---|
| [jq](jq/) (C, autotools, generated files committed) | **tool calls −36%, established** |
| [Polly](polly/) (C#, a build driven by a PowerShell script) | **cost −20%, tool calls −17%, established** |
| [Phoenix](phoenix/) (Elixir) | the numbers looked good and are **reported unread** — the arm differed from itself by more than the effect |
| [bat](bat/) (Rust), [Hugo](hugo/) (Go), [mitmproxy](mitmproxy/) (Python) | nothing established |

The two that moved are the two whose build and verification are hard to guess. The four
that did not all answer to a command an agent works out by itself. Same pattern as the
headline table, reached from a different direction — and answer completeness improved on
none of the six.

So an engagement opens with a measurement on your repository, not with a quote.

## What we measured and threw away

Published because a vendor who shows only what worked is not telling you how they know:

| what was tried | what happened |
|---|---|
| a ranked list of likely files, pushed into the session | right on half the cases, and **lost 6 tickets of 18 while winning none** — an agent follows a confident wrong answer and does not come back |
| a code index exposed as tools the agent can call | **0 calls in 205 sessions**, measured twice |
| that index attached to every search automatically | fired on 67% of searches; 21% of its answers named the file that needed fixing; no effect on the outcome |
| the same index behind a command named in the agent's own context | **never run in 212 sessions**, even on tasks where the agent used a shell five times |
| a confidence gate, to act only where the index agreed with itself | speaks on 3 cases of 18 and is right on 1 of those 3 — **rejected before it shipped** |
| the largest token reduction we have ever measured, 52% | **retracted as a claim** by our own replicate check, and still printed above |

Six mechanisms, six negatives, one of them ours for a month before the benchmark caught it.
That is why the next section exists.

## The benchmark is part of the deliverable

Every codebase that has been through the second study ships a self-contained kit in its
directory — the cases, the runner, the analysis with its guards, and the audit trail of what
was dropped from its page and why. Python standard library, no dependency on anything of
ours, and it runs against your own checkout: [jq](jq/kit/), [mitmproxy](mitmproxy/kit/),
[Polly](polly/kit/), [Hugo](hugo/kit/), [bat](bat/kit/), [Phoenix](phoenix/kit/).

It carries the guards that our own retracted results paid for:

* **a mechanism is counted by an event it logs itself**, never by its own installation. We
  once read a result out of a context file that was written into 106 sessions and opened by
  one of them;
* **every arm runs twice**, and the difference between an arm and itself is a **veto**: a
  metric where that fires is reported unread, not explained away. That rule is why the 52%
  above is not a claim;
* **ten bootstrap seeds, and both replicate strata**, because two identical arms once
  cleared a single-seed bar;
* **a session that returns one turn and no answer is an error, not a score of zero**,
  because scoring it silently credits the other arm. We found that one in our own control
  arm, where it was making the treatment look free.

Run it on your repository, before and after. If it says *not established*, that is the
honest answer for your codebase and we will tell you so rather than invoice against it.

## The nine codebases

Each page states what was measured there, what was not, and what the engagement left behind.

| | | |
|---|---|---|
| [Rocket.Chat](rocketchat/) · TypeScript | [Keycloak](keycloak/) · Java | [SuiteCRM](suitecrm/) · PHP |
| [mitmproxy](mitmproxy/) · Python | [jq](jq/) · C | [Polly](polly/) · C# |
| [Hugo](hugo/) · Go | [bat](bat/) · Rust | [Phoenix](phoenix/) · Elixir |
