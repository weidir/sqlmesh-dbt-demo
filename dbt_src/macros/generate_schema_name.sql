-- This is a custom macro taken from https://docs.getdbt.com/docs/build/custom-schemas#how-does-dbt-generate-a-models-schema-name
-- Essentially this macro changes the default schema naming convention to remove the prepended default schema name

-- Code that has been changed:
-- NEW: {{ custom_schema_name | trim }}
-- OLD: {{ default_schema }}_{{ custom_schema_name | trim }}

{% macro generate_schema_name(custom_schema_name, node) -%}

    {%- set default_schema = target.schema -%}
    {%- if custom_schema_name is none -%}

        {{ default_schema }}

    {%- else -%}

        {{ custom_schema_name | trim }}

    {%- endif -%}

{%- endmacro %}