#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Veles Team'
SITENAME = "Veles Developers' Blog"
SITEURL = 'https://velesnet.ml/blog'

PATH = 'content'

TIMEZONE = 'Europe/Moscow'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
MD_EXTENSIONS = ["gfm"]

# Blogroll
LINKS = (('Veles on GitHub', 'https://github.com/samsung/veles'),
         ('Gerrit', 'https://velesnet.ml/gerrit'),
         ('Jenkins', 'http://velesnet.ml/jenkins'),
         ('Benchmarks', 'http://velesnet.ml/benchmarks'),)

# Social widget
SOCIAL = (('Twitter', 'https:/twotter.com/velesml'),)
GITHUB_URL = "https://github.com/samsung/veles"
TWITTER_USERNAME = "velesml"

DEFAULT_PAGINATION = 5

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from twitter_tokens import *
TWITTER_TEMPLATE = "[BLOG] {{ article.title }} {{ article.url }}"
TWITTER_LANGUAGE = "en"
