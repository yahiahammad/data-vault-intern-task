-- Composite primary key (customer_hk, load_dts, created_ts) must be unique.
-- created_ts (src_eff) breaks ties when >1 real version of the same key lands in one load batch.
select customer_hk, load_dts, created_ts, count(*) as row_count
from {{ ref('rv_sat_customer_corporate') }}
group by customer_hk, load_dts, created_ts
having count(*) > 1
