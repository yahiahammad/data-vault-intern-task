# Reference Codes

Meanings of the code values that appear in the supplied data.

You are given the meanings but you are not given the lookup tables. Deciding
whether a code deserves its own Raw Vault model, and which kind, is part of
the task.

## Sector codes, fbnk_customer.sector

| Code | Meaning |
|------|---------|
| 1001 | Corporate |
| 2001 | Retail individual |

## Customer status, fbnk_customer.customer_status

| Code | Meaning |
|------|---------|
| 1 | Active |
| 2 | Under review |
| 3 | Suspended |

## Risk rating, fbnk_customer.risk_rate

| Code | Meaning |
|------|---------|
| 1 | Low |
| 2 | Medium |
| 3 | High |

## Profession, fbnk_customer.profession

| Code | Meaning |
|------|---------|
| PROF03 | Engineer |
| PROF07 | Accountant |
| PROF12 | Teacher |
| PROF21 | Physician |

## Dormancy, fbnk_customer.drmnt_code

| Code | Meaning |
|------|---------|
| empty | Not dormant |
| 18 | Dormant, no customer initiated activity for 18 months |

## Posting restriction, fbnk_customer.posting_restrict_n and fbnk_account.posting_restrict

| Code | Meaning |
|------|---------|
| 3 | No debits allowed |
| 9 | All postings blocked |

## Product category, fbnk_account.category and fbnk_stmt_entry.product_category

| Code | Meaning |
|------|---------|
| 1001 | Current account |
| 6001 | Savings account |
| 9999 | Internal bank account |

## Transaction code, fbnk_stmt_entry.transaction_code

| Code | Meaning |
|------|---------|
| 101 | Cash deposit |
| 102 | Cash withdrawal |
| 201 | Incoming transfer |
| 202 | Outgoing transfer |
| 301 | Cheque deposit |
| 401 | Charges |
| 501 | Interest credit |
| 601 | Reversal |

## Account officer, fbnk_customer.account_officer and fbnk_account.account_officer

| Code | Meaning |
|------|---------|
| 5001 | Corporate desk officer |
| 5002 | Retail branch officer |
| 5003 | Commercial desk officer |
| 5999 | System, used for internal accounts |

## Company code, company_book and co_code and company_code

| Code | Meaning |
|------|---------|
| EG0010001 | Head office branch |
| EG0010002 | Second branch |

## Alternative account type, fbnk_account.alt_acct_type_n

| Code | Meaning |
|------|---------|
| IBAN | International bank account number |
| OLDACC | Account number in the system replaced by T24 |

## Identity document type, fbnk_customer.id_type

| Code | Meaning |
|------|---------|
| NATID | National identity card |
| COMMREG | Commercial register document |
