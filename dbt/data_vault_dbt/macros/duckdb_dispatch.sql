{#-
  AutomateDV (dbtvault) 0.11.5 only ships platform macros for Snowflake,
  BigQuery, Databricks, Postgres, and SQL Server. Most of its dispatched
  macros fall back to a `default__` implementation when no adapter-specific
  one exists, so DuckDB gets those for free. get_escape_characters is one
  of the few with no default -- DuckDB uses standard double-quote
  identifier escaping, same as Postgres, so this is a direct copy of
  automate_dv's postgres__get_escape_characters.
  See dispatch: config in dbt_project.yml for how dbt finds this.
-#}
{%- macro duckdb__get_escape_characters() %}
    {%- do return (('"', '"')) -%}
{%- endmacro %}

{%- macro duckdb__cast_date(column_str, as_string=false, alias=none) -%}
    {%- if as_string -%}
    CAST('{{ column_str }}' AS DATE)
    {%- else -%}
    CAST({{ column_str }} AS DATE)
    {%- endif -%}
    {%- if alias %} AS {{ alias }} {%- endif -%}
{%- endmacro -%}

{%- macro duckdb__cast_datetime(column_str, as_string=false, alias=none, date_type=none) -%}
    CAST({{ column_str }} AS TIMESTAMP)
    {%- if alias %} AS {{ alias }} {%- endif -%}
{%- endmacro -%}

{#- default__type_binary emits BINARY(16), a Snowflake/SQL Server sized-binary
    type DuckDB doesn't have -- DuckDB's binary type is just BLOB. -#}
{%- macro duckdb__type_binary(for_dbt_compare=false) -%}
    BLOB
{%- endmacro -%}

{#- default__hash_alg_md5 emits MD5_BINARY(...), a Snowflake-only function.
    DuckDB's md5() returns a hex VARCHAR like Postgres's does; unhex() is
    DuckDB's equivalent of Postgres's decode(x, 'hex') to get back to BLOB. -#}
{%- macro duckdb__hash_alg_md5() -%}
    {%- do return("UNHEX(MD5([HASH_STRING_PLACEHOLDER]))") -%}
{%- endmacro %}
