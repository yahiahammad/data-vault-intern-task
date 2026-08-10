-- Statement entries with a known branch/company code.
select *
from {{ ref('stg_fbnk_stmt_entry') }}
where branch_id is not null and branch_id != ''
