# Facts about this repository

## Building and testing
- Suite: `./check.sh` (AGENTS.md:19) - bash; gofmt, staticcheck, then `go test -failfast ./...` (check.sh:62). Needs bash+`bc`; else `go test ./...`.
- One package: `./check.sh ./hugolib/...` (AGENTS.md:18). One test: `go test -count 1 -run "^TestTableHook" ./markup/goldmark/tables/`. No per-file runner: give the dir plus a `-run` regex.
- Without `CI_LOCAL=true`, tests gated on `htesting.IsCI()`/`SupportsAll()` skip silently (CONTRIBUTING.md:79).
- Tests sit beside the code as `*_test.go`; prefer `*_integration_test.go` calling `hugolib.Test(t, files, opts...)`, `files` a txtar string of `-- path --` sections, in package `<pkg>_test` (hugolib imports the package under test). Use `qt` matchers, not `t.Fatal` (AGENTS.md:11-12).
- CLI tests: txtar scripts under testscripts/ (5 dirs), run from main_test.go / main_withdeploy*_test.go.

## Where things live
- hugolib/ - build orchestrator; defines `hugolib.Test`.
- resources/ - assets; resources/page/ = Page/Site interfaces.
- tpl/ - template funcs per namespace; tplimpl = embedded templates.
- markup/ - content converters (markup/markup.go).
- commands/ - the CLI; testscripts/ - txtar CLI scripts.

## Changing things together
- A `tpl/<ns>` package is dead until blank-imported in tpl/tplimplinit/tplimplinit.go, the only such import list.
- A new `page.Page` method must be implemented at each compile-time assertion: resources/page/page_nop.go, resources/page/testhelpers_test.go, `pageState` (hugolib/page.go:52).
- A render-hook kind needs a `RendererType` constant (markup/converter/hooks/hooks.go) and a `case` in hugolib/page__per_output.go's switch, or no template resolves.

## Traps
- check.sh passes no `-tags`: deploy/ and the extended SCSS code never compile. CI sets `HUGO_BUILD_TAGS=extended,withdeploy`.
- `hdebug.Printf` left in the tree panics in real CI by design.
- Files under tpl/tplimpl/embedded/templates/ must be formatted with `gotmplfmt`; CI diffs it, check.sh does not.
- Snapshots fail in packages you did not edit: `tpl/*/init.go` `examples` are executed by a tpl/tplimpl test; media/config_test.go and output/outputFormat_test.go pin default counts.
