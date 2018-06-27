{% for version in changelog.versions_list -%}
{% include 'version.md' with context %}
{% endfor -%}
