select
    cast(account_officer as text) as account_officer,
    load_dts,
    {{ hash_key(['description']) }} as hashdiff,
    description,
    record_source
from {{ ref('stg_seed_account_officer') }}
