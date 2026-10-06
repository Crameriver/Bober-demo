# Results on this repository (Rust)

Measured by us: the package without the fact sheet in this kit, against the package with
it. Each arm ran twice, the two runs at opposite ends of the day, on
8 cases.

| | package | package + fact sheet | change |
|---|---|---|---|
| tool calls | 14.62 | 12.25 | -16.2% |
| cost per case | $0.2260 | $0.2105 | -6.9% |
| answer completeness | 0.509 | 0.530 | +0.020 |

**Not established.** Effort fell directionally and nothing cleared the bar. The arm also differed from itself on answer completeness, so that metric is unread.

## Across all six repositories we measured

Two of six showed an established reduction in effort, and they are exactly the two whose
verification is hard to guess. The four that did not move all answer to a command an agent already
guesses — `uv run pytest`, `cargo test`, `mix test`, `./check.sh`.

**So the rule is: a fact sheet earns its place in inverse proportion to how guessable the
repository is.** That is the single most useful thing we can tell you before you spend
anything, and it is why this kit ships with the instrument rather than only with the sheet.

Answer completeness was not improved on any of the six. The sheet makes the work cheaper
where it works; it does not make the answers better.
