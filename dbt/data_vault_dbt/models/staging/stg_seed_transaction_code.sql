{{ config(materialized='view') }}

{%- set yaml_metadata -%}
source_model: "seed_transaction_code"

derived_columns:
  load_dts: "cast('1900-01-01' as timestamp)"
  record_source: "'seed.reference_codes'"
{%- endset -%}

{% set metadata_dict = fromyaml(yaml_metadata) %}

{{ automate_dv.stage(include_source_columns=true,
                     source_model=metadata_dict['source_model'],
                     derived_columns=metadata_dict['derived_columns'],
                     null_columns=none,
                     hashed_columns=none,
                     ranked_columns=none) }}
