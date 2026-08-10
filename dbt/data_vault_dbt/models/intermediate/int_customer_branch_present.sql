-- Customers with a known branch/company code.
select *
from {{ ref('stg_fbnk_customer') }}
where branch_id is not null and branch_id != ''
