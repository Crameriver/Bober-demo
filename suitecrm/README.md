# SuiteCRM

**PHP · 4,797 source files · 914,599 lines · [https://github.com/salesagility/SuiteCRM](https://github.com/salesagility/SuiteCRM) · AGPL-3.0**

A long-lived PHP application where the same concept appears as a module, a
bean, a metadata array and a database table, and where the file you want is often not the file
the name suggests. The clearest result of the five: tokens, cost and model turns all fell and
all held up, on twelve tickets. It is also the codebase where answer quality moved up rather
than sideways, by a margin too small to claim.

## What was measured here

12 real defect tickets from this project's own history. Each ticket was run twice with
nothing installed and twice with the package installed, in runs placed at opposite ends of the
day: 48 agent sessions. The agent's patch is compared by script against the one the
maintainers actually wrote.

| Per ticket | without | with the package | |
|---|---|---|---|
| Tokens | 716,261 | **389,848** | **−45.6%** ✓ |
| Cost | $0.574 | **$0.393** | **−31.5%** ✓ |
| Model turns | 23.4 | **13.4** | **−42.8%** ✓ |
| Tool calls | 25.0 | **18.0** | **−28.2%** |
| Fix landed on the right file, of 12 | 6.5 | 8.0 | up, too small to claim |
| Sessions past 40 tool calls | 2 of 24 | 0 of 24 | |

✓ marks a difference that held on all ten resamplings and in both replicates. A row without
one moved but did not clear that bar, and is printed anyway.

## Estimate it for a repository this size

```
python ../tools/estimate.py --files 4797 --loc 914599
```

---

[Why these numbers can be believed](../docs/EVIDENCE.md) ·
[What gets installed](../docs/WHAT-IT-DOES.md) ·
[What an engagement looks like](../docs/ENGAGEMENT.md) ·
[Estimate your own repository](../docs/ESTIMATE.md)
