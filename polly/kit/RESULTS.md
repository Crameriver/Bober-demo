# Results on this repository (C#)

Measured by us: the package without the fact sheet in this kit, against the package with
it. Each arm ran twice, the two runs at opposite ends of the day, on
10 cases.

| | package | package + fact sheet | change |
|---|---|---|---|
| tool calls | 15.15 | 12.65 | -16.5% |
| cost per case | $0.2170 | $0.1730 | -20.3% |
| answer completeness | 0.594 | 0.509 | -0.084 |

**Established.** Cost fell 20.3% and tool calls fell 16.5%, both across ten seeds and in both strata. Answer completeness moved the WRONG way by a margin that only held in one stratum, so it is reported and not claimed.

## Across all six repositories we measured

Two of six showed an established reduction in effort, and they are exactly the two whose
verification is hard to guess. The four that did not move all answer to a command an agent already
guesses — `uv run pytest`, `cargo test`, `mix test`, `./check.sh`.

**So the rule is: a fact sheet earns its place in inverse proportion to how guessable the
repository is.** That is the single most useful thing we can tell you before you spend
anything, and it is why this kit ships with the instrument rather than only with the sheet.

Answer completeness was not improved on any of the six. The sheet makes the work cheaper
where it works; it does not make the answers better.
