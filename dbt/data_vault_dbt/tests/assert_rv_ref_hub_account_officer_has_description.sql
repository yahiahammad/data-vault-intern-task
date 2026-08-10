-- Every account_officer code observed in the data must have a description in the seed.
select h.account_officer
from {{ ref('rv_ref_hub_account_officer') }} h
left join {{ ref('rv_ref_sat_account_officer') }} s
    on s.account_officer = h.account_officer
where s.account_officer is null
