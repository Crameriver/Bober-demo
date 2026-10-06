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

- `cargo test` is the whole-suite command — `sed -n '885,905p' README.md` shows the comment "# Run unit tests and integration tests" directly above `cargo test`
- `cargo test --locked --release` is the CI suite run — `grep -n 'cargo test' .github/workflows/CICD.yml` → line 105 (not shipped in the sheet, used only to confirm `cargo test` is the right invocation)
- Each tests/*.rs is its own cargo target by autodiscovery — `grep -n '^\[\[' Cargo.toml` returns nothing (no [[test]]/[[bin]] sections); `ls tests/*.rs` lists 7 files
- One-file form `cargo test --test <name>` is in use in-repo — `grep -n -- '--test ' .github/workflows/CICD.yml` → :107 `--test assets`, :131 `--test system_wide_config`
- `basic` is a real, non-ignored test in tests/integration_tests.rs — `sed -n '40,53p' tests/integration_tests.rs` shows `#[test] fn basic()` with no `#[ignore]` and no `#[cfg_attr(...)]`
- A bare filter is a substring match, so `--exact` is needed for one test — `grep -n '^fn .*basic' tests/integration_tests.rs` returns 8 functions containing "basic"
- Exactly two integration targets carry `#[ignore]` — `grep -c '#\[ignore\]' tests/*.rs` → assets.rs 1, system_wide_config.rs 2, all five others 0
- The `-- --ignored` commands and `BAT_SYSTEM_CONFIG_PREFIX` — `sed -n '120,133p' .github/workflows/CICD.yml` (prefix at :125, command at :131); `sed -n '1,12p' tests/system_wide_config.rs` carries the same command in a committed comment
- Helpers are included per target, not a crate — `sed -n '1,35p' tests/utils/command.rs` plus `mod utils;` in tests/system_wide_config.rs:3
- In-source unit tests live in `#[cfg(test)] mod tests` — `grep -rln '#\[cfg(test)\]' src/` lists 10+ module files
- fmt/clippy gate verbatim — `sed -n '58,70p' .github/workflows/CICD.yml` → `cargo fmt -- --check` and `cargo clippy --locked --all-targets --all-features -- -D warnings`
- Top-level directory set — `ls -d */` → assets build diagnostics doc examples src tests; `ls src/` and `ls src/bin/bat/` confirm lib + separate binary with clap_app.rs
- No build.rs; build script is build/main.rs — `sed -n '1,20p' Cargo.toml` line `build = "build/main.rs"`, and `ls` shows no build.rs at root
- assets/ holds the three .bin blobs, submodules and create.sh — `ls assets/`
- doc/long-help.txt and doc/short-help.txt are expect_test snapshots — `sed -n '793,820p' tests/integration_tests.rs`: `short_help` → `test_help("-h", "../doc/short-help.txt")`, `long_help` → `../doc/long-help.txt`, helper uses `expect_test::expect_file![...]`
- Both help tests are ignored on Windows / without `git` — same sed output: `#[cfg_attr(any(not(feature = "git"), feature = "lessopen", target_os = "windows"), ignore)]`
- all-jobs needs-list is machine-checked — `cat tests/github-actions.rs`: parses .github/workflows/CICD.yml, builds expected from all job keys minus exceptions `["all-jobs", "winget"]`, asserts equality with `all-jobs.needs`
- A source/ syntax fixture with no committed highlighted/ twin fails CI — `sed -n '40,50p' tests/syntax-tests/compare_highlighted_versions.py` ("No fixture for this language, run update.sh" sets has_changes), driven by `cat tests/syntax-tests/regression_test.sh`; `ls tests/syntax-tests/` confirms update.sh exists
- Mapping table is generated, not checked in — `sed -n '1,20p' src/syntax_mapping/builtin.rs` has `include!(concat!(env!("OUT_DIR"), "/codegen_static_syntax_mappings.rs"))`; `grep -n 'OUT_DIR' build/syntax_mapping.rs` → :362-363 writes that file
- Mapping rules live in .toml under six platform subdirs — `sed -n '276,335p' build/syntax_mapping.rs` (hardcoded list common/unix-family/bsd-family/linux/macos/windows, .toml-only filter, sort by file_name only); `ls src/syntax_mapping/builtins/` matches
- Tests run with CWD=tests/examples and 14 env vars removed — `sed -n '1,35p' tests/utils/command.rs`: `cmd.current_dir("tests/examples")` then 14 `env_remove` calls
- Syntaxes/themes are embedded blobs — `grep -n 'include_bytes' src/assets.rs` → :378 syntaxes.bin, :382 themes.bin, :387 acknowledgements.bin
- assets/create.sh is the regeneration entry point — `sed -n '885,905p' README.md` → `bash assets/create.sh`; `ls assets/` confirms the script

## Dropped — and why

- `src/lib.rs` is the ONLY module-declaration/re-export site — refuted (R3): `grep -rn '^\(pub \)\?mod ' src/` shows mod declarations in src/assets.rs, src/syntax_mapping.rs, src/assets/build_assets.rs, src/bin/bat/main.rs
- `src/assets/minimal_assets.rs` and `ignored_suffixes.rs` under src/assets/ — refuted (R1, R2): the files do not exist; `ls src/assets/` has lazy_theme_set.rs instead
- New-flag registration list (clap_app.rs + app.rs + config.rs + both help files + integration_tests.rs + CHANGELOG.md) — refuted as incomplete (M2: src/printer.rs 7/8, src/lib.rs 3/8 missing) and CHANGELOG.md not universal (R9, 5/8); only the mechanically enforced help-snapshot half survives and is kept as such
- BAT_* env-var registration (config.rs + main.rs only, "nothing else in src/") — refuted (R4): both proof commits also touch src/bin/bat/clap_app.rs, plus CHANGELOG.md and tests
- Theme registration (.gitmodules + assets/themes/<Name> + tests/assets.rs) — refuted (R7/R8): ansi/base16/base16-256 are in-tree .tmTheme files with no submodule, and the stated derivation cannot produce the stated observation
- Syntax-submodule four-file shape incl. CHANGELOG.md — refuted (R9: absent in 2 of 4 proof commits) and incomplete (M3: tests/no_duplicate_extensions.rs can be required)
- Fixture naming rule `issue_<number>[.ext]` — refuted (R10): tests/examples/regression_tests/ contains issue_3647_tclsh (no extension) and first_line_fallback.invalid-syntax (no issue number)
- `cargo test --lib <name>` with its CICD.yml:244/:251 citation — refuted (R5/R6): those lines are echo/interpolation, 266-278 are `cargo check`, and --lib misses the binary-crate tests
- Cargo.toml -> Cargo.lock registration rule — the supporting count (185 of 202 commits) could not be reproduced exactly and the verifier found 17 counterexamples; dropped under rule 3/4 rather than restated
- `cargo test --test integration_tests -- long_help` as the one-test example — dropped (M1): that test is #[ignore]d on Windows and reports 0 passed; replaced with the verified `--exact basic`
- All line-number citations (lib.rs:24-64, app.rs:368, clap_app.rs 829 lines, integration_tests.rs 4752 lines, etc.) — omitted under rule 3; they add no actionable value and are the category that has been wrong repeatedly
- All commit SHAs and n/9 frequency figures — omitted: the 9th flag commit was never named, so the denominators are not reproducible
- Duplicate-glob-matcher build abort and the six-subdir silent-skip trap — verified true (build/syntax_mapping.rs:339-345 and :282-299) but cut for the 2200-character budget, not because it failed
- Nix dev shell, MSRV 1.88 / feature matrix, license-checks.sh GPL grep, CHANGELOG PR-number workflow, Windows crt-static, `#![deny(unsafe_code)]` — verified-adjacent but cut for budget in favour of the test-invocation facts

## What this means when you extend the sheet

Add a fact only if you can name the command or the file that proves it, and prefer
four facts that are certainly true to twelve that are probably true. A co-change
rule ("to add X you must also touch Y") is the most valuable kind and the easiest
to get wrong: check it against every commit that touched the trigger file, not the
five most recent, which is exactly how a false rule entered the first draft here.
