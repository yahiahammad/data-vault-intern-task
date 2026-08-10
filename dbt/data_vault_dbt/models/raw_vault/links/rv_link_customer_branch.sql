{{ automate_dv.link(src_pk='customer_branch_hk',
                    src_fk=['customer_hk', 'branch_hk'],
                    src_ldts='load_dts',
                    src_source='record_source',
                    source_model='int_customer_branch_present') }}
