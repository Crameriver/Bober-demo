# Facts about this repository

## Building and testing
`./mvnw` only; sources compile at release 17 (root POM `maven.compiler.release`), CI on JDK 25.
- All: `./mvnw clean install -DskipTests`; server only: add `-pl quarkus/deployment,quarkus/dist -am`.
- UTs: `./mvnw test -am -pl "$(.github/scripts/find-modules-with-unit-tests.sh)"`.
- ITs: `./mvnw package -pl tests/base -Dtest=<Class>`; suites run from the `tests` aggregator. Legacy: `-Pauth-server-quarkus -pl testsuite/integration-arquillian/tests/base`.
- Tests unpack `quarkus/dist/target/keycloak-<ver>.zip` (build it first) unless `KC_TEST_SERVER=embedded`; also `KC_TEST_DATABASE`/`KC_TEST_BROWSER`.
- Not committed: ANTLR parsers, kiota TS client, asciidoc guides; run Maven before an IDE build.
- `./mvnw -Pdocs,distribution,operator spotless:check`: imports only, no formatter; operator/ and distribution/ need their profiles.

## Where things live
- server-spi(-private) provider interfaces; services REST + logic; rest/admin-v2 new Admin API.
- model/ jpa (schema+Liquibase), infinispan (caches), storage-private (migrations).
- quarkus/ config-api (options), runtime, deployment (augmentation), dist (zip).
- tests/+test-framework/ current JUnit5 stack; testsuite/ frozen Arquillian; themes/ and js/ the UIs.

## Changing things together
- A theme dir is dead unless name+types are listed in that module's theme manifest under `META-INF/`.
- New Liquibase file -> `<include file=...>` in `META-INF/jpa-changelog-master.xml`.
- New JPA entity -> a `<class>` line in `model/jpa/src/main/resources/default-persistence.xml`.
- New package under tests/base/.../keycloak/tests/ -> add it to an aggregate suite class in the sibling `suites` package, or CI fails.
- New SPI/provider -> a `META-INF/services/` entry AND `kc.sh build`; discovery is closed-world at build time.
- New CLI option -> golden help files under quarkus/tests/integration/.../approvals/cli/help/; rewrite with `KEYCLOAK_REPLACE_EXPECTED=true`.

## Traps
- `testsuite/` is frozen: a PR to main fails if a file is added there or 100+ lines land in one (.github/actions/testsuite-deprecation-check/).
- The `keycloak` login theme ships no templates; `keycloak.v2` is the default (LOGIN_V2), so editing base/login may change nothing.
- The rolling-upgrade DB gate runs in model/jpa's `test` phase, but the JSON files it compares are absent: it passes silently.
- The committed OpenAPI doc under js/libs/keycloak-admin-client/ is overwritten by the rest/admin-v2 build.
