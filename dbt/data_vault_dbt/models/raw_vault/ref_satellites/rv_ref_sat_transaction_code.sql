select
    cast(transaction_code as text) as transaction_code,
    cast('1900-01-01' as timestamp) as load_dts,
    {{ hash_key(['description']) }} as hashdiff,
    description,
    'seed.reference_codes' as record_source
from {{ ref('seed_transaction_code') }}
