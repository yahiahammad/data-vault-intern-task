{{ automate_dv.sat(src_pk='customer_hk',
                   src_hashdiff='customer_staff_hashdiff',
                   src_payload=['emploee_no'],
                   src_extra_columns=none,
                   src_eff='created_ts',
                   src_ldts='load_dts',
                   src_source='record_source',
                   source_model='int_customer_staff_present') }}
