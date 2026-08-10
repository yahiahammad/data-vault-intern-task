{#- customer_hk is deliberately not a link FK: it's null for internal-account
   entries, and automate_dv's link() drops any row with a null FK (correct
   DV2.0 behaviour - links never carry an optional relationship). The
   customer for an entry is derivable via rv_link_customer_account instead. -#}
{{ automate_dv.link(src_pk='stmt_entry_hk',
                    src_fk=['account_hk', 'branch_hk'],
                    src_ldts='load_dts',
                    src_source='record_source',
                    source_model='stg_fbnk_stmt_entry') }}
