# Facts about this repository

## Building and testing
Absent here: `vendor/`, `cache/`, `custom/`, `config.php`, `config_override.php`, all of `tests/` — so `composer install` (PHP ^8.1, composer.json) and a web install come first. Runner = Robo (root RoboFile.php is deliberately empty; commands in lib/Robo/Plugin/Commands/). Unit: `robo tests:unit` = `vendor/bin/phpunit --configuration ./tests/phpunit.xml.dist ./tests/unit/phpunit`; one file = append its path; one test = add `--filter <testName>`. Codeception: `tests:api`; `tests:acceptance`/`tests:install` add `--env custom`.

## Where things live
- modules/ — one dir per CRM module: bean, vardefs.php, metadata/, views/, language/.
- include/ — framework: MVC, SugarFields, SugarObjects, Smarty, DB, utils.
- data/ — SugarBean + BeanFactory; lib/ — PSR-4 `SuiteCRM\` (Robo, Search).
- metadata/ — many-to-many relationship tables, NOT module metadata.
- Api/ — live REST v8 (Slim 3); service/ + soap/ — the legacy SOAP/REST.
- ModuleInstall/ — installs uploaded packages; install/ — the web installer.
- jssource/src_files/ — unminified JS; themes/ — Smarty tpls + SCSS.

## Changing things together
- New bean -> register in include/modules.php (`$moduleList`, `$beanList`, `$beanFiles`). `$beanFiles` also feeds SugarAutoLoader and `repair:database`: omit it and the class never autoloads and gets no table.
- A new file in metadata/ is inert until `include`d from modules/TableDictionary.php.
- Editing modules/<M>/vardefs.php or a module language file does nothing until cache/modules/<M>/ is rebuilt (grep `sugar_cached`, `RepairAndClear`).
- New cron job: an entry in `$job_strings` AND `LBL_<FUNCTIONNAMEUPPERCASED>` in the Schedulers language file, else the dropdown shows the raw key.
- Per-module metadata is reached via `$metafiles`, not by convention.
- Admin settings write to config_override.php, never config.php.

## Traps
- `$sugar_version` is 6.5.25 (SugarCRM heritage); the real version is `$suitecrm_version`.
- include/javascript/*.js are MINIFIED outputs; source = jssource/src_files/<same path>. The browser loads cache/include/javascript/sugar_grp*.js, built at request time.
- Field types alias: `date`->Datetime, `url`->Link, `varchar`->Base (grep `fixupFieldType`).
- Logic hooks load only from custom/ (grep `call_custom_logic`).
- phpcs.xml is dead; the lint task wants `.php_cs.dist`, absent here.
- Most PHP files die unless `sugarEntry` is set (grep 'Not A Valid Entry Point').
