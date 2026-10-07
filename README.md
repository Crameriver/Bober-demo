# Your AI coding agent, cheaper and predictable on your own codebase

We come in, set up a context infrastructure inside your repository, tune it to that repository,
and then measure what it changed — on tickets from your own history, against the same agent
working without us. Nine public codebases are worked through here so you can see the work before
you buy it.

**Across 56 tickets on five codebases, 224 agent sessions: 40% fewer tokens, 30% lower cost per
ticket, 43% fewer model turns, and two thirds fewer sessions that run away.**

| Over all 56 tickets | without us | with us | |
|---|---|---|---|
| Tokens per ticket | 658,137 | **391,356** | **−40.5%** |
| Cost per ticket | $0.57 | **$0.40** | **−30.0%** |
| Model turns | 24.6 | **14.1** | **−42.9%** |
| Tool calls | 26.1 | **19.1** | −26.7% |
| Sessions past 40 tool calls | 16 of 112 | **5 of 112** | |

Every figure in the first three rows clears a deliberately hard bar: the 95% interval excludes
zero on all ten resamplings **and** in each of two independent replicates. We do not quote a
number that has not.

## The runaway session is the number to budget around

Working without us, sixteen sessions of a hundred and twelve went past forty tool calls, one of
them reaching a hundred and sixty-one. With us, five. The cost saving is the average; this is the
variance — and it is what turns an agent from something you hope goes well into something you can
put in a sprint plan.

## How much it returns depends on your codebase, not your language

| Codebase | Language | Source files | Lines of code | Tokens per ticket |
|---|---|---|---|---|
| [Rocket.Chat](rocketchat/) | TypeScript | 7,454 | 503,665 | **−52%** |
| [SuiteCRM](suitecrm/) | PHP | 4,797 | 914,599 | **−46%** |
| [Keycloak](keycloak/) | Java | 6,326 | 764,287 | **−38%** |
| [mitmproxy](mitmproxy/) | Python | 472 | 68,824 | **−37%** |
| [jq](jq/) | C | 48 | 26,655 | −12% |

The table above is the headline figure broken down; what we stand behind as established is the
pooled result across all 56 tickets, and each codebase page shows exactly which of its own rows
cleared the bar.

**The pattern that holds: what we return scales with how much a newcomer has to rule out before
they can start.** A large product where one feature wears two names returns a lot. A tidy
eighty-file utility returns little — and on that one, [our advice was not to buy](jq/). You will
get the same answer about your own codebase before you spend anything with us.

## What will it save on your codebase? Find out in one command

```
python tools/estimate.py --scan /path/to/your/checkout
```

That prints the percentage of tokens you can expect to save, as a range, in about a minute. If
you would rather not point it at code, give it two numbers instead — and add your monthly agent
spend to see the saving in your own currency:

```
python tools/estimate.py --files 4200 --loc 610000 --monthly-spend 9000
```

```
  ESTIMATED TOKEN REDUCTION PER TICKET

      33% to 55%        central estimate 44%

  at 9,000 a month in agent spend, that is 2,970 to 4,950 a month back,
  or 3,960 at the central estimate.
```

Standard-library Python, no install, no network, and with `--scan` it reads file names and counts
lines — never the contents of your code. Run it on a private repository during a call if you like.

→ [How to read the estimate](docs/ESTIMATE.md)

## What we set up, and what we tune

One infrastructure, installed in your repository and then fitted to it:

* **a context engine** that decides what your agent is told, and when;
* **an index of your code**, built over your repository and kept current;
* **project memory**, so what the team has established carries from one session to the next
  instead of being rediscovered;
* **retrieval tuned to your repository** — your vocabulary, your conventions, your false friends;
* **delivery at the moment it matters**, so we act when an agent is about to go the wrong way
  rather than by filling its context up front;
* **the measurement**, which we run before and after, and keep running.

Setting it up is an afternoon. **Tuning it is the work**, and it is measured the same way as
everything else. Across nine codebases and 344 sessions, one component of that tuning on its own
cut **tool calls by 10.6% and cost by 8.9%**, both established — on top of everything else
already in place. On [jq](jq/) that component alone cut tool calls by 36%, and on
[Polly](polly/) it cut cost by 20%.

→ [What we set up, in more detail](docs/WHAT-IT-DOES.md) ·
[How we measure](docs/EVIDENCE.md) ·
[How an engagement runs](docs/ENGAGEMENT.md)

## The measurement is a service, not a hand-off

Most vendors give you a configuration and an invoice. We give you a number, and then we give you
the means to keep producing it.

Every codebase here that we tuned ships the instrument we used on it — the cases drawn from that
project's history, the runner, the analysis, and the record of what we kept and what we discarded
while tuning: [jq](jq/kit/), [mitmproxy](mitmproxy/kit/), [Polly](polly/kit/), [Hugo](hugo/kit/),
[bat](bat/kit/), [Phoenix](phoenix/kit/), [Rocket.Chat](rocketchat/kit/),
[SuiteCRM](suitecrm/kit/), [Keycloak](keycloak/kit/). Standard-library Python, no dependency on
anything of ours, and it runs against your own checkout.

That matters for three practical reasons:

* **you can re-run the number yourself**, before and after, without us in the room;
* **it does not go stale.** When your repository moves or your model changes, you measure again;
* **it is how we stay accountable.** We quote what the instrument says, and you own the
  instrument.

## The nine codebases

Each page shows what we measured there, how, and what we left behind.

| | | |
|---|---|---|
| [Rocket.Chat](rocketchat/) · TypeScript | [Keycloak](keycloak/) · Java | [SuiteCRM](suitecrm/) · PHP |
| [mitmproxy](mitmproxy/) · Python | [jq](jq/) · C | [Polly](polly/) · C# |
| [Hugo](hugo/) · Go | [bat](bat/) · Rust | [Phoenix](phoenix/) · Elixir |
