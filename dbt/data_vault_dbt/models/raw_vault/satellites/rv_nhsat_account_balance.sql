{{ automate_dv.sat(src_pk='account_hk',
                   src_hashdiff='account_balance_hashdiff',
                   src_payload=['online_actual_bal', 'online_cleared_bal', 'open_actual_bal',
                                'working_balance', 'prev_bal'],
                   src_extra_columns=none,
                   src_eff=none,
                   src_ldts='load_dts',
                   src_source='record_source',
                   source_model='stg_fbnk_account') }}
