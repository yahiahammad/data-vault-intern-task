-- Every transaction_code observed in the data must have a description in the seed.
select h.transaction_code
from {{ ref('rv_ref_hub_transaction_code') }} h
left join {{ ref('rv_ref_sat_transaction_code') }} s
    on s.transaction_code = h.transaction_code
where s.transaction_code is null
