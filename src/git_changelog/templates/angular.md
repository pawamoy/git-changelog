<!-- insertion marker -->
{% macro render_commit(commit) -%}
- {% if commit.style.scope %}**{{ commit.style.scope }}:** {% endif %}{{ commit.style.subject }} ([{{ commit.hash|truncate(7, True, '') }}]({{ commit.url }}))
{%- if commit.text_refs.issues_not_in_subject %}, related to {% for issue in commit.text_refs.issues_not_in_subject -%}
[{{ issue.ref }}]({{ issue.url }}){% if not loop.last %}, {% endif -%}
{%- endfor -%}{%- endif -%}
{%- endmacro -%}

{%- macro render_section(section) -%}
### {{ section.type or "Misc" }}
{% for commit in section.commits|sort(attribute='subject') -%}
{{ render_commit(commit) }}
{% endfor %}
{%- endmacro -%}

{%- macro render_version(version) -%}
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
{{ render_section(section) }}
{% endif -%}
{%- endfor -%}
{%- endmacro -%}

{% for version in changelog.versions_list -%}
{{ render_version(version) }}
{%- endfor %}
