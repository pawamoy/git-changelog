{%- if version.tag or version.planned_tag -%}
## [{{ version.tag or version.planned_tag }}]({{ version.url }}){% if version.date %} - {{ version.date }}{% endif %}

<small>[Compare with {{ version.previous_version.tag|default("first commit") }}]({{ version.compare_url }})</small>
{%- else -%}
## Unreleased

<small>[Compare with latest]({{ version.compare_url }})</small>
{%- endif %}

{% for type in changelog.style.DEFAULT_RENDER %}
{%- if type in version.sections_dict -%}
{%- with section = version.sections_dict[type] -%}
{% include 'section.md' with context %}
{%- endwith -%}
{%- endif -%}
{%- endfor -%}
