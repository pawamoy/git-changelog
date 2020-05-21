- {% if commit.style.scope %}**{{ commit.style.scope }}:** {% endif %}{{ commit.style.subject }} ([{{ commit.sha|truncate(7, True, '') }}]({{ commit.url }}))
{%- if commit.text_refs.issues_not_in_subject %}, related to {% for issue in commit.text_refs.issues_not_in_subject -%}
[{{ issue.ref }}]({{ issue.url }}){% if not loop.last %}, {% endif -%}
{%- endfor -%}{%- endif -%}
