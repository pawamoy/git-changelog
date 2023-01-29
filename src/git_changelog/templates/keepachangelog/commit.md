- {{ commit.style.subject|default(commit.subject) }} ([{{ commit.hash|truncate(7, True, '') }}]({{ commit.url }}) by {{ commit.author_name }}).
{%- if commit.text_refs.issues_not_in_subject %} Related issues/PRs: {% for issue in commit.text_refs.issues_not_in_subject -%}
{% if issue.url %}[{{ issue.ref }}]({{ issue.url }}){% else %}{{ issue.ref }}{% endif %}{% if not loop.last %}, {% endif -%}
{%- endfor -%}{%- endif -%}
{%- for trailer_name, trailer_value in commit.trailers.items() -%}
{%- if trailer_value|is_url %} [{{ trailer_name }}]({{ trailer_value }})
{%- else %} {{ trailer_name }}: {{ trailer_value }}{% endif %}
{%- if not loop.last %},{% endif %}
{%- endfor -%}
