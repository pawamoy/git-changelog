- {{ commit.subject }} ([{{ commit.hash|truncate(7, True, '') }}]({{ commit.url }})).
{%- if commit.text_refs.issues_not_in_subject %} Related issues/PRs: {% for issue in commit.text_refs.issues_not_in_subject -%}
{{ issue.ref }}{% if not loop.last %}, {% endif -%}
{%- endfor -%}{%- endif -%}