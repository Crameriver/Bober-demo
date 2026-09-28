# Context engineering, measured

Five public codebases. On each, an AI coding agent fixes real defects from that project's own
history — first with nothing, then with an infrastructure built for that codebase. Same tickets,
same model, a fresh checkout every time, and the diff the agent produces compared by script to
the one the maintainers actually wrote.

| Codebase | Language | Source files | Tokens | Turns | Runaway sessions |
|---|---|---|---|---|---|
| [Rocket.Chat](rocketchat/) | TypeScript | 9,179 | **−52%** | −51% | 7 → 2 |
| [SuiteCRM](suitecrm/) | PHP | 4,903 | **−46%** | −43% | 2 → 0 |
| [Keycloak](keycloak/) | Java | 9,561 | **−38%** | −54% | 3 → 3 |
| [mitmproxy](mitmproxy/) | Python | 808 | **−37%** | −37% | 4 → 0 |
| [jq](jq/) | C | 83 | **−12%** | −18% | 0 → 0 |

**Two thirds fewer sessions run away.** Without the infrastructure, sixteen sessions of a hundred
and twelve passed forty tool calls, one of them reaching a hundred and sixty-one. With it, five.
The spread of what a single session costs halves. That is the number to plan a sprint around, and
it is the one nobody else publishes.

**The gain tracks the size and the internal ambiguity of a codebase, not its language.** It runs
from 52% of tokens on a nine-thousand-file monorepo down to 12% on an eighty-three-file project,
where the honest advice is not to buy. That case is in the table rather than left out of it.

**What does not change is whether the answer is right.** Across all five, the infrastructure
placed its fix correctly on 42.5 tickets of 56 against 40.5 without — a difference inside what
the benchmark produces by chance. This work makes an agent faster, cheaper and far more
predictable. It does not make it cleverer, and every page here says so.

## The five studies

Each one carries the measurement for that codebase, the shape of what was delivered, a verbatim
sample of it, and what the study found there.

| | |
|---|---|
| [Rocket.Chat](rocketchat/) | TypeScript · 9 179 files · the largest saving of the five |
| [SuiteCRM](suitecrm/) | PHP · 4 903 files · the one where correctness also rose |
| [Keycloak](keycloak/) | Java · 9 561 files · the most expensive to work in unaided |
| [mitmproxy](mitmproxy/) | Python · 808 files · every wandering session eliminated |
| [jq](jq/) | C · 83 files · too small to be worth it, and published anyway |

## Read next

| | |
|---|---|
| [What the infrastructure does](docs/WHAT-IT-DOES.md) | what an agent gains, and where it gains nothing |
| [Why these numbers can be believed](docs/EVIDENCE.md) | the protocol, the noise floor, and what was thrown away |
| [Working with us](docs/ENGAGEMENT.md) | whether your codebase qualifies, and how an engagement runs |

## The measurement in one paragraph

Fifty-six real tickets, three hundred and thirty-six sessions, every configuration run twice so
the benchmark could measure its own noise before reading a result out of itself. A difference is
claimed only when it exceeds that noise and holds across ten independent resamplings; anything
else is reported as not established, in those words. Five tickets were declared unwinnable before
the data existed and counted in every figure anyway. Nothing is judged by a model.

