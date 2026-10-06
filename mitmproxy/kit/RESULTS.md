# Results on this repository (Python)

Measured by us: the package without the fact sheet in this kit, against the package with
it. Each arm ran twice, the two runs at opposite ends of the day, on
9 cases.

| | package | package + fact sheet | change |
|---|---|---|---|
| tool calls | 12.83 | 12.28 | -4.3% |
| cost per case | $0.2056 | $0.2017 | -1.9% |
| answer completeness | 0.766 | 0.789 | +0.022 |

**Not established, and the mechanism explains why.** This repository's test command is one an agent guesses on its own, so a sheet that states it adds almost nothing: effort fell 4.3%, the smallest of the six.

## Across all six repositories we measured

Two of six showed an established reduction in effort, and they are exactly the two whose
verification is hard to guess. The four that did not move all answer to a command an agent already
guesses — `uv run pytest`, `cargo test`, `mix test`, `./check.sh`.

**So the rule is: a fact sheet earns its place in inverse proportion to how guessable the
repository is.** That is the single most useful thing we can tell you before you spend
anything, and it is why this kit ships with the instrument rather than only with the sheet.

Answer completeness was not improved on any of the six. The sheet makes the work cheaper
where it works; it does not make the answers better.
