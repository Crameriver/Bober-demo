# mitmproxy

**Python · 808 source files · [https://github.com/mitmproxy/mitmproxy](https://github.com/mitmproxy/mitmproxy) · MIT**

9 real defect tickets from this project's own history, each run twice with no
infrastructure and twice with it. 36 sessions.

| Per ticket | no infrastructure | with it | |
|---|---|---|---|
| Tokens per ticket | 738 974 | **464 192** | **−37%** |
| Turns | 27.1 | **17.1** | **−37%** ✓ |
| Tool calls | 29.2 | **19.2** | **−34%** ✓ |
| Cost per ticket | $0.560 | **$0.450** | **−20%** |
| Fix placed on the right file, of 9 | 4.5 | 4.0 | a tie |
| Sessions past 40 tool calls | 4 of 18 | 0 of 18 | |

✓ marks a difference whose 95% interval excludes zero across all ten resamplings. A row
without one moved in the right direction but not far enough to claim, and is printed anyway.

## The deliverable

50 KB of plain text, of which **2.9 KB is resident** — reloaded on every turn of the conversation, and therefore the only part that costs anything while nothing is using it. The rest stays inert until something calls for it.

| File | Size | |
|---|---|---|
| `.claude/agents/blast-radius.md` | 2 496 B | answers what else a change here touches |
| `.claude/agents/reviewer.md` | 2 986 B | a reviewer that knows this project's conventions |
| `.claude/hooks/kit_gates.json` | 15 636 B | the answers this codebase has already taught us, each with the moment it is worth delivering |
| `.claude/hooks/kit_gates.py` | 7 523 B | delivers them, and stays out of the way otherwise |
| `.claude/rules/context.md` | 2 995 B | **resident** — what this codebase's vocabulary hides, and where each kind of task starts. Reloaded every turn, so its size is the one hard budget. |
| `docs/ai/reference.md` | 19 403 B | the long-form reference your engineers read |

### The opening of the resident core

Verbatim — the first 1 077 bytes of 2 995.

```markdown
# mitmproxy
Intercepting HTTP/TLS proxy. Three front-ends over one core: `mitmproxy` (urwid TUI,
`tools/console/`), `mitmdump` (`tools/dump.py`), `mitmweb` (tornado `tools/web/` + React `web/`).
Nearly every feature is an **addon**.

## Commands (uv-managed; bare `pytest` is wrong)
`uv run pytest test/mitmproxy/addons/test_view.py -k name` for one file.
`uv run tox` | `-e lint` | `-e mypy` | `-e filename_matching` | `-e individual_coverage`.
mitmweb client: `cd web && npm test` (also runs tsc).

## Vocabulary traps
| you read | it is |
|---|---|
| `mitmproxy/test/` | shipped test *helpers* (tflow/taddons). The suite is `test/mitmproxy/`. |
| "hook" | an addon callback: `class HttpRequestHook` -> `def http_request(self, flow)`, dispatched by `getattr(addon, hook.name)` in `addonmanager.py`, so grep finds no call site. |
| `proxy/commands.py` | sans-io instructions a layer *yields*. Not `command.py`, the `:` command system of the UIs. |
| `View` | `addons/view.py` = the flow list. Body pretty-printers are `contentviews/` (`Contentview`; `base.View` deprecated). |
```

The rest of this file, the answers that accompany it and the conditions that decide when each one is delivered are the engagement's work and travel with it.

## What made the difference here

A small, disciplined codebase with a layered core whose rules are strict and nowhere written down for a newcomer. The gain is real but smaller, and it arrives mostly as the disappearance of the sessions that wandered: four of twenty-four passed forty tool calls without the infrastructure, none with.

See [why these numbers can be believed](../docs/EVIDENCE.md) for the protocol, and
[working with us](../docs/ENGAGEMENT.md) for what an engagement on your own codebase involves.
