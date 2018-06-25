{%- if version.tag -%}
<a name="{{ version.tag }}"></a>
## [{{ version.tag }}]({{ version.compare_url }})
{%- else -%}
<a name="{{ version.planned_tag or "Unrealeased" }}"></a>
## {{ version.planned_tag or "Unrealeased" }} ([compare]({{ version.compare_url }})){%- endif -%}{% if version.date %} ({{ version.date }}){% endif %}

{% for type, section in version.sections_dict|dictsort -%}
{%- if type and type != 'Merged' -%}
{% include 'angular/section.md' with context %}
{% endif -%}
{%- endfor -%}
