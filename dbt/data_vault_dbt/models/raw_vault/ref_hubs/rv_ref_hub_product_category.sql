with codes as (
    select category as product_category, load_dts, record_source
    from {{ ref('stg_fbnk_account') }}
    where category is not null and category != ''

    union all

    select product_category, load_dts, record_source
    from {{ ref('stg_fbnk_stmt_entry') }}
    where product_category is not null and product_category != ''
)

select
    product_category,
    min(load_dts) as load_dts,
    min(record_source) as record_source
from codes
group by product_category
