# Facts about this repository

## Building and testing
Three Mix projects (root, installer/, integration_test/) plus a jest suite; no one command runs all.
- root suite: `mix test`
- one file: `mix test test/phoenix/router/routing_test.exs`
- one test: append the `test` line — `mix test test/phoenix/router/routing_test.exs:94`
- installer: `cd installer && mix test` · JS: `npm ci && npm test`
- plain `mix test` skips test/mix/tasks/phx.gen.auth_test.exs (the only `@moduletag :mix_phx_new`, excluded in test/test_helper.exs) — use `mix test --only mix_phx_new`

Root tests are `test/**/*_test.exs`, mirroring `lib/` loosely: `lib/phoenix/router.ex` has no `router_test.exs` (test/phoenix/router/*), and controller/endpoint/socket tests sit in a same-named subdirectory. JS tests: assets/test/*_test.js.

CI gates are only warnings-as-errors; no format check and no eslint anywhere.

## Where things live
- lib/phoenix/ — runtime: endpoint, router, controller, socket/channel, transports
- lib/mix/ — the `mix phx.*` tasks and their generator model
- priv/templates/ — EEx sources for `mix phx.gen.*`
- priv/static/ — the built JS bundles (generated) and logos
- assets/ — the JS client (js/phoenix) and its jest suite
- installer/ — the `phx_new` Mix project; integration_test/ — a third, generating apps on real DBs
- guides/ — ex_doc pages, each listed by hand in mix.exs `extras()`

## Changing things together
- Nothing is auto-discovered: a new installer/templates/ file needs a `template(...)` entry in the matching installer/lib/phx_new/ module; a new priv/templates/phx.gen.X file needs one in `files_to_be_generated/1` of lib/mix/tasks/phx.gen.X.ex. Unlisted files are never written.
- A new `mix phx.new` flag must join `@switches` in installer/lib/mix/tasks/phx.new.ex — `OptionParser.parse!(strict: @switches)` makes an undeclared flag fatal.

## Traps
- priv/templates/phx.gen.live/core_components.ex.eex is gitignored and rewritten by every `mix compile` from installer/templates/phx_web/components/ — edit that copy.
- The priv/static/phoenix.js/.min.js/.mjs/.cjs.js bundles are esbuild output auto-committed by .github/workflows/assets.yml — edit assets/js/phoenix/.
