-- Every product_category observed in the data must have a description in the seed.
select h.product_category
from {{ ref('rv_ref_hub_product_category') }} h
left join {{ ref('rv_ref_sat_product_category') }} s
    on s.product_category = h.product_category
where s.product_category is null
