{{ automate_dv.sat(src_pk='customer_hk',
                   src_hashdiff='customer_hashdiff',
                   src_payload=['short_name', 'arabic_name', 'birth_incorp_date', 'id_type', 'id_number',
                                'nationality', 'sector', 'opening_date', 'account_officer'],
                   src_extra_columns=none,
                   src_eff=none,
                   src_ldts='load_dts',
                   src_source='record_source',
                   source_model='stg_fbnk_customer') }}
