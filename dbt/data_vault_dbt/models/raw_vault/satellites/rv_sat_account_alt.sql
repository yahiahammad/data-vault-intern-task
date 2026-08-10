{{ automate_dv.sat(src_pk='account_hk',
                   src_hashdiff='account_alt_hashdiff',
                   src_payload=['alt_acct_id_1', 'alt_acct_type_1', 'alt_acct_id_2', 'alt_acct_type_2'],
                   src_extra_columns=none,
                   src_eff=none,
                   src_ldts='load_dts',
                   src_source='record_source',
                   source_model='int_account_alt_present') }}
