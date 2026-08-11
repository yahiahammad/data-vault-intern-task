{#- int_customer_ghost contributes the single unknown-member row ('-1') so that
   link FKs carrying the ghost key resolve to a real hub row. Everything else
   comes from fbnk_customer, the only authoritative source of customers. -#}
{{ automate_dv.hub(src_pk='customer_hk',
                   src_nk='customer_id',
                   src_ldts='load_dts',
                   src_source='record_source',
                   source_model=['stg_fbnk_customer', 'int_customer_ghost']) }}
