select
    cast(transaction_code as text) as transaction_code,
    load_dts,
    {{ hash_key(['description']) }} as hashdiff,
    description,
    record_source
from {{ ref('stg_seed_transaction_code') }}
