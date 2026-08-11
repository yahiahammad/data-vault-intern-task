{#-
  The "unknown member" ghost key: hash of the sentinel business key '-1'.

  Used where a link FK is structurally absent rather than merely unknown --
  currently internal contra-account statement entries, which have no customer.
  Substituting this keeps those rows in the link (automate_dv's link() drops
  any row with a NULL FK) instead of silently losing them.

  Hashed the same way automate_dv hashes any single business key
  (UNHEX(MD5(UPPER(TRIM(...)))) -- '-1' is unaffected by upper/trim), so it is
  indistinguishable in type and width from a real customer_hk.

  int_customer_ghost unions a matching row into rv_hub_customer, so FKs
  carrying this key resolve to a real hub row and relationships tests stay
  unscoped. The trade-off: rv_hub_customer holds 11 rows for 10 real
  customers, so counts of customers need `where customer_id <> '-1'`.
-#}
{% macro unknown_hk() -%}
    unhex(md5('-1'))
{%- endmacro %}
