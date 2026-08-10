{{ automate_dv.sat(src_pk='customer_hk',
                   src_hashdiff='customer_contact_hashdiff',
                   src_payload=['telephone_1', 'telephone_2', 'sms_1', 'email_address', 'email_1'],
                   src_extra_columns=none,
                   src_eff='created_ts',
                   src_ldts='load_dts',
                   src_source='record_source',
                   source_model='stg_fbnk_customer') }}
