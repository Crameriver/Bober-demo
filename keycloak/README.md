# Keycloak

**Java · 9,561 source files · [https://github.com/keycloak/keycloak](https://github.com/keycloak/keycloak) · Apache-2.0**

11 real defect tickets from this project's own history, each run twice with no
infrastructure and twice with it. 44 sessions.

| Per ticket | no infrastructure | with it | |
|---|---|---|---|
| Tokens per ticket | 631 468 | **393 966** | **−38%** |
| Turns | 28.0 | **12.9** | **−54%** ✓ |
| Tool calls | 29.3 | **22.2** | **−24%** ✓ |
| Cost per ticket | $0.731 | **$0.454** | **−38%** ✓ |
| Fix placed on the right file, of 11 | 7.5 | 8.5 | a tie |
| Sessions past 40 tool calls | 3 of 22 | 3 of 22 | |

✓ marks a difference whose 95% interval excludes zero across all ten resamplings. A row
without one moved in the right direction but not far enough to claim, and is printed anyway.

## The deliverable

49 KB of plain text, of which **2.9 KB is resident** — reloaded on every turn of the conversation, and therefore the only part that costs anything while nothing is using it. The rest stays inert until something calls for it.

| File | Size | |
|---|---|---|
| `.claude/agents/blast-radius.md` | 2 498 B | answers what else a change here touches |
| `.claude/agents/reviewer.md` | 2 996 B | a reviewer that knows this project's conventions |
| `.claude/hooks/kit_gates.json` | 12 521 B | the answers this codebase has already taught us, each with the moment it is worth delivering |
| `.claude/hooks/kit_gates.py` | 7 523 B | delivers them, and stays out of the way otherwise |
| `.claude/rules/context.md` | 2 998 B | **resident** — what this codebase's vocabulary hides, and where each kind of task starts. Reloaded every turn, so its size is the one hard budget. |
| `docs/ai/reference.md` | 21 738 B | the long-form reference your engineers read |

### The opening of the resident core

Verbatim — the first 966 bytes of 2 998.

```markdown
# Keycloak (IAM server) — orientation

Maven multi-module Java (release 17) + React UIs in `js/`. `services/` = logic,
`server-spi[-private]/` = interfaces, `model/` = persistence, `quarkus/` = runtime.
`999.0.0-SNAPSHOT` in poms is a placeholder, not a release.
Cold detail: `docs/ai/reference.md`, numbered; `§n` = open that section, not the file.

## The user's word vs the code's

| You would search for | The code calls it | Lives in |
|---|---|---|
| identity provider, SAML/OIDC login, social | **broker** | `services/.../broker/`, `.../social/`; brokered login enters at `services/.../resources/IdentityBrokerService` (§3) |
| user federation, LDAP | **storage** | SPI `model/storage/.../UserStorageProvider` (**not** `server-spi`: capability mixins only); impls `federation/` |
| application | **client** | `ClientModel` |
| config of an LDAP / key / mapper provider instance | **ComponentModel**, one generic row for all | `server-spi/.../component/` |
```

The rest of this file, the answers that accompany it and the conditions that decide when each one is delivered are the engagement's work and travel with it.

## What made the difference here

Its vocabulary misleads in both directions. What the interface calls an identity provider the engine calls something else entirely, and what the admin screens call user federation is a third word in the source — so an agent searching the words a human would use lands on the administrative surface and never the machinery. Several central class names are also declared twice, one copy shadowing the other, and a change made in the obvious one compiles and does nothing. This was the most expensive codebase of the five to work in unaided, and the one where the infrastructure returned the most per ticket.

See [why these numbers can be believed](../docs/EVIDENCE.md) for the protocol, and
[working with us](../docs/ENGAGEMENT.md) for what an engagement on your own codebase involves.
