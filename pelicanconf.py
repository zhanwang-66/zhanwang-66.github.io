#!/usr/bin/env python
"""Pelican configuration for zhanwang-66.github.io"""

AUTHOR = 'zhanwang-66'
SITENAME = 'Zhanwang Blog'
SITESUBTITLE = ''
SITEURL = 'https://zhanwang-66.github.io'

PATH = 'content'
OUTPUT_PATH = 'output'

TIMEZONE = 'Asia/Shanghai'
DEFAULT_LANG = 'zh'

# ── URL structure: /posts/slug/ ──────────────────────────
ARTICLE_URL = 'posts/{slug}/'
ARTICLE_SAVE_AS = 'posts/{slug}/index.html'
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
CATEGORY_URL = 'category/{slug}/'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'
TAG_URL = 'tag/{slug}/'
TAG_SAVE_AS = 'tag/{slug}/index.html'

# ── Feeds ────────────────────────────────────────────────
FEED_ALL_ATOM = 'feeds/all.atom.xml'
FEED_ALL_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# ── Content ──────────────────────────────────────────────
DEFAULT_PAGINATION = 10
SUMMARY_MAX_LENGTH = 50

# Use Markdown
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.toc': {'permalink': '#'},
    },
}

# ── Theme ────────────────────────────────────────────────
# THEME = 'theme'  # 当前使用 Pelican 内置 simple 主题，后续可自定义

# ── Plugins ──────────────────────────────────────────────
PLUGINS = []

# ── Static files ─────────────────────────────────────────
STATIC_PATHS = ['images', 'extra']
EXTRA_PATH_METADATA = {
    'extra/favicon.ico': {'path': 'favicon.ico'},
    'extra/CNAME': {'path': 'CNAME'},
}

# ── Disable unused pages ─────────────────────────────────
AUTHOR_SAVE_AS = ''
ARCHIVES_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
CATEGORIES_SAVE_AS = ''
TAGS_SAVE_AS = ''
