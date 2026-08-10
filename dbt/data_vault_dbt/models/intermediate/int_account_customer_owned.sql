-- Accounts that have a real owning customer (excludes internal bank accounts).
select *
from {{ ref('stg_fbnk_account') }}
where customer_id is not null and customer_id != ''
