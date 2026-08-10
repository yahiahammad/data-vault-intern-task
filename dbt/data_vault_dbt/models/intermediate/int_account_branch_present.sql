-- Accounts with a known branch/company code.
select *
from {{ ref('stg_fbnk_account') }}
where branch_id is not null and branch_id != ''
