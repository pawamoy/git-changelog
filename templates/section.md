### {{ section.type or "Misc" }}
{% for commit in section.commits|sort(attribute='subject') -%}
{% include 'commit.md' with context %}
{% endfor %}
