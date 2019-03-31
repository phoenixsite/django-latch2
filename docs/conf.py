import os
import sys

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

extensions = []
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'django-latch'
copyright = u'2019, Javier Moral'
version = '0.3'
release = '0.3'
exclude_trees = ['_build']
pygments_style = 'sphinx'
html_static_path = ['_static']
htmlhelp_basename = 'django-latchdoc'
latex_documents = [
  ('index', 'django-latch.tex', u'django-latch Documentation',
   u'Javier Moral', 'manual'),
]
if not on_rtd:
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
