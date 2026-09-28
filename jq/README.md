# jq

**C · 83 source files · [https://github.com/jqlang/jq](https://github.com/jqlang/jq) · MIT**

12 real defect tickets from this project's own history, each run twice with no
infrastructure and twice with it. 48 sessions.

| Per ticket | no infrastructure | with it | |
|---|---|---|---|
| Tokens per ticket | 348 264 | **308 143** | **−12%** |
| Turns | 15.9 | **13.1** | **−18%** ✓ |
| Tool calls | 17.5 | **15.9** | **−10%** |
| Cost per ticket | $0.366 | **$0.312** | **−15%** |
| Fix placed on the right file, of 12 | 10.5 | 11.0 | a tie |
| Sessions past 40 tool calls | 0 of 24 | 0 of 24 | |

✓ marks a difference whose 95% interval excludes zero across all ten resamplings. A row
without one moved in the right direction but not far enough to claim, and is printed anyway.

## The deliverable

49 KB of plain text, of which **2.9 KB is resident** — reloaded on every turn of the conversation, and therefore the only part that costs anything while nothing is using it. The rest stays inert until something calls for it.

| File | Size | |
|---|---|---|
| `.claude/agents/blast-radius.md` | 2 496 B | answers what else a change here touches |
| `.claude/agents/reviewer.md` | 2 997 B | a reviewer that knows this project's conventions |
| `.claude/hooks/kit_gates.json` | 14 976 B | the answers this codebase has already taught us, each with the moment it is worth delivering |
| `.claude/hooks/kit_gates.py` | 7 523 B | delivers them, and stays out of the way otherwise |
| `.claude/rules/context.md` | 2 986 B | **resident** — what this codebase's vocabulary hides, and where each kind of task starts. Reloaded every turn, so its size is the one hard budget. |
| `docs/ai/reference.md` | 19 388 B | the long-form reference your engineers read |

### The opening of the resident core

Verbatim — the first 1 089 bytes of 2 986.

```markdown
# jq — orientation

C, ~27k lines in `src/`: `main.c` (CLI) -> `parser.y`+`lexer.l` (jq language) -> `compile.c`
(IR) -> `execute.c` (`jq_next`, the VM) -> `jv*.c` (values). `jv_parse.c` parses JSON **input**,
`parser.y` parses jq **programs** — different parsers.

## Misleading names

| looks like | actually |
|---|---|
| "filter" = select/where | ANY jq program or expression. The predicate one is `select(f)`. |
| `block` = braces | compiler IR: a list of `inst`, built by the `gen_*()` in `compile.c`. |
| `jv_invalid()` | **end of output**; an *error* is `jv_invalid_with_msg()`. Same kind, so test `jv_invalid_has_msg`. |

## Always true

- **Never search `src/` bare.** 239 KB of committed bison/flex output swamps every hit, so
  always exclude it: Grep tool glob `!{parser,lexer}.[ch]`, shell `grep -rn X src
  --exclude=parser.[ch] --exclude=lexer.[ch]`. A hit in them is never where you edit — the
  source is `parser.y`/`lexer.l`. Exclude `src/jv_dtoa.c` and `vendor/` too.
- **Also generated, never hand-edit**: `jq.1.prebuilt`, `tests/man.test`, `tests/manonig.test`,
```

The rest of this file, the answers that accompany it and the conditions that decide when each one is delivered are the engagement's work and travel with it.

## What made the difference here

Eighty-three source files. An agent finds its own way, and the honest result is a gain too small to justify the work. It is published here rather than left out of the table, because a claim about where something helps is worth what the claim about where it does not is worth.

See [why these numbers can be believed](../docs/EVIDENCE.md) for the protocol, and
[working with us](../docs/ENGAGEMENT.md) for what an engagement on your own codebase involves.
