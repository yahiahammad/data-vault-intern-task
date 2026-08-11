# data-vault-intern-task

## What this actually is

An intern task that grew into a 4-milestone analytics-platform build. The
task sheet is `intern-task-ducklake-stack.md.pdf` (extract text with
`pdftotext -layout`, `Read` can't render PDFs on this machine — no
`poppler-utils`).

**The purpose of this repo is for the user to learn while building it.**
That governs how to work here, more than usual:

- Explain the *mechanism*, not just the fix — why a container can't reach
  `localhost`, why Cosmos re-runs `dbt deps` per task, why a column doesn't
  show up as a datetime candidate. The explanation is often the actual
  deliverable, the code change is secondary.
- Don't silently pick a side on a real architectural fork (separate DB per
  app vs. shared instance, cast in dbt vs. cast at the BI layer, etc.) —
  ask, the way earlier sessions did throughout Milestone 1.
- When something breaks, diagnose from real evidence (container logs,
  `information_schema`, actual data) before proposing a fix, and say what
  the evidence showed. Several M1 bugs were genuine data/config issues, not
  guesses.

## Milestone map

| # | Scope | Status |
|---|-------|--------|
| 1 | Airflow + dbt + Cosmos + Superset + Redis, all against the existing Postgres vault | **Done** |
| 2 | Swap storage: DuckLake/DuckDB + MinIO under the same dbt models | **Airflow side done** — pipeline runs green through Cosmos, row-for-row parity with the M1 Postgres vault. Superset still points at Postgres. |
| 3 | Replace CSV drops with API ingestion | Spec not written yet — don't start early |
| 4 | Productionize: compaction/snapshot expiry, catalog backups, secrets out of compose, Superset RBAC, alerting, README/runbook, retire old Postgres silver tables | Not started |

Milestone order is deliberate: if M2 goes badly, M1 is still a working
platform. Don't skip ahead to M3 before M2's "done when" check passes: *the
lake reproduces the Postgres vault row-for-row, and a dashboard loads
correctly while a DAG run is in progress.*

## Layout

```
dbt/data_vault_dbt/     dbt project — models/{staging,intermediate,raw_vault/{hubs,links,ref_hubs,satellites,ref_satellites}}
docker/docker-compose.yaml   one compose file, all services (postgres, airflow-*, redis, superset*)
docker/postgres/init.sql     bootstraps raw.fbnk_* from data/*.csv on a FRESH volume only
docker/airflow/               custom image: apache/airflow + dbt-postgres + astronomer-cosmos
docker/superset/               custom image: apache/superset + psycopg2-binary
data/*.csv                    the only source data right now (M3 replaces this)
```

Every app gets its own metadata Postgres (`postgres` = data vault,
`airflow-postgres`, `superset-postgres`) rather than sharing one instance —
established in M1 for isolation, keep the pattern in M2 (`ducklake_catalog`
per the task sheet is a 4th database, likely on `postgres` itself — check
the spec's wording before assuming a new container).

## Load-bearing gotchas from Milestone 1 (don't rediscover these)

- **`raw.fbnk_*` tables are not loaded by dbt.** They're `sources`, not
  seeds. `docker/postgres/init.sql` loads them via `\copy`, but Postgres
  only runs `docker-entrypoint-initdb.d/` scripts on a *fresh* volume. If
  the volume already exists, load manually (see the git history around the
  "raw.fbnk_account does not exist" fix for the exact commands).
- **Containers reach each other by service name, never `localhost`.**
  `localhost` inside a container means itself. This bit Superset's DB
  connection and Airflow's dbt connection both.
- **The official `apache/airflow` and `apache/superset` images don't bundle
  the Postgres driver.** Both needed a custom Dockerfile adding
  `dbt-postgres`/`psycopg2-binary`. Superset's image specifically uses a
  `uv`-managed venv at `/app/.venv` with **no `pip` inside it** — install
  with `uv pip install --python /app/.venv/bin/python -r requirements.txt`,
  not plain `pip install` (that installs into the wrong Python silently).
- **`load_dts` is the batch-load timestamp** (`current_timestamp`, one
  value per dbt run), **`created_ts`/`src_eff` is the per-record version
  discriminator.** If a source batch ever contains >1 real version of the
  same key, uniqueness tests need `(hk, load_dts, created_ts)`, not just
  `(hk, load_dts)` — this happened for real with the test account-balance
  data.
- **Cosmos**: `operator_args.install_deps` and `RenderConfig.dbt_deps` must
  match, or the DAG fails to import. `dbt_packages/` is gitignored but
  physically present (someone ran `dbt deps` locally) and gets volume-mounted
  in — that's why `install_deps: False` is safe here specifically.
- **Superset's "Main Datetime Column" only offers columns Postgres typed as
  `date`/`timestamp`.** Raw vault columns like `opening_date` came in as
  `text` off the CSV and were never cast. Fix at the reporting layer (a
  SQL Lab virtual dataset with `to_date(col, 'YYYYMMDD')`), not by changing
  the vault's typing, unless there's a reason every consumer needs it.
- Airflow's `LOAD_EXAMPLES` and default `@daily` schedule are both off in
  this repo on purpose (`false` / `schedule=None`) — the DAG only runs when
  triggered.

## Load-bearing gotchas from Milestone 2 (DuckDB/DuckLake)

- **AutomateDV has no built-in DuckDB support** (only Snowflake/BigQuery/
  Databricks/Postgres/SQL Server). Most of its dispatched macros still work
  via a `default__` fallback (and the actual `hub`/`link`/`sat` table
  builders under `tables/snowflake/` are really the generic defaults,
  despite the folder name) — but `get_escape_characters`, `cast_date`,
  `cast_datetime`, `type_binary`, and `hash_alg_md5` have no default and
  needed real `duckdb__*` overrides, in `macros/duckdb_dispatch.sql`, found
  by running models and fixing whatever the next dispatch error named —
  don't try to pre-audit every macro. Requires a `dispatch:` block in
  `dbt_project.yml` pointing dbt at our own project first.
- **The lake must be attached declaratively in `profiles.yml`'s `attach:`
  list, not via an `on-run-start` hook.** dbt validates a model's configured
  `+database` at connection setup, before `on-run-start` hooks run — attach
  there and every model fails with "Catalog does not exist" even though the
  hook itself would have worked fine, just too late.
- **Every layer needs `+database: lake`, not just the physical raw_vault
  tables.** Cosmos gives each model its own task = its own fresh, isolated
  DuckDB session; nothing survives in DuckDB's own `:memory:` catalog
  between tasks. A `view` is fine (its definition persists in the
  Postgres-backed DuckLake catalog, re-executed on read), but only if it
  was created *in* the lake, not the ephemeral default catalog. Seeds need
  the same `+database: lake` — they're a separate dbt command too.
- **DuckDB uses `unhex(md5(x))` for a binary MD5, not `MD5_BINARY()`**
  (that's Snowflake-only, sitting under `default__hash_alg_md5` because
  Snowflake was the original platform) — and its binary type is bare
  `BLOB`, not a sized `BINARY(16)`.
- **Thread-level concurrency races; process-level concurrency doesn't.**
  `dbt run --threads 4` reliably hit a DuckLake catalog race ("schema not
  found in metadata catalog") — multiple threads sharing one dbt-duckdb
  connection. But the same project via Cosmos on LocalExecutor ran **69/69
  tasks green with up to 32 genuinely overlapping tasks** (1012s of task
  work in 87.7s wall time), because each Airflow task is its own process
  with its own DuckDB session committing through Postgres — exactly what
  DuckLake's catalog-as-Postgres-transactions design is built for. So keep
  `threads: 1` in profiles.yml, and let Airflow provide the parallelism.
- **Cosmos caches `dbt ls` output in an Airflow Variable**
  (`cosmos_cache__data_vault_dbt`), not only in `/tmp/cosmos/`. A DAG that
  "parses fine" may be replaying that cache — deleting the /tmp dir alone
  doesn't force a real re-parse, so a broken project can look healthy until
  something invalidates the cache. That's what hid the packages.yml problem
  below all through M1.
- **`packages.yml` must declare transitive dbt packages explicitly.**
  Cosmos deliberately never symlinks `package-lock.yml` into its `dbt ls`
  temp dir, so dbt can't see the resolved dependency tree and just counts
  `packages.yml` entries against folders in `dbt_packages/`. AutomateDV
  pulls in `dbt_utils`, so with only automate_dv declared dbt fails with
  "expects 1 package(s) ... found 2" — surfaced by Cosmos, confusingly, as
  "missing dbt_packages. Set RenderConfig.dbt_deps=True". Declaring
  `dbt-labs/dbt_utils` explicitly fixes it and keeps `dbt_deps=False`.
- **`profiles.yml` mounted into Airflow must NOT be `:ro`.** `airflow-init`
  runs `chown -R /opt/airflow/`, which fails hard on a read-only bind mount
  and takes the whole init container down with it.
- Verified row-for-row parity against the M1 Postgres vault on every table
  checked, and confirmed real Parquet files land in MinIO
  (`data_vault/<table>/ducklake-*.parquet`) — already visibly one-file-per-
  incremental-run, i.e. the small-files problem M4's compaction step exists
  for is real and starts on day one, not just at scale.

## Conventions

- One `docker/docker-compose.yaml`, all apps as services in it — not one
  compose file per app.
- `docker/.env` holds secrets (`FERNET_KEY`, `SUPERSET_SECRET_KEY`, admin
  creds) — gitignored, `.env.example` documents what's required.
- Commit in small, working pieces (task sheet's own instruction) — not one
  commit per session.
