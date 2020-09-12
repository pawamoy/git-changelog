{% if not inplace -%}
# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

{% endif %}<!-- insertion marker -->
{% macro render_commit(commit) -%}
- {{ commit.style.subject|default(commit.subject) }} ([{{ commit.hash|truncate(7, True, '') }}]({{ commit.url }}) by {{ commit.author_name }}).
{%- if commit.text_refs.issues_not_in_subject %} References: {% for issue in commit.text_refs.issues_not_in_subject -%}
{% if issue.url %}[{{ issue.ref }}]({{ issue.url }}){%else %}{{ issue.ref }}{% endif %}{% if not loop.last %}, {% endif -%}
{%- endfor -%}{%- endif -%}
{%- endmacro -%}

{%- macro render_section(section) -%}
### {{ section.type or "Misc" }}
{% for commit in section.commits|sort(attribute='author_date',reverse=true)|unique(attribute='subject') -%}
{{ render_commit(commit) }}
{% endfor %}
{%- endmacro -%}

{%- macro render_version(version) -%}
{%- if version.tag or version.planned_tag -%}
## [{{ version.tag or version.planned_tag }}]({{ version.url }}){% if version.date %} - {{ version.date }}{% endif %}

<small>[Compare with {{ version.previous_version.tag|default("first commit") }}]({{ version.compare_url }})</small>
{%- else -%}
## Unrealeased

<small>[Compare with latest]({{ version.compare_url }})</small>
{%- endif %}

{% for type, section in version.sections_dict|dictsort -%}
{%- if type and type in changelog.style.DEFAULT_RENDER -%}
{{ render_section(section) }}
{% endif -%}
{%- endfor -%}
{%- endmacro -%}

{% for version in changelog.versions_list -%}
{{ render_version(version) }}
{%- endfor -%}
