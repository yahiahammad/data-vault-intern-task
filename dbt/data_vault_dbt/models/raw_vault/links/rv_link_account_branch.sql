{{ automate_dv.link(src_pk='account_branch_hk',
                    src_fk=['account_hk', 'branch_hk'],
                    src_ldts='load_dts',
                    src_source='record_source',
                    source_model='int_account_branch_present') }}
