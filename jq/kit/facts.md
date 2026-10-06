# Facts about this repository

## Building and testing
No `configure` and no `Makefile` are committed (Autotools). Whole suite:
`git submodule update --init && autoreconf -i && ./configure --with-oniguruma=builtin && make -j8 && make check VERBOSE=yes` (README.md; ci.yml:87-102).
- One suite: `make check TESTS=tests/jqtest VERBOSE=yes` (TESTS, Makefile.am:143)
- One driver, built tree: `JQ=$PWD/jq sh tests/jqtest`
- One case: `./jq --run-tests --skip N --take 1 tests/jq.test` — positional only, no name selector (src/jq_test.c)
tests/ is flat, not mirrored on src/. Each suite = sh driver `tests/<name>test` + data file `tests/<name>.test` fed to `$JQ --run-tests`. Data = 3-line records (program / input / expected output lines), blank-line separated, `#` ignored. shtest and utf8test are hand-written shell.

## Where things live
- src/ — libjq + CLI (main.c); src/builtin.jq is the jq-written stdlib, embedded
- tests/ — whole suite, plus modules/ and torture/ fixtures
- docs/ — content/manual/dev/manual.yml + Python manpage/man-test/site generators
- vendor/ — decNumber + oniguruma (empty submodule); scripts/, config/, m4/ — codegen, autoconf

## Changing things together
- Edit docs/content/manual/dev/manual.yml -> regenerate and commit jq.1.prebuilt, and tests/man.test or manonig.test if an example changed (Makefile.am:166,182; gate manpage.yml).
- New C builtin -> the `f_<name>` body AND a row in `function_list[]` (builtin.c:1986); an f_* not listed there is dead code.
- New CLI option -> the isoption() chain AND the usage() text; a boolean flag also needs a bit in main.c's option enum.
- New src/*.c or .h -> add to LIBJQ_SRC/LIBJQ_INCS (Makefile.am:4-18) or it is never built.

## Traps
- Editing parser.y/lexer.l alone does nothing: maintainer mode is off (configure.ac:18), so the .y/.l rules only cp+touch the committed parser.c|h and lexer.c|h (Makefile.am:33-52).
- Regex builtins (test/match/capture/scan/sub/gsub/splits, split/2) go in tests/onig.test or manonig.test, never jq.test or man.test; those two run only `if WITH_ONIGURUMA` (Makefile.am:207).
- Precision-sensitive expectations read `== if have_decnum then X else Y end`; CI also builds --disable-decnum.
