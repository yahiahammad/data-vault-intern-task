"""Runs the data_vault_dbt project as an Airflow DAG, one task per dbt model."""
from datetime import datetime

from cosmos import DbtDag, ProfileConfig, ProjectConfig, RenderConfig

# M2: DuckDB's profile shape (extensions/attach/settings) has no equivalent
# Cosmos ProfileMapping class -- point it at a real profiles.yml file instead.
profile_config = ProfileConfig(
    profile_name="data_vault_dbt",
    target_name="dev",
    profiles_yml_filepath="/opt/airflow/dbt/profiles.yml",
)

data_vault_dag = DbtDag(
    dag_id="data_vault_dbt",
    project_config=ProjectConfig("/opt/airflow/dbt/data_vault_dbt"),
    # dbt_deps/install_deps must always match, or the DAG fails to import.
    # Both False: dbt_packages/ is already vendored and volume-mounted in, so
    # re-running `dbt deps` on every one of ~40 tasks is pure wasted time.
    render_config=RenderConfig(dbt_deps=False),
    profile_config=profile_config,
    schedule=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    operator_args={"install_deps": False},
)
