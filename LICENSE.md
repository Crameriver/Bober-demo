Copyright 2026 Marc Verriere. All rights reserved.

## What this repository is

Nine worked examples of a context-engineering engagement, published so that a prospective
client can see the work and the numbers before buying either. Each `*/kit/` directory is the
measuring tool we would leave with that client, unedited.

## What you may do with it

Read it, run it, and copy a kit into a checkout of the codebase it was written for — that is
what the case studies invite you to do, and the measurements are worth nothing if you cannot
reproduce them. `tools/estimate.py` is free to run on anything you like, including your own
private repositories: it has no network access and reads no file contents.

The kits themselves are not offered under an open-source licence. They are part of an
engagement, shown here as examples. Each one is written against one specific codebase: its
value is in the study of that codebase, not in the file format, so copying one into a different
repository gains you nothing a blank file would not.

## The codebases

The nine projects studied here are independent open-source works under their own licences —
Rocket.Chat (MIT), Keycloak (Apache-2.0), SuiteCRM (AGPL-3.0), mitmproxy (MIT), jq (MIT), Polly
(BSD-3-Clause), Hugo (Apache-2.0), bat (MIT OR Apache-2.0) and Phoenix (MIT). This repository
contains no code from any of them. It contains documentation *about* them: paths, names,
conventions and the occasional shell command. Nothing here is affiliated with or endorsed by
those projects.

## The measurements

Every figure on these pages is computed from the session records and written into the pages by
a generator, never typed, so a number and the measurement behind it cannot drift apart.
`tools/check_repo.py` fails if a codebase page, a kit's results, the landing table and the
estimator's calibration ever stop agreeing.

Where a result did not clear the noise the benchmark measured on itself, the page says so
instead of rounding it up — including the largest reduction in the repository, which is printed
and not claimed.
