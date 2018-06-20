This is my changelog

{% for commit in commits -%}
  {% include 'commit.md' with context %}
{% endfor %}
