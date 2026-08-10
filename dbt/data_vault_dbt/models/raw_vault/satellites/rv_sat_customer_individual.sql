{{ automate_dv.sat(src_pk='customer_hk',
                   src_hashdiff='customer_individual_hashdiff',
                   src_payload=['genders', 'nat_security_number', 'profession'],
                   src_extra_columns=none,
                   src_eff='created_ts',
                   src_ldts='load_dts',
                   src_source='record_source',
                   source_model='int_customer_individual_present') }}
