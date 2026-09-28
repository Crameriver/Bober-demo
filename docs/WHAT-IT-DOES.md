# What the infrastructure does

A large codebase carries knowledge that is nowhere in the code: which of two identically named
classes is the live one, which directory is frozen, which change has to be made in two places or
it silently does nothing. A human learns it over months. An agent re-derives it from scratch
every session, and how long that takes is a lottery.

The infrastructure ends the lottery.

```mermaid
flowchart LR
  subgraph B["Without"]
    direction TB
    b1["the agent arrives knowing nothing"] --> b2["it explores"]
    b2 --> b3["it guesses"]
    b3 --> b4["sometimes it guesses well<br/>and answers in four calls"]
    b3 --> b5["sometimes it reads forty files<br/>and edits the wrong one"]
  end
  subgraph A["With"]
    direction TB
    a1["the agent arrives already<br/>holding this codebase's answers"] --> a2["it goes to the right place"]
    a2 --> a3["the spread between a good session<br/>and a bad one collapses"]
  end
  B ==>|"−41% tokens · −43% turns<br/>runaway sessions cut by two thirds"| A
  style A fill:#e6f2ef,stroke:#0f6b5c
```

## What an agent gets that it did not have

**The vocabulary your codebase actually uses.** Every mature system has a gap between the words
on the screen and the words in the source. What Keycloak's interface calls an *identity provider*
its engine calls a `broker`; what its admin screens call *user federation* the code calls
`storage`. An agent that searches the words a human would use finds the administrative surface
and never the machinery. Closing that gap is the single highest-yield thing an engagement does,
and it is entirely specific to one codebase.

**The traps, before they are sprung.** Four class names declared twice, where the first search
result is always the dead one. A directory that looks alive and was frozen two years ago. A
hundred JavaScript files that are build output, silently regenerated over any edit. A change that
must touch two files or it compiles and does nothing.

**The answer at the moment of the question.** When the agent is about to spend calls
rediscovering something this codebase has already taught us, it receives the answer instead. Not
a pointer to where the answer lives — the answer.

**Two specialists that know the house rules.** A reviewer that knows this project's conventions,
and one that answers what else a change touches. Available when wanted, costing nothing when not.

## What that buys, measured

Across 56 real defect tickets on five large codebases, 336 sessions, every configuration run
twice:

```mermaid
flowchart TB
  M1["<b>−41%</b><br/>tokens per ticket<br/>658 000 → 391 000"]
  M2["<b>−43%</b><br/>turns of conversation<br/>24.6 → 14.1"]
  M3["<b>16 → 5</b><br/>sessions of 112 that<br/>pass 40 tool calls"]
  M4["<b>$0.51 → $0.28</b><br/>spread of what one<br/>session costs"]
  M1 --- M2
  M3 --- M4
  style M1 fill:#e6f2ef,stroke:#0f6b5c
  style M3 fill:#e6f2ef,stroke:#0f6b5c
```

The averages are the smaller half. **The spread halves, and the sessions that run away mostly
stop happening** — one in seven becomes one in twenty-two. What a team buys is not a discount on
tokens. It is the disappearance of the afternoon where the agent read forty files and changed the
wrong one, and the ability to tell a product owner how long something will take.

## Where the gain comes from

Not from making the agent search less. From removing the ambiguity it would otherwise have to
resolve by searching.

```mermaid
flowchart LR
  subgraph W["the work that disappears"]
    direction TB
    w1["whole files read to find out<br/>what they are<br/><b>4.18 → 2.54</b>"]
    w2["searches that return nothing<br/><b>2.84 → 1.79</b>"]
    w3["shell commands spent orienting<br/><b>3.71 → 1.31</b>"]
  end
  W --> R["every one of those was the agent<br/>asking the codebase a question<br/>the infrastructure had already answered"]
  style R fill:#e9eef2,stroke:#17415c
```

## Where it does not help

**Correctness does not move.** Across the five codebases the infrastructure placed its fix
correctly on 42.5 tickets of 56 against 40.5 without — a difference inside what the benchmark
produces by chance. This is not a product that makes an agent smarter. It makes it faster,
cheaper and far more predictable at the thing it was already doing.

**Small codebases do not need it.** On an eighty-three-file C project the agent finds its own way
and the gain falls to 12%. Below roughly five hundred source files we will tell you not to buy.

That second sentence is in this document deliberately. A claim about where something works is
worth exactly as much as the willingness to name where it does not.
