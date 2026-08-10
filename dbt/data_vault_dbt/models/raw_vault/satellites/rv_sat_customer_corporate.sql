{{ automate_dv.sat(src_pk='customer_hk',
                   src_hashdiff='customer_corporate_hashdiff',
                   src_payload=['commercial_registration_no', 'licence_expiry_date'],
                   src_extra_columns=none,
                   src_eff='created_ts',
                   src_ldts='load_dts',
                   src_source='record_source',
                   source_model='int_customer_corporate_present') }}
