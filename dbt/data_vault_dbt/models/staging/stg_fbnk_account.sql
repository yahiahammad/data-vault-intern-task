{{ config(materialized='view') }}

{%- set yaml_metadata -%}
source_model:
  raw: "fbnk_account"

derived_columns:
  account_number: "recid"
  customer_id: "customer"
  branch_id: "co_code"
  load_dts: "cast(created_ts as timestamp)"
  record_source: "concat(source_system, '.', source_table)"

hashed_columns:
  account_hk: "account_number"
  customer_hk: "customer_id"
  branch_hk: "branch_id"
  customer_account_hk:
    - "customer_id"
    - "account_number"
  account_branch_hk:
    - "account_number"
    - "branch_id"
  account_detail_hashdiff:
    is_hashdiff: true
    columns:
      - "short_title"
      - "account_title_1"
      - "arabic_title"
      - "category"
      - "currency"
      - "opening_date"
      - "closure_date"
      - "record_status"
      - "closed_online"
      - "inactiv_marker"
      - "posting_restrict"
      - "limit_ref"
      - "account_officer"
  account_balance_hashdiff:
    is_hashdiff: true
    columns:
      - "online_actual_bal"
      - "online_cleared_bal"
      - "open_actual_bal"
      - "working_balance"
      - "prev_bal"
  account_alt_hashdiff:
    is_hashdiff: true
    columns:
      - "alt_acct_id_1"
      - "alt_acct_type_1"
      - "alt_acct_id_2"
      - "alt_acct_type_2"
{%- endset -%}

{% set metadata_dict = fromyaml(yaml_metadata) %}

{{ automate_dv.stage(include_source_columns=true,
                     source_model=metadata_dict['source_model'],
                     derived_columns=metadata_dict['derived_columns'],
                     null_columns=none,
                     hashed_columns=metadata_dict['hashed_columns'],
                     ranked_columns=none) }}
