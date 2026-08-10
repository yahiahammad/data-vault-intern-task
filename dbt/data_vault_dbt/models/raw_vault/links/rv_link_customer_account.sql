{{ automate_dv.link(src_pk='customer_account_hk',
                    src_fk=['customer_hk', 'account_hk'],
                    src_ldts='load_dts',
                    src_source='record_source',
                    source_model='int_account_customer_owned') }}
