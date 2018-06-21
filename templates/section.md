### {{ section.type or "Misc" }}
{% for commit in section.commits -%}
{% include 'commit.md' with context %}
{% endfor %}
