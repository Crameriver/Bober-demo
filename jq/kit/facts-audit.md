# How this fact sheet was built, and what was thrown away

The sheet beside this file is short on purpose. It was produced in three passes: one
pass read the repository and wrote down everything it believed; a second pass
attacked every claim; a third kept only what it could re-verify itself, and dropped
every count and line number because those proved unreliable.

**17 facts kept, 13 dropped.** That ratio is the useful part of
this page: facts about a repository that cannot go stale are harder to produce than
they look, and a sheet that is 40% wrong is worse than no sheet, because an agent
follows it.

## Kept — each one re-verified, with the check used

- Full build+test sequence — re-read `sed -n '44,56p' README.md` (git submodule update --init / autoreconf -i / ./configure --with-oniguruma=builtin / make -j8 / make check) and `grep -n 'make check|autoreconf|./configure' .github/workflows/ci.yml` (87, 88, 102)
- No committed `configure` or `Makefile` — `git ls-files | grep -E '^(configure|Makefile)$'` returns nothing, so autoreconf is mandatory
- One suite via TESTS override — `grep -n '^TESTS = ' Makefile.am` → line 143 `TESTS = tests/mantest tests/jqtest tests/shtest tests/utf8test tests/base64test tests/uritest` (standard automake overridable variable)
- One driver directly — `tests/jqtest:5` `$VALGRIND $Q $JQ -L "$mods" --run-tests $JQTESTDIR/jq.test`; `tests/setup:13` defaults JQ; Makefile.am:148 `AM_TESTS_ENVIRONMENT = JQ=$(abs_builddir)/jq`
- One case via --skip/--take, positional selection only — `sed -n '20,50p' src/jq_test.c` shows the only two flags and that any other argv is opened as a data file; `grep -n run-tests src/main.c` → :519
- Test layout and suite pairing — `ls tests/` plus `grep -n run-tests tests/*test`: 7 drivers exec a matching tests/<name>.test, shtest and utf8test contain no --run-tests
- Record data format — `head -4 tests/jq.test`: 'Tests are groups of three lines: program, input, expected output. Blank lines and lines starting with # are ignored'
- Top-level directory roles — `ls -F --group-directories-first` (build config docs m4 scripts sig src tests vendor); `ls -A vendor/oniguruma | wc -l` → 0 (empty submodule); `sed -n '1,20p' Makefile.am` for LIBJQ lists
- manual.yml -> jq.1.prebuilt co-change — re-ran the loop over ALL 25 commits touching docs/content/manual/dev/manual.yml: 24 also touch jq.1.prebuilt, the only exception being c1d885b which CREATED the file; mechanism re-read at Makefile.am:166 and :182 (both `: $(srcdir)/docs/content/manual/dev/manual.yml`) and the gate at .github/workflows/manpage.yml:44-51 (`git diff --exit-code tests/man.test tests/manonig.test` plus a diff of jq.1.prebuilt)
- function_list[] is the C-builtin registration — `grep -n '^static const struct cfunction function_list' src/builtin.c` → 1986; builtin.c:2156 `gen_cbinding(function_list, sizeof(function_list)/sizeof(function_list[0]), builtins)`
- CLI option = isoption() chain AND usage() text — extracted all 31 long names from the isoption chain and checked each against the usage() block (src/main.c:49-142): every one present except the hidden `run-tests`
- Boolean flag needs an option-enum bit — `sed -n '143,165p' src/main.c` (RAW_OUTPUT0 = 16) and `grep -n RAW_OUTPUT0 src/main.c` → :150 enum, :386 set in the chain, :183/:205 consumed
- New src/*.c|h must be listed — Makefile.am:4 LIBJQ_INCS, :12 LIBJQ_SRC, :62 `libjq_la_SOURCES = ${LIBJQ_SRC}`
- parser.y / lexer.l edits are inert without maintainer mode — `grep -n AM_MAINTAINER_MODE configure.ac` → 18 `AM_MAINTAINER_MODE([disable])`; `sed -n '33,52p' Makefile.am` shows the non-maintainer else branch where .y.c and .l.c are plain cp + touch
- Regex builtins absent from jq.test/man.test — `grep -cE '\b(test|match|capture|scan|splits|sub|gsub)\s*\(' ` → tests/jq.test 0, tests/man.test 0, tests/onig.test 50, tests/manonig.test 17; the 4 `split(` hits in jq.test are all split/1 (string separator), so split/2 is the regex form
- onig suites are conditional — Makefile.am:207 `if WITH_ONIGURUMA` / 208 `TESTS += tests/onigtest tests/manonigtest`; configure.ac:292 AM_CONDITIONAL([WITH_ONIGURUMA])
- have_decnum guard — `grep -c have_decnum tests/jq.test tests/man.test` → 9 and 4 occurrences; .github/workflows/decnum.yml builds --disable-decnum

## Dropped — and why

- 'Six CI workflows end make check with git diff --exit-code' — refuted; my own `grep -c 'git diff --exit-code' .github/workflows/*.yml` gives ci 4, decnum 1, manpage 1, oniguruma 2, valgrind 1, scanbuild 0, website 0, and scanbuild has make check without the diff. Count unreproducible, dropped entirely.
- 'Editing src/parser.y always means committing src/parser.c (5/5)' as a co-change RULE — refuted (5dacc6b and 3a8c8f4 are counterexamples after the generated files were committed; parser.y has 30 commits). Kept only the structural statement about maintainer mode, which I verified in the build files.
- 'src/lexer.l -> also commit src/lexer.c AND src/lexer.h' — refuted: lexer.c 7/8, lexer.h 6/8 of the commits. Dropped as a rule.
- All proof_commits / sha lists, and every 'N/N' co-change count except the manual.yml one I recomputed myself — rule 3: shas and counts were wrong repeatedly, so no sha and no count ships.
- Registration point 'new jq-level builtin = five exact files' — the C-route variant was refuted (0e0cdd5 does not touch tests/man.test and does touch Makefile.am); the five-file set is not a rule. Replaced by the mechanical function_list[] claim only.
- Registration point 'new opcode = opcode_list.h + compile.c + execute.c' — survives mechanically (I re-checked all 5 non-move commits of `git log -- src/opcode_list.h` touch compile.c and execute.c) but the must_touch set is wrong (omits tests/jq.test) and most cited commits are not additions; cut for space in favour of facts an agent hits more often.
- 'to add a new file under tests/ you must touch Makefile.am EXTRA_DIST' — only 14/22 historically, and `Makefile.am:221` already distributes $(TESTS), so the rule as stated is wrong for drivers. Dropped.
- libm/configure.ac math-filter rule, @format strcmp rule, docs/manual_schema.yml additionalProperties rule, valgrind-leak trap, 4096-byte fgets trap, export-symbols-regex trap, builtin.inc octal-array trap, tests/optional.test WIN32 trap, src/version.h untracked trap — all unrefuted but cut to stay under 2200 characters; the kept facts are the ones an agent building, testing or editing jq will touch first.
- 'docs/content/manual/manual.yml is a git symlink' — I did verify it (`git ls-files -s` → mode 120000) but dropped it for space; the surviving registration line already names the correct path, docs/content/manual/dev/manual.yml.
- AC_CONFIG_MACRO_DIRS at configure.ac:17 — refuted (it is at :302). Dropped; no m4-directory line ships.
- tests/jq.test:2198-2206 'asserts every builtin is name/arity' — refuted as mischaracterised. Dropped.
- Path A / Path C candidate sections, the 1949-commit / 18-tag / 222-commit figures and the HEAD sha gloss — not part of the required output shape and count-dependent; dropped.
- Any claim that a build or test command was actually EXECUTED — I did not run make check (no configure, empty oniguruma submodule, Windows host). The commands ship as what README.md and CI spell out, which is what I re-read.

## What this means when you extend the sheet

Add a fact only if you can name the command or the file that proves it, and prefer
four facts that are certainly true to twelve that are probably true. A co-change
rule ("to add X you must also touch Y") is the most valuable kind and the easiest
to get wrong: check it against every commit that touched the trigger file, not the
five most recent, which is exactly how a false rule entered the first draft here.
