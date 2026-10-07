# Facts about this repository

## Building and testing
Yarn 4 workspaces + turbo; Meteor 3.5.2 (apps/meteor/.meteor/release). `yarn install` then `yarn build` FIRST (turbo.json): every workspace `dist/` is gitignored; CI ships it as the `packages-build` artifact before any test job (ci-test-unit.yml). All unit tests: `yarn testunit`; one workspace: `yarn workspace <pkg> testunit`. In apps/meteor that's 3 runs: guard mocha (.mocharc.definition.js), jest (jest.config.ts), mocha+nyc (.mocharc.js). `yarn testapi` (mocha/REST) and `yarn test:e2e [file]` (Playwright) need a live server: `TEST_MODE=true yarn dev`, or CI's compose stack. `yarn lint` and `yarn turbo run typecheck` both shell out to `meteor lint`, so the Meteor toolchain is needed even to typecheck. User-visible change => changeset (.changeset/config.json).

## Where things live
- `apps/meteor/` the Meteor monolith; server code is responsibility-first, `server/<api|services|lib|hooks|cron|settings|startup>/<domain>/` (docs/backend-folder-structure.md).
- `apps/meteor/ee/`, `ee/apps/`, `ee/packages/` = Enterprise; the directory IS the license boundary.
- `packages/` = `@rocket.chat/*` workspaces; `apps/meteor/packages/` = Meteor/Atmosphere packages.
- `tests/end-to-end/` = mocha REST, `tests/e2e/` = Playwright UI.

## Changing things together
- Nothing is auto-discovered: a new boot module, endpoint group, migration, Meteor method, setting-definition file, room type or EE patch runs only once its side-effect import lands in its folder's barrel - lint, tsc and tests stay green when you forget.
- Models wire by STRING key: typings interface + class export + `registerModel(...)` in both the monolith and the microservices registrar; a mismatch throws `Model X not found` at runtime only.
- Translations: edit `packages/i18n/src/locales/en.i18n.json` only; other locales are derived, rewritten by `yarn workspace @rocket.chat/i18n lint`. A misspelled key is NOT a compile error.

## Traps
- `apps/meteor/app/` is frozen: only `*/lib`, `theme/client`, `apps/server` remain. `imports/`, `server/meteor-methods/`, `server/publications/` are deprecated - add REST.
- The two unit runners have disjoint allow-lists: a spec in a folder matched by neither silently never runs; a jest-style spec caught by a mocha glob dies with `jest is not defined`.
- Some committed paths under `apps/meteor/private/` and `apps/meteor/public/` are symlinks into `node_modules` or a generated `dist/`; they dangle before install+build.
