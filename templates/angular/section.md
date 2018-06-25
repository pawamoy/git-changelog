### {{ section.type or "Misc" }}
{% for commit in section.commits|sort(attribute='subject') -%}
{% include 'angular/commit.md' with context %}
{% endfor %}
