# -*- coding: utf-8 -*-
#
# Jiggety documentation build configuration file, created by
# sphinx-quickstart on Tue Jul  5 02:34:19 2011.
#

import sys, os

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#sys.path.insert(0, os.path.abspath('.'))

# -- General configuration -----------------------------------------------------
extensions = []
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'Jiggety'
copyright = u'2011, Lukasz Dobrzanski'
version = '0.0.1'
release = '0.0.1'
exclude_patterns = ['_build']
pygments_style = 'sphinx'

# -- Options for HTML output ---------------------------------------------------
html_theme = 'jiggety_theme'
html_theme_path = ["."]
html_static_path = ['_static']
htmlhelp_basename = 'Jiggetydoc'

# -- Options for LaTeX output --------------------------------------------------
latex_documents = [
  ('index', 'Jiggety.tex', u'Jiggety Documentation',
   u'Lukasz Dobrzanski', 'manual'),
]

# -- Options for manual page output --------------------------------------------
man_pages = [
    ('index', 'jiggety', u'Jiggety Documentation',
     [u'Lukasz Dobrzanski'], 1)
]
