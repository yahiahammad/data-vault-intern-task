{{ config(materialized='view') }}

{%- set yaml_metadata -%}
source_model:
  raw: "fbnk_stmt_entry"

derived_columns:
  stmt_entry_id: "recid"
  branch_id: "company_code"
  load_dts: "cast(current_timestamp as timestamp)"
  record_source: "concat(source_system, '.', source_table)"

hashed_columns:
  stmt_entry_hk: "stmt_entry_id"
  account_hk: "account_number"
  customer_hk: "customer_id"
  branch_hk: "branch_id"
  stmt_entry_detail_hashdiff:
    is_hashdiff: true
    columns:
      - "stmt_entry_id"
      - "transaction_code"
      - "product_category"
      - "currency"
      - "amount_lcy"
      - "amount_fcy"
      - "exchange_rate"
      - "booking_date"
      - "value_date"
      - "processing_date"
      - "exposure_date"
      - "system_date_time"
      - "our_reference"
      - "their_reference"
      - "trans_reference"
      - "reversal_marker"
      - "narrative"
      - "cheque_number"
      - "chq_type"
      - "counterparty"
      - "account_officer"
      - "position_type"
      - "system_id"
{%- endset -%}

{% set metadata_dict = fromyaml(yaml_metadata) %}

{{ automate_dv.stage(include_source_columns=true,
                     source_model=metadata_dict['source_model'],
                     derived_columns=metadata_dict['derived_columns'],
                     null_columns=none,
                     hashed_columns=metadata_dict['hashed_columns'],
                     ranked_columns=none) }}
