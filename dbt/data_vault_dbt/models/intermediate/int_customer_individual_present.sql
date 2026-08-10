-- Customer versions that carry individual-only attributes (non-corporate).
select *
from {{ ref('stg_fbnk_customer') }}
where genders is not null and genders != ''
