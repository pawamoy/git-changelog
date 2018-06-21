{%- if version.previous_version -%}
{%- if version.date -%}
[{{ version.tag }}]: {{ gitolog.compare_url }}{{ version.previous_version.tag }}...{{ version.tag}}
{%- else -%}
[{{ version.tag }}]: {{ gitolog.compare_url }}{{ version.previous_version.tag }}...HEAD
{% endif -%}
{%- endif -%}