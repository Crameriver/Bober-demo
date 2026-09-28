# Rocket.Chat

**TypeScript · 9,179 source files · [https://github.com/RocketChat/Rocket.Chat](https://github.com/RocketChat/Rocket.Chat) · MIT**

12 real defect tickets from this project's own history, each run twice with no
infrastructure and twice with it. 48 sessions.

| Per ticket | no infrastructure | with it | |
|---|---|---|---|
| Tokens per ticket | 873 703 | **419 059** | **−52%** ✓ |
| Turns | 29.8 | **14.6** | **−51%** ✓ |
| Tool calls | 30.5 | **20.7** | **−32%** ✓ |
| Cost per ticket | $0.631 | **$0.403** | **−36%** ✓ |
| Fix placed on the right file, of 12 | 11.5 | 11.0 | a tie |
| Sessions past 40 tool calls | 7 of 24 | 2 of 24 | |

✓ marks a difference whose 95% interval excludes zero across all ten resamplings. A row
without one moved in the right direction but not far enough to claim, and is printed anyway.

## The deliverable

47 KB of plain text, of which **2.9 KB is resident** — reloaded on every turn of the conversation, and therefore the only part that costs anything while nothing is using it. The rest stays inert until something calls for it.

| File | Size | |
|---|---|---|
| `.claude/agents/blast-radius.md` | 2 499 B | answers what else a change here touches |
| `.claude/agents/reviewer.md` | 2 994 B | a reviewer that knows this project's conventions |
| `.claude/hooks/kit_gates.json` | 14 202 B | the answers this codebase has already taught us, each with the moment it is worth delivering |
| `.claude/hooks/kit_gates.py` | 7 523 B | delivers them, and stays out of the way otherwise |
| `.claude/rules/context.md` | 2 985 B | **resident** — what this codebase's vocabulary hides, and where each kind of task starts. Reloaded every turn, so its size is the one hard budget. |
| `docs/ai/reference.md` | 17 841 B | the long-form reference your engineers read |

### The opening of the resident core

Verbatim — the first 1 076 bytes of 2 985.

```markdown
# Rocket.Chat — orientation

Monorepo: `apps/meteor/` = the app (`server/`, `client/`, `ee/`, frozen `app/`);
`packages/*` = `@rocket.chat/*`; `ee/*` = EE. Server files sort
**responsibility, then domain**: `server/{api,services,lib,hooks,settings}/<domain>/`.

## Names that mislead

| Looks like | Actually |
|---|---|
| Livechat vs Omnichannel | one feature. Engine `server/lib/omnichannel/`; models/REST/types say `Livechat*`. `packages/livechat` = the embedded **widget**. |
| channel / group / DM | one `IRoom.t`: `c` public, `p` private ("group"), `d` direct, `l` omnichannel. REST: `channels.*`=c, `groups.*`=p, `im.*`+`dm.*`=d. |
| `Rooms` vs `LivechatRooms` | one `rocketchat_room` collection; the second is the `t:'l'` view. |
| `room.unread` / `alert` / `favorite` | on `IRoom` but written nowhere; per-user truth is `ISubscription` (`unread` required, plus `f`, `tunread`, room roles, `*Notifications`). |
| Team / Discussion / Thread | Team = room `teamMain:true` + `rocketchat_team` doc; Discussion = room with `prid`; Thread = `tmid` messages, **no room**. |
```

The rest of this file, the answers that accompany it and the conditions that decide when each one is delivered are the engagement's work and travel with it.

## What made the difference here

One feature carries two names across a monorepo, and a second tree inside it holds components with the same names as the main application — so a plausible-looking edit can land in an embedded widget nobody was asking about. A frozen legacy tree still looks alive. The largest saving of the five, on the codebase with the most internal ambiguity.

See [why these numbers can be believed](../docs/EVIDENCE.md) for the protocol, and
[working with us](../docs/ENGAGEMENT.md) for what an engagement on your own codebase involves.
