# Configuration file for the Sphinx documentation builder.
# collective.mastodon documentation build configuration file


from datetime import datetime
from packaging.version import parse
from packaging.version import Version
from pathlib import Path

# -- Path setup --------------------------------------------------------------
import re


# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath("."))


# -- Project information -----------------------------------------------------
year = datetime.now().year

project = "collective.mastodon"
copyright = f"2023 - {year}, Simples Consultoria"
author = "Érico Andrei"
trademark_name = "Simples Consultoria"
now = datetime.now()
year = str(now.year)

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.


def extract_version() -> Version:
    """Extract version from setup.py."""
    path = Path("../setup.py").resolve()
    text = path.read_text()
    pattern = r"""version="([^"]*)","""
    return parse(re.search(pattern, text).groups()[0])


_version = extract_version()

# The short X.Y version.
version = f"{_version.major}.{_version.minor}"
# The full version, including alpha/beta/rc tags.
release = f"{_version}"

# -- General configuration ----------------------------------------------------

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# Add any Sphinx extension module names here, as strings.
# They can be extensions coming with Sphinx (named "sphinx.ext.*")
# or your custom ones.
extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx_copybutton",
]


# If true, the Docutils Smart Quotes transform, originally based on SmartyPants
# (limited to English) and currently applying to many languages, will be used
# to convert quotes and dashes to typographically correct entities.
# Note to maintainers: setting this to `True` will cause contractions and
# hyphenated words to be marked as misspelled by spellchecker.
smartquotes = False

# The name of the Pygments (syntax highlighting) style to use.
# pygments_style = "sphinx.pygments_styles.PyramidStyle"
pygments_style = "sphinx"

# Options for the linkcheck builder
# Ignore localhost
linkcheck_ignore = [
    r"http://localhost",
    r"http://0.0.0.0",
    r"http://127.0.0.1",
]
linkcheck_anchors = True
linkcheck_timeout = 10
linkcheck_retries = 2

# This is our wordlist with known words, like Github or Plone ...
spelling_word_list_filename = "spelling_wordlist.txt"
spelling_ignore_pypi_package_names = True

# The suffix of source filenames.
source_suffix = {
    ".md": "markdown",
    ".rst": "restructuredtext",
}

# The master toctree document.
master_doc = "index"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "spelling_wordlist.txt",
    "robots.txt",
    "requirements.txt",
    "Dockerfile",
    "_build/*",
    "_static/*",
    "bin/*",
    "include/*",
    "lib/*",
    "lib64/*",
]

html_extra_path = [
    "robots.txt",
]

html_static_path = [
    "_static",
]

# -- Options for myST markdown conversion to html -----------------------------

# For more information see:
# https://myst-parser.readthedocs.io/en/latest/syntax/optional.html
myst_enable_extensions = [
    "deflist",  # You will be able to utilise definition lists
    # https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#definition-lists
    "linkify",  # Identify “bare” web URLs and add hyperlinks.
    "colon_fence",  # You can also use ::: delimiters to denote code fences,\
    #  instead of ```.
]

myst_substitutions = {}

# -- Intersphinx configuration ----------------------------------

# This extension can generate automatic links to the documentation of objects
# in other projects. Usage is simple: whenever Sphinx encounters a
# cross-reference that has no matching target in the current documentation set,
# it looks for targets in the documentation sets configured in
# intersphinx_mapping. A reference like :py:class:`zipfile.ZipFile` can then
# linkto the Python documentation for the ZipFile class, without you having to
# specify where it is located exactly.
#
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html
#
# Note that collective.mastodon documentation imports documentation from
# several remote repositories.
# These projects need to build their docs as part of their CI/CD and testing.
# We use Intersphinx to resolve targets when either the individual project's or
# the entire collective.mastodon documentation is built.
intersphinx_mapping = {}


# -- GraphViz configuration ----------------------------------

graphviz_output_format = "svg"


# -- OpenGraph configuration ----------------------------------

ogp_site_url = "https://collectivemastodon.readthedocs.io/"
ogp_description_length = 200
ogp_image = "https://collectivemastodon.readthedocs.io/_static/images/icon.png"
ogp_site_name = "collective.mastodon documentation"
ogp_type = "website"
ogp_custom_meta_tags = [
    '<meta property="og:locale" content="en_US" />',
]


# -- sphinx_copybutton -----------------------
copybutton_prompt_text = r"^ {0,2}\d{1,3}"
copybutton_prompt_is_regexp = True


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_book_theme"

html_logo = "_static/images/icon.png"
html_favicon = "_static/favicon.ico"

html_css_files = ["custom.css", ("print.css", {"media": "print"})]

# See http://sphinx-doc.org/ext/todo.html#confval-todo_include_todos
todo_include_todos = True

# Announce that we have an opensearch plugin
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_use_opensearch
html_use_opensearch = "https://collectivemastodon.readthedocs.io/"

html_theme_options = {
    "path_to_docs": "docs",
    "repository_url": "https://github.com/collective/collective.mastodon",
    "repository_branch": "main",
    "use_repository_button": True,
    "use_issues_button": True,
    "use_edit_page_button": True,
    "extra_navbar": "",
    "extra_footer": "",
}

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = f"{project} v{release}"

# If false, no index is generated.
html_use_index = True

# Used by sphinx_sitemap to generate a sitemap
html_baseurl = "https://collectivemastodon.readthedocs.io/"

# -- Options for HTML help output -------------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "ContentRulesMastodonDoc"


# -- Options for LaTeX output -------------------------------------------------

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual])
latex_documents = [
    (
        "index",
        "ContentRulesMastodonDoc.tex",
        "collective.mastodon documentation",
        "Pendect GmbH",
        "manual",
    ),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
latex_logo = "_static/images/icon.png"
