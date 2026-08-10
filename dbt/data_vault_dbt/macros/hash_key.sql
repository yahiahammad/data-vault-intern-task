{% macro hash_key(columns) %}
md5(upper(trim(concat_ws('||',
{%- for col in columns %}
    coalesce(cast({{ col }} as text), '')
    {%- if not loop.last -%}, {%- endif %}
{%- endfor %}
))))
{% endmacro %}
