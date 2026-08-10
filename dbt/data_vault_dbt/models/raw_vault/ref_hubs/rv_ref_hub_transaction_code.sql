select
    transaction_code,
    min(load_dts) as load_dts,
    min(record_source) as record_source
from {{ ref('stg_fbnk_stmt_entry') }}
where transaction_code is not null and transaction_code != ''
group by transaction_code
