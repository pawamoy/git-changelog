## [{{ version.tag or version.planned_tag or "Unrealeased" }}]({{ gitolog.compare_url }}
  {%- if version.previous_version -%}
    {{- version.previous_version.tag -}}
  {%- else -%}
    {{- (version.commits|last).hash -}}
  {%- endif -%}
  ...{{ version.tag or "HEAD" }}){% if version.date %} - {{ version.date }}{% endif %}

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
