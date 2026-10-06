# How this fact sheet was built, and what was thrown away

The sheet beside this file is short on purpose. It was produced in three passes: one
pass read the repository and wrote down everything it believed; a second pass
attacked every claim; a third kept only what it could re-verify itself, and dropped
every count and line number because those proved unreliable.

**23 facts kept, 14 dropped.** That ratio is the useful part of
this page: facts about a repository that cannot go stale are harder to produce than
they look, and a sheet that is 40% wrong is worse than no sheet, because an agent
follows it.

## Kept — each one re-verified, with the check used

- `./check.sh` is the documented whole-suite command — re-read AGENTS.md:19 via `cat -n AGENTS.md` (line 19: "Use `./check.sh` when you're done.")
- check.sh runs gofmt, staticcheck, then `go test -failfast $PACKAGES` with PACKAGES defaulting to ./... — re-read whole check.sh with `cat -n check.sh` (line 6 PACKAGES="${1:-./...}", line 62 `go test -failfast $PACKAGES`)
- check.sh needs bash + `bc` (check.sh:20 `echo "$end - $start" | bc` under `set -e`) and `bc` is absent here — `command -v bc` exit=1; `command -v go` exit=1 too, so the portable fallback `go test ./...` is stated
- One-package form `./check.sh ./somepackage/...` — AGENTS.md:18 verbatim via `cat -n AGENTS.md`
- Single-test invocation form `go test -count 1 -run "^Name" ./pkg/` — committed at resources/images/imagetesting/testing.go line 81 (`sed -n '75,85p'`); target named in the sheet verified real: `sed -n '1,30p' markup/goldmark/tables/tables_integration_test.go` shows line 22 `func TestTableHook` in dir markup/goldmark/tables
- CI_LOCAL=true unmasks silently-skipped tests — CONTRIBUTING.md line 79 (`sed -n '70,85p' CONTRIBUTING.md`) plus htesting/test_helpers.go:139 IsCI / :155 SupportsAll (`sed -n '128,160p'`)
- Tests live beside the code as `*_test.go` — `git ls-files '*_test.go' | wc -l` = 389, no separate test tree
- `hugolib.Test(t, files, opts ...TestOpt)` signature and txtar `files` — `sed -n '145,160p' hugolib/integrationtest_builder.go` (line 151) plus the `-- hugo.toml --` sections in tables_integration_test.go
- Every `*_integration_test.go` is in the external package `<pkg>_test` — loop over `git ls-files '*_integration_test.go'` grepping the package clause: 88 of 88 end in `_test`
- `qt` matchers rather than raw if/t.Fatal — AGENTS.md:12 verbatim; `git grep -l frankban/quicktest -- '*_test.go' | wc -l` = 276
- testscripts/ holds txtar CLI scripts in 5 dirs, each with its own runner — `ls testscripts` = commands server unfinished withdeploy withdeploy-off; `git grep -n 'testscript.Run' -- '*.go'` = main_test.go:44,:52,:67 and main_withdeploy{,_off}_test.go:27
- hugolib/ defines hugolib.Test (same read of integrationtest_builder.go); resources/page/ holds the Page and Site interfaces (`sed -n '170,175p' resources/page/page.go`, `sed -n '35,40p' resources/page/site.go`)
- tpl/tplimpl embeds the template tree — `grep -n 'go:embed' tpl/tplimpl/templatestore.go` → line 113 `//go:embed all:embedded/templates/*`
- markup/ holds the content converters registered in markup/markup.go — `sed -n '66,90p' markup/markup.go` shows the five add(...Provider) calls
- commands/ is the CLI on bep/simplecobra — `sed -n '20,45p' commands/commands.go` (newExec root list) and `grep -n simplecobra go.mod`
- tpl/tplimplinit/tplimplinit.go is the ONLY file holding `_ "github.com/gohugoio/hugo/tpl/..."` blank imports — `git grep -l '_ "github.com/gohugoio/hugo/tpl/'` returns exactly that one file (31 imports); CreateFuncMap builds the func map solely from internal.TemplateFuncsNamespaceRegistry (`sed -n '58,88p'`)
- page.Page has exactly four compile-time assertions — `git grep -n '_ page.Page\|Page .*= new(\|_ Page ' -- '*.go'`: hugolib/page.go:52, hugolib/page.go:938 (pageWithOrdinal, embeds pageState), resources/page/page_nop.go:45, resources/page/testhelpers_test.go:45
- Render-hook kind needs a RendererType constant plus a case in hugolib/page__per_output.go's switch — `sed -n '205,220p' markup/converter/hooks/hooks.go` (7 constants) and `sed -n '290,320p' hugolib/page__per_output.go` (one case per constant setting Variant1)
- No `-tags` in check.sh and buildTags() defaults to "none", so the extended/withdeploy files never compile — `git grep -n 'go:build' -- '*.go' | grep -E 'extended|withdeploy'` (deploy/*, commands/deploy.go, scss/tocss.go, client_extended.go, common/hugo/vars_*), `sed -n '340,352p' magefile.go`, and `grep -n HUGO_BUILD_TAGS .github/workflows/test.yml` → lines 126 and 133 set extended,withdeploy
- hdebug panics in real CI — `sed -n '50,65p' common/hdebug/debug.go` (panicIfRealCI) with IsRealCI = CI set and CI_LOCAL unset (htesting/test_helpers.go:144-146)
- gotmplfmt gate on tpl/tplimpl/embedded/templates and its absence from check.sh — `grep -n gotmplfmt .github/workflows/test.yml` → :64 install, :113 `diff <(gotmplfmt -d tpl/tplimpl/embedded/templates) <(printf '')`; check.sh only gofmts Go files
- tpl/*/init.go `examples` are executed as real templates by a tpl/tplimpl test — `sed -n '25,80p' tpl/tplimpl/template_funcs_test.go` (TestTemplateFuncsExamples walks TemplateFuncsNamespaceRegistry MethodMappings and asserts output)
- media/config_test.go and output/outputFormat_test.go pin exact default counts — `sed -n '150,162p' media/config_test.go` (len(DefaultTypes) assertion) and `grep -n 'len(DefaultFormats)' output/*_test.go` → outputFormat_test.go:71

## Dropped — and why

- `mage -v check` == `go test -race ./... -tags extended,withdeploy` — refuted (CI takes the per-package loop branch); all mage target internals dropped, only the HUGO_BUILD_TAGS env fact kept
- ab4e1dfa as proof commit for media/builtin.go + media/config_test.go and for output/outputFormat.go — refuted, it touches neither file
- "one package per template namespace, each registering from its own init.go" and must_touch tpl/<ns>/init.go — refuted: re-ran `git grep -l 'internal.AddTemplateFuncsNamespace' -- tpl/` = 31 files, two NOT init.go (tpl/css/css.go, tpl/hash/hash.go); the recipe `--diff-filter=A -- 'tpl/*/init.go'` is blind to them
- fa7d37f0 "22 init.go files" — refuted (21); all proof-commit shas and counts removed from the sheet
- "~1000 hugolib.Test call sites across 93 test files" — refuted as internally inconsistent; no call-site count shipped
- common/ as "leaf helper packages with no Hugo-internal dependencies" — refuted (5 of 7 named packages have internal deps); common/ line dropped from the module map entirely
- "pageState is the one real implementation of page.Page" — refuted; restated as "each compile-time assertion" listing the files
- Line citations 26 for testscript.Run in main_withdeploy*_test.go and 115-118 for the staticcheck CI step — refuted; re-checked: testscript.Run is at :27, so no line numbers are quoted for those
- Registration rule "security.DefaultConfig change must also touch config/security/securityConfig_test.go" — dropped under rule 4: over ALL 31 commits touching securityConfig.go only 23 also touch the test file (8 do not), so it does not hold across all commits
- Registration rule "media/builtin.go change must also touch media/config_test.go" as a commit-derived rule — dropped under rule 4 (a795acbc touches builtin.go only); kept only the code-verified snapshot-count trap
- Registration rules for a new config section (allconfig.go + alldecoders.go), a new CLI command (commands/<name>.go + commands.go), a new embedded template, a new output format and a new media-type field — mechanisms verified but cut for the 5-line/2200-char ceiling; the strongest four were kept
- Go version, module path, commit count, top-level dir count, 4211/39, and all exact numbers (47 DefaultTypes, 15 DefaultFormats, 389/88/79/276 file counts) — reproduced but omitted: numbers have been wrong repeatedly and add no actionable value, so rules are stated without them
- Deprecation escalation ladder, stringer/autogen hand-edit trap, docs/data/docs.yaml generation, CLI-flag-becomes-config-key trap, golden-image GOARCH pinning, forked go_templates tree — all unrefuted but cut to the 4-trap limit; not re-verified, so not shipped
- Path A / Path B / Path C candidate material — the draft JSON is truncated and the verifier flagged the answer keys as undelivered/unverifiable; nothing from there is shipped

## What this means when you extend the sheet

Add a fact only if you can name the command or the file that proves it, and prefer
four facts that are certainly true to twelve that are probably true. A co-change
rule ("to add X you must also touch Y") is the most valuable kind and the easiest
to get wrong: check it against every commit that touched the trigger file, not the
five most recent, which is exactly how a false rule entered the first draft here.
