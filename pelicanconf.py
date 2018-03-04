#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Charlie Hu'
SITENAME = 'Tower of Babel'
SITEURL = ''

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'))

# Social widget
SOCIAL = (('linkedin', 'http://www.linkedin.com/in/danieldebie'),
          ('github', 'https://github.com/Motor-taxi-master-rider'))

DEFAULT_PAGINATION = 5

# Paths
PATH = 'content'
PAGE_PATHS = ['pages']
ARTICLE_PATHS = ['posts']
STATIC_PATHS = ['img','assets','assets/CNAME', 'code']
PLUGIN_PATHS = ['pelican-plugins']
EXTRA_PATH_METADATA = {
    	'assets/custom.css': {'path': 'static/css/custom.css'},
	    'assets/jupyter.css': {'path': 'static/css/jupyter.css'},
    	'assets/custom.js': {'path': 'static/js/custom.js'},
    	'assets/CNAME': {'path': 'CNAME'},
}
#consider above to have assets/custom.js bath go to static/theme/js and see if that works

SUMMARY_MAX_LENGTH = 50
WITH_FUTURE_DATES = False

#Theme, environements and plugins
THEME = 'pelican-themes/pelican-bootstrap3'
BOOTSTRAP_THEME = 'flatly'
FAVICON = 'assets/favicon.ico'
AVATAR ='assets/img/avatar.png'
CUSTOM_CSS = 'static/css/custom.css'
CUSTOM_JS = 'static/js/custom.js'
PYGMENTS_STYLE = 'native'

#to ignore any injected css for ipynb pages
IPYNB_IGNORE_CSS = True


#Plugins, extensions
JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}
PLUGINS = [
    'i18n_subsites','series','tag_cloud',
    'liquid_tags.img', 'liquid_tags.video', 'liquid_tags.youtube', 'liquid_tags.notebook',
    'liquid_tags.vimeo',
    'liquid_tags.include_code',
    'pelican_javascript',
    'related_posts',
    'render_math','tipue_search','pelican-ipynb.markup',
    'neighbors',]

NOTEBOOK_DIR = 'posts'

I18N_TEMPLATES_LANG = 'en'
MARKUP = ('md', 'ipynb','html')
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
	'markdown.extensions.tables': {},
    },
    'output_format': 'html5',
}
#Ignore all files that start with a dot .
IGNORE_FILES = ['.*']

# Breadcrumbs
DISPLAY_BREADCRUMBS = True
DISPLAY_CATEGORY_IN_BREADCRUMBS = True

SERIES_TEXT = 'Article %(index)s of the %(name)s series'
#sidebar options
   # Tag Cloud Options
DISPLAY_SERIES_ON_SIDEBAR = True
DISPLAY_TAGS_INLINE = True
TAG_CLOUD_MAX_ITEMS = 10
   # Recent Posts in Sidebas
DISPLAY_RECENT_POSTS_ON_SIDEBAR = True
RECENT_POST_COUNT = 3
   # Series infor on sidebar
SHOW_SERIES = True
DISPLAY_ARTICLE_INFO_ON_INDEX = True
    #Github on sidebar
GITHUB_USER = 'Motor-taxi-master-rider'
GITHUB_REPO_COUNT = 3
GITHUB_SKIP_FORK = True
GITHUB_SHOW_USER_LINK = True


# Top menus
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = True
ARCHIVES_SAVE_AS = 'archives.html'
DISPLAY_ARCHIVE_ON_MENU = True
YEAR_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/{date:%b}/index.html'
ABOUT_ME = 'Software engineer, Geeker. ' \
           'Here I mostly blog about Python, algorithm and how programing can be intersting.'

# for Tique Search Plugin
DIRECT_TEMPLATES = ('index','tags', 'categories', 'authors', 'archives', 'search')

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = 5
