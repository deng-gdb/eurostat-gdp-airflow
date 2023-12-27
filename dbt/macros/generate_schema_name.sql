{% macro generate_schema_name(custom_schema_name, node) %}

    {% set default_schema = target.schema ~ '_'~ target.name %}

    {% if custom_schema_name is none or target.name == 'sandbox' or target.name == 'dev' %}

        {{ default_schema }}

    {% else %}

        {{ default_schema }}_{{ custom_schema_name | trim }}

    {% endif %}

{% endmacro %}