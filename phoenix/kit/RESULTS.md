# Results on this repository (Elixir)

Measured by us: the package without the fact sheet in this kit, against the package with
it. Each arm ran twice, the two runs at opposite ends of the day, on
8 cases.

| | package | package + fact sheet | change |
|---|---|---|---|
| tool calls | 13.75 | 12.25 | -10.9% |
| cost per case | $0.2445 | $0.1959 | -19.9% |
| answer completeness | 0.459 | 0.546 | +0.088 |

**Unread.** The numbers look good — cost down 19.9% — but the arm differed from ITSELF on cost, calls and turns when its two replicates were compared. When the instrument is noisier than the effect, the honest report is that this day could not tell, so nothing is claimed.

## Across all six repositories we measured

Two of six showed an established reduction in effort, and they are exactly the two whose
verification is hard to guess. The four that did not move all answer to a command an agent already
guesses — `uv run pytest`, `cargo test`, `mix test`, `./check.sh`.

**So the rule is: a fact sheet earns its place in inverse proportion to how guessable the
repository is.** That is the single most useful thing we can tell you before you spend
anything, and it is why this kit ships with the instrument rather than only with the sheet.

Answer completeness was not improved on any of the six. The sheet makes the work cheaper
where it works; it does not make the answers better.
