-- Composite primary key (customer_hk, load_dts) must be unique.
select customer_hk, load_dts, count(*) as row_count
from {{ ref('rv_sat_customer_staff') }}
group by customer_hk, load_dts
having count(*) > 1
