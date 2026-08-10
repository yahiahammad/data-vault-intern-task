-- Account versions that carry an alternative account identifier.
select *
from {{ ref('stg_fbnk_account') }}
where alt_acct_id_1 is not null and alt_acct_id_1 != ''
