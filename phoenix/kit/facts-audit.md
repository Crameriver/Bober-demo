# How this fact sheet was built, and what was thrown away

The sheet beside this file is short on purpose. It was produced in three passes: one
pass read the repository and wrote down everything it believed; a second pass
attacked every claim; a third kept only what it could re-verify itself, and dropped
every count and line number because those proved unreliable.

**17 facts kept, 17 dropped.** That ratio is the useful part of
this page: facts about a repository that cannot go stale are harder to produce than
they look, and a sheet that is 40% wrong is worse than no sheet, because an agent
follows it.

## Kept — each one re-verified, with the check used

- Three Mix projects, root + installer/ + integration_test/, each its own project: `ls`; `sed -n '1,80p' mix.exs` (app: :phoenix, elixir ~> 1.15); `sed -n '1,32p' installer/mix.exs` (app: :phx_new, ~> 1.18); `grep -n 'elixir:' integration_test/mix.exs` (line 13)
- Root suite command `mix test`: `sed -n '160,180p' CONTRIBUTING.md` (fenced `mix test`) and `grep -n 'run:' .github/workflows/ci.yml` -> line 67 `run: mix test`
- One-file invocation `mix test <path>`: `sed -n '190,215p' guides/testing/testing.md` documents `mix test <file>` and `<file>:<line>`; path substituted with one that exists here, `ls test/phoenix/router/` shows routing_test.exs
- One-test line number 94: `grep -n '^  test ' test/phoenix/router/routing_test.exs` -> first match `94:  test "get root path" do`
- Installer suite runs inside installer/: `grep -n 'working-directory:' .github/workflows/ci.yml` -> 117/121 `working-directory: installer` around `run: mix test` at 120
- JS suite `npm ci && npm test`: ci.yml lines 163 and 166; `cat package.json` scripts.test = node --experimental-vm-modules ./node_modules/jest/bin/jest.js
- mix_phx_new exclusion: `grep -rn 'mix_phx_new' test/` -> exactly test/mix/tasks/phx.gen.auth_test.exs:6 `@moduletag :mix_phx_new` and test/test_helper.exs:28 `excludes = [:mix_phx_new]`; `cat test/test_helper.exs` shows ExUnit.start(exclude: excludes); escape hatch `mix test --only mix_phx_new` at ci.yml:127
- Root tests are test/**/*_test.exs and the lib/ mirror is loose: `find test -name 'router_test.exs'` returns nothing; `ls test/phoenix/router/` shows 10 split files; `ls test/phoenix/controller test/phoenix/endpoint test/phoenix/socket` shows controller_test.exs / endpoint_test.exs / socket_test.exs in same-named subdirectories
- JS tests are assets/test/*_test.js: `cat jest.config.js` testRegex "/assets/test/.*_test\\.js$"; `ls assets/test`
- Only gates are warnings-as-errors, no format check, no eslint: `grep -n 'run:' .github/workflows/ci.yml` (63 compile, 71 test, 223 docs, all --warnings-as-errors) and `grep -rn 'mix format|eslint|lint' .github/workflows/` -> only two step *names* containing "lint", no invocation
- Module map: `ls` at root, `ls lib lib/phoenix config usage-rules assets priv`, `ls priv/static` (phoenix.js/.min.js/.mjs/.cjs.js + logos), `ls installer/test assets/test integration_test/test`
- guides/ pages are enumerated by hand: `sed -n '165,180p' mix.exs` shows `defp extras do` returning a literal list of "guides/..." strings; `grep -n 'wildcard' mix.exs` returns nothing
- Installer template registration: `sed -n '20,62p' installer/lib/phx_new/generator.ex` — `__before_compile__` emits a `render/3` clause only for sources listed in @templates and `template_files(name), do: Keyword.fetch!(@templates, name)`; `grep -n 'defmacro template' installer/lib/phx_new/generator.ex` (line 63) and `grep -n '^  template(' installer/lib/phx_new/single.ex`
- priv/templates registration: `grep -n 'files_to_be_generated' lib/mix/tasks/phx.gen.html.ex` (def at 191) + `sed -n '196,218p' lib/mix/tasks/phx.gen.html.ex` — the explicit {:eex, source, target} list is handed to `Mix.Phoenix.copy_from` at 216, which `sed -n '25,45p' lib/mix/phoenix.ex` shows iterating only that mapping
- phx.new flag must be declared: `grep -n '@switches|OptionParser.parse' installer/lib/mix/tasks/phx.new.ex` -> @switches at 155, `OptionParser.parse!(argv, strict: @switches)` at 193 and 249 (strict => undeclared flag raises)
- core_components trap: `cat .gitignore` last line ignores /priv/templates/phx.gen.live/core_components.ex.eex; `grep -n 'compile:|copy_core_components' mix.exs` -> `compile: [&copy_core_components/1, "compile"]` (282) and `sed -n '298,310p' mix.exs` shows File.cp! from installer/templates/phx_web/components/core_components.ex.eex
- priv/static bundles auto-committed: `grep -n 'run:|uses:|file_pattern' .github/workflows/assets.yml` -> `mix assets.build` (65) then git-auto-commit-action with `file_pattern: priv/static` (72); `grep -n 'assets.build' mix.exs` -> esbuild alias at 278

## Dropped — and why

- Telemetry-event registration point ("also update the lib/phoenix/logger.ex catalogue") — REFUTED: controller.render is emitted at controller.ex:1001/1009 but documented nowhere, and the moduledoc lists 11 names not 9, so the catalogue is not authoritative
- "9 documented telemetry names match 9 emitted names" — REFUTED by the verifier's grep
- Endpoint-config-key registration point (endpoint.ex + supervisor.ex defaults/2 + config.ex) — proof commit 3087baac does not touch endpoint.ex and adds no config key; rule 4 (all commits, not a sample) not satisfiable
- CRUD-generator option registration point — REFUTED: proof commit fd31ace4 does not touch phx.gen.context.ex, and the supporting grep claim (only 3 files define @switches) is false (7 files)
- single <-> umbrella installer-template pairing — co-change numbers do not reproduce (98 vs 109) and "highest pair in the repo" is false; rule 4 cannot be met from mining alone
- Socket-serializer vsn registration point and the JS/Elixir "both transports" rule — commit-mined, confirmed only on a 2-commit sample; not re-checked across all commits
- Release/version-bump file set (mix.exs, installer/mix.exs, package.json, lockfile, CHANGELOG) — commit-mined only; the sheet itself had to overrule RELEASE.md
- Transport line numbers websocket.ex:29 / long_poll.ex:20 — REFUTED (26 and 15)
- guides/testing/testing.md:196/210 example paths — REFUTED: they are generated-app paths (test/hello_web/...), and the substituted `routing_test.exs:11` is a blank line; replaced with the verified line 94
- "7 *_test.js in assets/test" — REFUTED: 6 (`find assets -name '*_test.js' | wc -l` = 6)
- "23 run: lines" and all co-change counts / 7654-commit figure / proof-commit shas — numbers not reproduced, dropped per rule 3
- "package.json test is a bare jest invocation" and `npm test -- <path>` for one JS file — the script is node --experimental-vm-modules ...; no node_modules present, so I could not run the per-file form and would not ship it unverified
- Doubled-test-name rule (controller/endpoint/socket pattern stated as a rule) — REFUTED by 6 counterexamples; restated as "the mirror is loose, locate the file"
- "test/support and test/fixtures are excluded from discovery by test_ignore_filters" — the causal mechanism is unverifiable (the option only governs Mix's warning); only the option's presence is checkable
- All Path C answer keys and the later registration points — absent/truncated in the delivered draft, so unverified
- Elixir-floor checklist in installer/mix.exs, websocket:/longpoll: key whitelist (Keyword.validate! at endpoint.ex:804), .formatter.exs locals_without_parens export, "16 files under test/ require_file installer/test/mix_helper.exs", mix.exs:60 elixirc_paths — all re-verified true, but cut to fit the 2200-character budget in favour of the invocation facts
- integration_test conventions (no `only:` on deps, short app names) — from integration_test/README.md only; not re-checked, and out of budget

## What this means when you extend the sheet

Add a fact only if you can name the command or the file that proves it, and prefer
four facts that are certainly true to twelve that are probably true. A co-change
rule ("to add X you must also touch Y") is the most valuable kind and the easiest
to get wrong: check it against every commit that touched the trigger file, not the
five most recent, which is exactly how a false rule entered the first draft here.
