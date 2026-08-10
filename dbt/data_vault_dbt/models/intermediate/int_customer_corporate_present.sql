-- Customer versions that carry corporate-only attributes.
select *
from {{ ref('stg_fbnk_customer') }}
where commercial_registration_no is not null and commercial_registration_no != ''
