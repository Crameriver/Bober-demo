# How this fact sheet was built, and what was thrown away

The sheet beside this file is short on purpose. It was produced in three passes: one
pass read the repository and wrote down everything it believed; a second pass
attacked every claim; a third kept only what it could re-verify itself, and dropped
every count and line number because those proved unreliable.

**22 facts kept, 15 dropped.** That ratio is the useful part of
this page: facts about a repository that cannot go stale are harder to produce than
they look, and a sheet that is 40% wrong is worse than no sheet, because an agent
follows it.

## Kept — each one re-verified, with the check used

- SDK pinned to 10.0.401, allowPrerelease false — `cat global.json`
- Test runner is Microsoft.Testing.Platform, not VSTest — global.json "test": {"runner": ...}
- CI's one build step is `./build.ps1` — `sed -n '90,105p' .github/workflows/build.yml` (name: Build, Test and Package / shell: pwsh / run: ./build.ps1)
- build.ps1 drives cake — build.ps1:28 `$Script = "cake.cs"`, build.ps1:85 `& dotnet $Script -- --target=...`
- `dotnet test`, per-project, `--filter "FullyQualifiedName~..."`, `--framework net10.0` are the repo's documented commands — `sed -n '10,40p' AGENTS.md`
- TFMs net10.0;net9.0;net8.0 plus net481 on Windows — `sed -n '1,10p' test/Polly.Core.Tests/Polly.Core.Tests.csproj`
- Only *{Tests,Specs}.csproj under test/ is executed — cake.cs `__RunTests` glob `./test/**/*{Tests,Specs}.csproj` (`sed -n '141,160p' cake.cs`); `ls test/*/*.csproj` shows the 7 projects, 5 match
- Test path/name convention test/<Pkg>.Tests/<src subfolder>/<Name>Tests.cs — python walk of src/Polly.Core vs test/Polly.Core.Tests (dominant pattern, 110/174; number not shipped)
- Namespace mirrors the folder — `head -12 test/Polly.Core.Tests/Retry/RetryHelperTests.cs` (namespace Polly.Core.Tests.Retry) and the Timeout equivalent
- test/Polly.Specs files are named per policy, not per source file — `ls test/Polly.Specs/Timeout/` shows TimeoutSpecs.cs, TimeoutAsyncSpecs.cs and no TimeoutEngineSpecs.cs
- Global `using Shouldly; using Xunit;`, NSubstitute, xunit.v3.mtp-v2 — `cat -n eng/Test.targets` lines 9-23
- Module map — `ls src`, `ls eng`, `ls bench samples`, `ls src/Polly.Core` (strategy folders Retry/Timeout/CircuitBreaker/Hedging/Fallback/Simmy), `ls src/Polly.Extensions` (DependencyInjection/, Telemetry/)
- src/Polly keeps nullable off by design while Polly.Core enables it — `sed -n '1,16p' src/Polly/Polly.csproj` (comment, no <Nullable>) vs `grep -n Nullable src/Polly.Core/Polly.Core.csproj`
- PublicAPI.Unshipped.txt is required and Shipped.txt is release-owned — `sed -n '40,75p' eng/Library.targets` (PublicApiAnalyzers + .PublicAPI AdditionalFiles), `find src -name "PublicAPI*.txt"`, `sed -n '1,30p' eng/update-baselines.ps1`
- Central package versions — Directory.Build.props:4 ManagePackageVersionsCentrally true; `grep -rn PackageReference --include=*.csproj src test bench | grep -i Version=` returns nothing
- Snippets are the source of docs code and are gated — `cat mdsnippets.json` (Convention InPlaceOverwrite, ExcludeSnippetDirectories), `sed -n '330,356p' cake.cs` (__ValidateDocs runs `dotnet mdsnippets --validate-content`, inside __CommonBuild before __BuildSolutions)
- <ProjectType> plus a .slnx entry are mandatory — Directory.Build.targets:3 conditional import of eng/$(ProjectType).targets, `grep -rn "<ProjectType>"`, cake.cs:21 `GetFiles("./**/*.slnx")`, `find . -name "*.slnx"` = 2
- Coverage gate is 100% and is evaluated per TFM — `grep -rn "<Threshold" test/*/*.csproj` (four 100, Polly.Specs 96,95,93) and `sed -n '255,305p' cake.cs` (loops coverage.<tfm>.xml, throws on violation)
- Warnings-as-errors exists only in the cake build — `sed -n '110,120p' cake.cs` TreatAllWarningsAs = Error; `grep -rn TreatWarningsAsErrors --include=*.props --include=*.targets --include=*.csproj .` returns nothing
- SKIP_POLLY_ANALYZERS is a real kill switch — `sed -n '1,20p' eng/Analyzers.targets` and `grep -rn SKIP_POLLY_ANALYZERS` (gh-pages.yml:50, mutation-tests.yml:71, Polly.AotTest.csproj:6)
- DateTime/DateTimeOffset .Now/.Today banned outside tests — `cat eng/analyzers/BannedSymbols.txt` + Analyzers.targets:6 `Condition=" '$(IsTestProject)' != 'true' "`
- Expression-bodied members at :error, enforced in build — `grep -n ":error" .editorconfig` (6 rules) + eng/Analyzers.targets EnforceCodeStyleInBuild true

## Dropped — and why

- Mirror ratio "126 of 174 (72%)" — refuted; my own walk gives 110/174, so the rule is stated with no number
- "Libraries multi-target net8.0;net6.0;netstandard2.0;net472;net462" — refuted; src/Polly/Polly.csproj:4 has no net8.0 and src/Polly.Testing is net8.0;netstandard2.0
- "The four other Unshipped files contain only the #nullable enable header" — refuted (src/Polly's is a bare BOM); not needed for any surviving rule
- Polly.Specs mirroring as "<same subdir>/<Name>Specs.cs" — refuted (12% hit); replaced by the per-policy naming I re-checked in test/Polly.Specs/Timeout
- "--filter is equivalent to one file because every test file has exactly one class of that name" — refuted (IssuesTests, ResiliencePipelineTests are partial across files; 12 helper files carry no Tests suffix); the command is kept as a class-substring filter
- "The six Snippets commits without a .md are pure style passes" — refuted (f5cbe89c, 3254c539 are not); characterization dropped, the mechanism kept
- Issues/ naming with the file count — count wrong (7 of 8 match, one has a space in its name); dropped for budget rather than restated
- All proof-commit shas and co-change percentages (72/61, 82/76, 263/51/18, 12) — not re-checkable inside this budget; every surviving rule now rests on a mechanism I read instead
- Line-number citations (cake.cs:350-353, 141-156 were off by one) — dropped entirely; the sheet names files and properties, no line numbers
- Commit totals (2971 / 2777) — no operational value, dropped
- Mutation-score gate (100 in the five shipped csprojs, Stryker, mutation-tests.yml matrix) — verified by grep but cut to fit 2200 chars
- InternalsVisibleToProject rule (only route to internals, no [InternalsVisibleTo] in any .cs) — verified by grep but cut for budget
- AOT/trim publish, package-validation baseline, the five TypeForwardedTo entries, wordlist/spellcheck gate, "no central strategy registry" (grep AddStrategy confirmed one builder-extension per strategy) — verified but cut for budget
- build.ps1's -Configuration ValidateSet trap and AGENTS.md:84 being wrong about LegacySupport — verified but cut for budget
- Every command as an observed-working fact — unverifiable here: no .NET SDK on this machine (`dotnet --version` reports "A compatible .NET SDK was not found"), so commands are transcribed from AGENTS.md and the CI workflow

## What this means when you extend the sheet

Add a fact only if you can name the command or the file that proves it, and prefer
four facts that are certainly true to twelve that are probably true. A co-change
rule ("to add X you must also touch Y") is the most valuable kind and the easiest
to get wrong: check it against every commit that touched the trigger file, not the
five most recent, which is exactly how a false rule entered the first draft here.
