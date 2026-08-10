{{ config(materialized='view') }}

{%- set yaml_metadata -%}
source_model:
  raw: "fbnk_customer"

derived_columns:
  customer_id: "split_part(recid, ';', 1)"
  branch_id: "company_book"
  load_dts: "cast(current_timestamp as timestamp)"
  record_source: "concat(source_system, '.', source_table)"

hashed_columns:
  customer_hk: "customer_id"
  branch_hk: "branch_id"
  customer_branch_hk:
    - "customer_id"
    - "branch_id"
  customer_hashdiff:
    is_hashdiff: true
    columns:
      - "short_name"
      - "arabic_name"
      - "birth_incorp_date"
      - "id_type"
      - "id_number"
      - "nationality"
      - "sector"
      - "opening_date"
      - "account_officer"
  customer_individual_hashdiff:
    is_hashdiff: true
    columns:
      - "genders"
      - "nat_security_number"
      - "profession"
  customer_corporate_hashdiff:
    is_hashdiff: true
    columns:
      - "commercial_registration_no"
      - "licence_expiry_date"
  customer_status_hashdiff:
    is_hashdiff: true
    columns:
      - "customer_status"
      - "risk_rate"
      - "drmnt_code"
      - "drmnt_date"
      - "posting_restrict_1"
      - "posting_restrict_2"
      - "peps"
  customer_staff_hashdiff:
    is_hashdiff: true
    columns:
      - "emploee_no"
  customer_contact_hashdiff:
    is_hashdiff: true
    columns:
      - "telephone_1"
      - "telephone_2"
      - "sms_1"
      - "email_address"
      - "email_1"
{%- endset -%}

{% set metadata_dict = fromyaml(yaml_metadata) %}

{{ automate_dv.stage(include_source_columns=true,
                     source_model=metadata_dict['source_model'],
                     derived_columns=metadata_dict['derived_columns'],
                     null_columns=none,
                     hashed_columns=metadata_dict['hashed_columns'],
                     ranked_columns=none) }}
