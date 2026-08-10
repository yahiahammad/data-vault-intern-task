{{ automate_dv.sat(src_pk='customer_hk',
                   src_hashdiff='customer_status_hashdiff',
                   src_payload=['customer_status', 'risk_rate', 'drmnt_code', 'drmnt_date',
                                'posting_restrict_1', 'posting_restrict_2', 'peps'],
                   src_extra_columns=none,
                   src_eff=none,
                   src_ldts='load_dts',
                   src_source='record_source',
                   source_model='stg_fbnk_customer') }}
