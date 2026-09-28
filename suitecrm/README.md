# SuiteCRM

**PHP · 4,903 source files · [https://github.com/salesagility/SuiteCRM](https://github.com/salesagility/SuiteCRM) · AGPL-3.0**

12 real defect tickets from this project's own history, each run twice with no
infrastructure and twice with it. 48 sessions.

| Per ticket | no infrastructure | with it | |
|---|---|---|---|
| Tokens per ticket | 716 261 | **389 848** | **−46%** ✓ |
| Turns | 23.4 | **13.4** | **−43%** ✓ |
| Tool calls | 25.0 | **18.0** | **−28%** ✓ |
| Cost per ticket | $0.574 | **$0.393** | **−31%** ✓ |
| Fix placed on the right file, of 12 | 6.5 | 8.0 | a tie |
| Sessions past 40 tool calls | 2 of 24 | 0 of 24 | |

✓ marks a difference whose 95% interval excludes zero across all ten resamplings. A row
without one moved in the right direction but not far enough to claim, and is printed anyway.

## The deliverable

52 KB of plain text, of which **2.9 KB is resident** — reloaded on every turn of the conversation, and therefore the only part that costs anything while nothing is using it. The rest stays inert until something calls for it.

| File | Size | |
|---|---|---|
| `.claude/agents/blast-radius.md` | 2 500 B | answers what else a change here touches |
| `.claude/agents/reviewer.md` | 2 996 B | a reviewer that knows this project's conventions |
| `.claude/hooks/kit_gates.json` | 17 516 B | the answers this codebase has already taught us, each with the moment it is worth delivering |
| `.claude/hooks/kit_gates.py` | 7 523 B | delivers them, and stays out of the way otherwise |
| `.claude/rules/context.md` | 2 977 B | **resident** — what this codebase's vocabulary hides, and where each kind of task starts. Reloaded every turn, so its size is the one hard budget. |
| `docs/ai/reference.md` | 19 965 B | the long-form reference your engineers read |

### The opening of the resident core

Verbatim — the first 1 030 bytes of 2 977.

```markdown
# SuiteCRM 7.15.1 — orientation

A fork of SugarCRM CE 6.5 (`sugar_version.json`). PHP 8.1+, 4,305 PHP files, 121 modules.
No `vendor/`, `tests/`, `custom/` or `cache/`: **nothing here runs, installs or tests.**
Verify by reading. Most files open with a ~40-line licence header (code starts 41-60) — skim it,
never seek to a fixed line: 726 PHP files are shorter than the header, and 330 `*defs.php`,
`vardefs.php`, `controller.php`, `view.*.php` files in 57 modules, plus 82 of the 98 files
under `Api/`, hold code above line 41.

## One feature carries four different names
`modules/<Dir>/` → bean class → vardef key → SQL table, and they differ.
`include/modules.php` is the index (`$beanList`, `$beanFiles`, `$objectList`);
`modules/<Dir>/vardefs.php`'s `$dictionary['<Key>']` names the table.
Cases: dir `Cases`, class **`aCase`** (`case` is reserved in PHP), key `Case`, table `cases`.
Resolve the name there FIRST; a grep on the UI word usually returns nothing.

## What the UI calls it → what the code calls it
```

The rest of this file, the answers that accompany it and the conditions that decide when each one is delivered are the engagement's work and travel with it.

## What made the difference here

Screens here are data, not templates, so the file an agent reaches for is usually the wrong one. Four class names are declared twice and the first search result is always the dead copy. A hundred JavaScript files are build output, regenerated over any edit. The one codebase of the five where the correctness count also rose.

See [why these numbers can be believed](../docs/EVIDENCE.md) for the protocol, and
[working with us](../docs/ENGAGEMENT.md) for what an engagement on your own codebase involves.
