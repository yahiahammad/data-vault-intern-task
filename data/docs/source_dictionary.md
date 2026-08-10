# Source Dictionary

Column meanings for the three supplied tables. These are trimmed extracts of
real T24 tables. The real tables have several hundred columns each; the
columns kept here are the ones that carry a design decision.

Read this next to the CSV files, not instead of them.

## T24 conventions that apply to all three tables

| Convention | Meaning |
|------------|---------|
| recid | The record identifier in T24. It is not always the business key on its own. |
| curr_no | Current version number of the record in T24. It increments on every amendment. |
| Dates as YYYYMMDD strings | T24 stores dates as 8 character strings, not date types. |
| Timestamps as YYMMDDHHMM strings | 10 character strings. 2601121032 is 2026-01-12 10:32. |
| Empty string vs null | The extract writes both as empty CSV fields. Treat them as unknown. |
| Multi-value fields | T24 stores repeating values in one field. In this extract they have already been split into numbered columns such as telephone_1 and telephone_2. |
| inputter and authoriser | The user who entered and the user who approved the record version. T24 enforces separation between them. |

## Metadata columns present on all three tables

These are added by the ingestion layer, not by T24.

| Column | Meaning |
|--------|---------|
| source_system | Always t24 in this extract. |
| source_table | The source table name. |
| ingested_ts | When the ingestion job wrote the row. Same for every row in a batch. |
| created_ts | The business timestamp of the record version in the source. |
| created_dt | Partition date derived from created_ts. |

## fbnk_customer

One row per customer version. A customer with three amendments has three rows.

| Column | Meaning | Note |
|--------|---------|------|
| recid | Customer identifier followed by a version suffix, such as 100123;3 | The part before the semicolon is the customer number |
| curr_no | Version number of this record | Matches the suffix in recid |
| short_name | Customer name in English | Personal name for individuals, trading name for companies |
| arabic_name | Customer name in Arabic | |
| genders | M or F | Empty for corporate customers |
| birth_incorp_date | Date of birth for individuals, date of incorporation for companies | One row in the data has a value that is not a real date |
| nat_security_number | National identity number | Empty for corporate customers |
| id_type | Type of identity document, NATID or COMMREG | |
| id_number | Identity document number | Repeats nat_security_number for individuals |
| nationality | Two letter country code | |
| sector | Economic sector code | See reference_codes.md |
| profession | Profession code | Empty for corporate customers |
| customer_status | Customer status code | See reference_codes.md |
| risk_rate | Risk rating code, 1 to 3 | See reference_codes.md |
| account_officer | Employee code of the relationship officer | |
| company_book | Booking company or branch code | |
| emploee_no | Employee number when the customer is also a member of bank staff | Spelling is as in the source. Populated for a minority of customers |
| telephone_1, telephone_2 | Landline numbers | A customer may have zero, one, or two |
| sms_1 | Mobile number used for SMS | |
| email_address, email_1 | Email addresses | A customer may have zero, one, or two |
| drmnt_code | Dormancy code | Empty when the customer is not dormant. See reference_codes.md |
| drmnt_date | Date the customer became dormant | Empty when not dormant |
| posting_restrict_1, posting_restrict_2 | Posting restriction codes applied to the customer | See reference_codes.md |
| peps | YES or NO, politically exposed person flag | |
| commercial_registration_no | Commercial register number | Corporate customers only |
| licence_expiry_date | Trade licence expiry date | Corporate customers only |
| opening_date | Date the customer relationship started | Does not change across versions |
| update_date | Date this version was written | Changes on every version |

## fbnk_account

One row per account version. Note that the versioning pattern here is not the
same as fbnk_customer. Confirm this from the data before you design.

| Column | Meaning | Note |
|--------|---------|------|
| recid | Account number | |
| curr_no | Version number of this record | |
| customer | Customer number that owns the account | Empty for internal bank accounts |
| category | Product category code | See reference_codes.md |
| currency | Account currency, three letter code | |
| opening_date | Account opening date | |
| closure_date | Account closure date | Empty for open accounts |
| short_title, account_title_1 | Account title in English | |
| arabic_title | Account title in Arabic | |
| alt_acct_id_1, alt_acct_id_2 | Alternative identifiers for the account | |
| alt_acct_type_1, alt_acct_type_2 | Type of the matching alternative identifier, IBAN or OLDACC | Pairs positionally with alt_acct_id_n |
| account_officer | Employee code of the account officer | |
| co_code | Branch or company code currently holding the account | |
| limit_ref | Credit limit reference | Empty when the account has no limit |
| online_actual_bal | Current balance including uncleared items | Changes constantly |
| online_cleared_bal | Current balance of cleared items only | Changes constantly |
| open_actual_bal | Balance at the start of the current business day | Changes daily |
| working_balance | Balance used for availability checks | Changes constantly |
| prev_bal | Balance at the previous update | Changes constantly |
| record_status | CLOSED or empty | |
| closed_online | Y or empty | |
| inactiv_marker | Y when the account is flagged inactive, otherwise empty | |
| posting_restrict | Posting restriction code applied to the account | See reference_codes.md |
| date_last_update | Date of the last change to this account record | |

## fbnk_stmt_entry

One row per accounting entry. T24 posts double entry, so a single business
transaction usually appears as two rows sharing one our_reference: one on the
customer account and one on a contra account.

Statement entries are never amended in place. A mistake is corrected by
posting a reversal entry.

The statement entry extract is a sample. The balances on fbnk_account are
point in time snapshots taken when that account version was written. Do not
expect the entries in this extract to add up to those balances.

| Column | Meaning | Note |
|--------|---------|------|
| recid | Statement entry identifier | Unique per entry, no version suffix |
| account_number | Account the entry was posted to | |
| customer_id | Customer the entry was posted for | Empty when the account is an internal bank account. In at least one row it does not match the customer currently shown on the account |
| product_category | Product category of the account at posting time | |
| transaction_code | Transaction type code | See reference_codes.md |
| currency | Currency of the entry | |
| amount_lcy | Amount in local currency, negative for debit and positive for credit | |
| amount_fcy | Amount in the account currency when the account is not in local currency | Empty for local currency entries |
| exchange_rate | Rate used to convert between the two | Empty for local currency entries |
| booking_date | Date the entry was booked | |
| value_date | Date the entry affects interest calculation | Can differ from booking_date, for example cheque clearing |
| processing_date | T24 processing date | |
| exposure_date | Date used for exposure reporting | |
| system_date_time | Timestamp the entry was created, YYMMDDHHMM | |
| our_reference | Bank transaction reference | Shared by both legs of a double entry |
| their_reference | Customer or counterparty reference | Often empty |
| trans_reference | Reference to the original entry when this entry is a reversal | Empty otherwise |
| reversal_marker | R when this entry reverses another, otherwise empty | |
| narrative | Free text description | |
| cheque_number, chq_type | Cheque details | Populated for cheque transactions only |
| counterparty | Other account or party in the transaction | Often empty |
| account_officer | Employee code of the officer | |
| company_code | Branch or company code that booked the entry | |
| position_type | Accounting position type | |
| system_id | T24 subsystem that generated the entry, such as TT, FT, CQ, IC, CH | |

## Things to look for while profiling

This list is deliberately not exhaustive. Finding what is not on it is part
of the task.

- Which columns are empty for every row, and which are empty only for a
  specific kind of customer or account.
- Which columns change between two versions of the same entity and which
  never change.
- Whether any entity appears with two versions where nothing meaningful
  changed.
- How many distinct values of each identifier column there are, compared to
  the row count.
- Whether every foreign key value in one table exists in the other.
