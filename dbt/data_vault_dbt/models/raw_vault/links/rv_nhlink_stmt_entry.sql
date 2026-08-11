{#- customer_hk is an FK here even though internal contra-account entries have
   no customer: stg_fbnk_stmt_entry substitutes the unknown-member business key
   '-1' before hashing, so those rows carry the ghost key rather than NULL and
   survive link() (which drops any row with a NULL FK). Without that this link
   would cover 19 of 30 entries.

   Note customer here is NOT derivable from rv_link_customer_account: an
   entry's customer can differ from the account's registered owner (e.g.
   STE00000025 on account 1010100100130, owner 100130, booked to 100126) --
   read as a joint holder the current extract has no column for. -#}
{{ automate_dv.link(src_pk='stmt_entry_hk',
                    src_fk=['account_hk', 'branch_hk', 'customer_hk'],
                    src_ldts='load_dts',
                    src_source='record_source',
                    source_model='stg_fbnk_stmt_entry') }}
