-- The unknown-member ghost record ('-1'), unioned into rv_hub_customer so that
-- link FKs carrying the ghost key -- currently rv_nhlink_stmt_entry, for
-- internal contra-account entries with no customer -- resolve to a real hub
-- row instead of dangling, keeping the relationships tests unscoped.
--
-- Derived from stg_fbnk_stmt_entry (where the substitution happens) rather than
-- hardcoded, but filtered to '-1' on purpose: feeding the whole staging model
-- into the hub would auto-create a hub row for any customer seen in a statement
-- entry, silently defeating the referential-gap detection rv_hub_customer
-- documents as intentional.
select distinct
    customer_hk,
    customer_id,
    load_dts,
    record_source
from {{ ref('stg_fbnk_stmt_entry') }}
where customer_id = '-1'
