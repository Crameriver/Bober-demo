# Keycloak

**Java · 6,326 source files · 764,287 lines · [https://github.com/keycloak/keycloak](https://github.com/keycloak/keycloak) · Apache-2.0**

A large Java product with a conventional build and an unconventional amount
of indirection: service provider interfaces, generated code, and several modules whose names
differ from the concepts they implement. Model turns fell by more than half and held up under
every check. Tokens fell 38% and did not clear the bar on eleven tickets — a real effect this
many cases cannot resolve, printed as such.

## What was measured here

11 real defect tickets from this project's own history. Each ticket was run twice with
nothing installed and twice with the package installed, in runs placed at opposite ends of the
day: 44 agent sessions. The agent's patch is compared by script against the one the
maintainers actually wrote.

| Per ticket | without | with the package | |
|---|---|---|---|
| Tokens | 631,468 | **393,966** | **−37.6%** |
| Cost | $0.731 | **$0.454** | **−37.9%** |
| Model turns | 28.0 | **12.9** | **−54.0%** ✓ |
| Tool calls | 29.3 | **22.2** | **−24.3%** |
| Fix landed on the right file, of 11 | 7.5 | 8.5 | up, too small to claim |
| Sessions past 40 tool calls | 3 of 22 | 3 of 22 | |

✓ marks a difference that held on all ten resamplings and in both replicates. A row without
one moved but did not clear that bar, and is printed anyway.

## Why there is no benchmark kit here

Six of the nine codebases in this repository ship one. This is not one of them: the second
study was not run on this codebase, and we do not hand over an instrument we have not run
against it ourselves. What is published above is the first study, which is the measurement
that matters most — the package against nothing at all.

An engagement builds the kit for your repository, from your own history, and you keep it.
See [what an engagement leaves behind](../docs/ENGAGEMENT.md).

## Estimate it for a repository this size

```
python ../tools/estimate.py --files 6326 --loc 764287
```

---

[Why these numbers can be believed](../docs/EVIDENCE.md) ·
[What gets installed](../docs/WHAT-IT-DOES.md) ·
[What an engagement looks like](../docs/ENGAGEMENT.md) ·
[Estimate your own repository](../docs/ESTIMATE.md)
