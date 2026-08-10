with codes as (
    select account_officer, load_dts, record_source
    from {{ ref('stg_fbnk_customer') }}
    where account_officer is not null and account_officer != ''

    union all

    select account_officer, load_dts, record_source
    from {{ ref('stg_fbnk_account') }}
    where account_officer is not null and account_officer != ''

    union all

    select account_officer, load_dts, record_source
    from {{ ref('stg_fbnk_stmt_entry') }}
    where account_officer is not null and account_officer != ''
)

select
    account_officer,
    min(load_dts) as load_dts,
    min(record_source) as record_source
from codes
group by account_officer
