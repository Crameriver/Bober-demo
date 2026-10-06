# Results on this repository (C)

Measured by us: the package without the fact sheet in this kit, against the package with
it. Each arm ran twice, the two runs at opposite ends of the day, on
10 cases.

| | package | package + fact sheet | change |
|---|---|---|---|
| tool calls | 15.75 | 10.15 | -35.6% |
| cost per case | $0.2229 | $0.1858 | -16.6% |
| answer completeness | 0.633 | 0.680 | +0.047 |

**Established.** Tool calls fell 35.6% and turns fell, both across ten bootstrap seeds and in both replicate strata. Cost fell 16.6% but did not reach the bar. Answer completeness did not move.

## Across all six repositories we measured

Two of six showed an established reduction in effort, and they are exactly the two whose
verification is hard to guess. The four that did not move all answer to a command an agent already
guesses — `uv run pytest`, `cargo test`, `mix test`, `./check.sh`.

**So the rule is: a fact sheet earns its place in inverse proportion to how guessable the
repository is.** That is the single most useful thing we can tell you before you spend
anything, and it is why this kit ships with the instrument rather than only with the sheet.

Answer completeness was not improved on any of the six. The sheet makes the work cheaper
where it works; it does not make the answers better.
