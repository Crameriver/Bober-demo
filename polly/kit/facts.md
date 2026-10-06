# Facts about this repository

## Building and testing
SDK pinned to 10.0.401 (`global.json`); runner is Microsoft.Testing.Platform, not VSTest.
- Whole suite, all gates (what CI runs): `./build.ps1` in pwsh at the repo root
- Tests only: `dotnet test`
- One project: `dotnet test ./test/Polly.Core.Tests/Polly.Core.Tests.csproj`
- One class: `dotnet test ./test/Polly.Core.Tests --filter "FullyQualifiedName~RetryHelperTests"`
- Add `--framework net10.0`, else every project runs net10.0;net9.0;net8.0 (+net481 on Windows)

Tests: `test/<Pkg>.Tests/<same subfolder as src>/<Name>Tests.cs`, namespace mirrors the folder; only `*{Tests,Specs}.csproj` under test/ is run. Legacy `src/Polly` -> `test/Polly.Specs`, whose `*Specs.cs` are named per policy, not per source file (`TimeoutEngine.cs` -> `TimeoutSpecs.cs`). `eng/Test.targets` adds global `using Shouldly; using Xunit;` + NSubstitute (xunit v3): assert via Shouldly.

## Where things live
- src/Polly.Core - v8 engine, one folder per strategy (Retry, Timeout, CircuitBreaker, Hedging, Fallback, Simmy)
- src/Polly legacy v7 API (nullable OFF by design) | src/Polly.Extensions DI+telemetry | src/Polly.RateLimiting | src/Polly.Testing
- eng/ shared MSBuild+analyzers | docs/ docfx | bench/ | samples/ a second .slnx, also built

## Changing things together
- New public member -> a line in `src/<Pkg>/.PublicAPI/PublicAPI.Unshipped.txt`, else RS0016 fails the build; never edit PublicAPI.Shipped.txt.
- New NuGet dep -> version-less `<PackageReference>` + a `<PackageVersion>` in Directory.Packages.props.
- C# shown in any .md -> edit the `#region` in src/Snippets/Docs/*.cs; markdown is generated and gated at build time.
- New project -> `<ProjectType>`Library|Test|Benchmark + an entry in a `.slnx`, else it gets no targets and is never built.

## Traps
- 100% line+branch+method coverage gates the build, per TFM (Polly.Specs 96,95,93).
- `./build.ps1` makes every warning an error and runs all analyzers; `dotnet build` is laxer. Escape: `/p:SKIP_POLLY_ANALYZERS=true`.
- DateTime/DateTimeOffset `.Now`/`.Today` are banned outside tests; take a TimeProvider.
- Expression-bodied members are `:error` in .editorconfig (enforced in build).
