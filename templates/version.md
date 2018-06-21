## [{{ version.tag }}]{% if version.date %} - {{ version.date }}{% endif %}

{% for type, section in version.sections_dict|dictsort -%}
{%- if type and type != 'Merged' -%}
{% include 'section.md' with context %}
{% endif -%}
{%- endfor -%}
{%- if version.untyped_section -%}
{%- with section = version.untyped_section -%}
{% include 'section.md' with context %}
{% endwith -%}
{%- endif -%}
