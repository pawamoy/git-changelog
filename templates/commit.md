commit {{ commit.commit_hash }}
Author name: {{ commit.author_name }}
Author email: {{ commit.author_email }}
Author date: {{ commit.author_date }}
Committer name: {{ commit.committer_name }}
Committer email: {{ commit.committer_email }}
Committer date: {{ commit.committer_date }}
{% if commit.tag %}Tag: {{ commit.tag }}{% endif %}
Subject: {{ commit.subject }}
Body: {% for line in commit.body %}
{% if line %}{{ line }}{% endif %}
{% endfor %}