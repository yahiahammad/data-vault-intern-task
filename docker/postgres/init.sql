-- Bootstraps the raw landing schema on first container start (fresh volume only).
-- Columns are all text: this is a raw landing zone, staging models do the casting.

CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE raw.fbnk_account (
    recid text, curr_no text, customer text, category text, currency text,
    opening_date text, closure_date text, short_title text, account_title_1 text,
    arabic_title text, alt_acct_id_1 text, alt_acct_type_1 text, alt_acct_id_2 text,
    alt_acct_type_2 text, account_officer text, co_code text, limit_ref text,
    online_actual_bal text, online_cleared_bal text, open_actual_bal text,
    working_balance text, prev_bal text, record_status text, closed_online text,
    inactiv_marker text, posting_restrict text, date_last_update text, inputter text,
    authoriser text, source_system text, source_table text, ingested_ts text,
    created_ts text, created_dt text
);
\copy raw.fbnk_account FROM '/data/fbnk_account.csv' WITH CSV HEADER

CREATE TABLE raw.fbnk_customer (
    recid text, curr_no text, short_name text, arabic_name text, genders text,
    birth_incorp_date text, nat_security_number text, id_type text, id_number text,
    nationality text, sector text, profession text, customer_status text, risk_rate text,
    account_officer text, company_book text, emploee_no text, telephone_1 text,
    telephone_2 text, sms_1 text, email_address text, email_1 text, drmnt_code text,
    drmnt_date text, posting_restrict_1 text, posting_restrict_2 text, peps text,
    commercial_registration_no text, licence_expiry_date text, opening_date text,
    update_date text, inputter text, authoriser text, source_system text,
    source_table text, ingested_ts text, created_ts text, created_dt text
);
\copy raw.fbnk_customer FROM '/data/fbnk_customer.csv' WITH CSV HEADER

CREATE TABLE raw.fbnk_stmt_entry (
    recid text, account_number text, customer_id text, product_category text,
    transaction_code text, currency text, amount_lcy text, amount_fcy text,
    exchange_rate text, booking_date text, value_date text, processing_date text,
    exposure_date text, system_date_time text, our_reference text, their_reference text,
    trans_reference text, reversal_marker text, narrative text, cheque_number text,
    chq_type text, counterparty text, account_officer text, company_code text,
    position_type text, system_id text, inputter text, authoriser text,
    source_system text, source_table text, ingested_ts text, created_ts text,
    created_dt text
);
\copy raw.fbnk_stmt_entry FROM '/data/fbnk_stmt_entry.csv' WITH CSV HEADER
