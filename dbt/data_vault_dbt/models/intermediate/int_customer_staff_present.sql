-- Customer versions where the customer is also a member of bank staff.
select *
from {{ ref('stg_fbnk_customer') }}
where emploee_no is not null and emploee_no != ''
