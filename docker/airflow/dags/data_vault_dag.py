"""Runs the data_vault_dbt project as an Airflow DAG, one task per dbt model."""
from datetime import datetime

from cosmos import DbtDag, ProfileConfig, ProjectConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping

profile_config = ProfileConfig(
    profile_name="data_vault_dbt",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id="postgres_data_vault",
        profile_args={"schema": "data_vault"},
    ),
)

data_vault_dag = DbtDag(
    dag_id="data_vault_dbt",
    project_config=ProjectConfig("/opt/airflow/dbt/data_vault_dbt"),
    profile_config=profile_config,
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
)
