-- Composite primary key (account_hk, load_dts) must be unique.
select account_hk, load_dts, count(*) as row_count
from {{ ref('rv_sat_account_alt') }}
group by account_hk, load_dts
having count(*) > 1
