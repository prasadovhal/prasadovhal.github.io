---
layout: archive
title: "Writing"
permalink: /writing/
author_profile: true
---

{% if site.author.medium %}
  <div class="wordwrap">You can also find my articles on <a href="{{ site.author.medium }}">Medium</a>.</div>
{% endif %}

{% include base_path %}

{% for post in site.writing reversed %}
  {% include archive-single.html %}
{% endfor %}
