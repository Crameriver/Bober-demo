# Results on this repository (Go)

Measured by us: the package without the fact sheet in this kit, against the package with
it. Each arm ran twice, the two runs at opposite ends of the day, on
8 cases.

| | package | package + fact sheet | change |
|---|---|---|---|
| tool calls | 13.56 | 11.50 | -15.2% |
| cost per case | $0.2245 | $0.2056 | -8.4% |
| answer completeness | 0.504 | 0.516 | +0.012 |

**Not established.** Everything directional, nothing clearing the bar.

## Across all six repositories we measured

Two of six showed an established reduction in effort, and they are exactly the two whose
verification is hard to guess. The four that did not move all answer to a command an agent already
guesses — `uv run pytest`, `cargo test`, `mix test`, `./check.sh`.

**So the rule is: a fact sheet earns its place in inverse proportion to how guessable the
repository is.** That is the single most useful thing we can tell you before you spend
anything, and it is why this kit ships with the instrument rather than only with the sheet.

Answer completeness was not improved on any of the six. The sheet makes the work cheaper
where it works; it does not make the answers better.
