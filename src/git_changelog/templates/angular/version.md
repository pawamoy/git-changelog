{%- if version.tag or version.planned_tag -%}
<a name="{{ version.tag or version.planned_tag }}"></a>
## [{{ version.tag or version.planned_tag }}]({{ version.compare_url }})
{%- else -%}
<a name="Unrealeased"></a>
## Unrealeased ([compare]({{ version.compare_url }}))
{%- endif -%}
{% if version.date %} ({{ version.date }}){% endif %}

{% for type, section in version.sections_dict|dictsort -%}
{%- if type -%}
{% include 'section.md' with context %}
{% endif -%}
{%- endfor -%}
