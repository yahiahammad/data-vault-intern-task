select
    cast(product_category as text) as product_category,
    load_dts,
    {{ hash_key(['description']) }} as hashdiff,
    description,
    record_source
from {{ ref('stg_seed_product_category') }}
