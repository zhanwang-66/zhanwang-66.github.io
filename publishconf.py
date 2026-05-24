"""Production overrides — loaded by pelican -s publishconf.py"""

import sys
sys.path.insert(0, '.')
from pelicanconf import *  # noqa

SITEURL = 'https://zhanwang-66.github.io'
RELATIVE_URLS = False

# Cleaner output
DELETE_OUTPUT_DIRECTORY = True
