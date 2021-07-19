# -*- coding: utf-8 -*-

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import sys, os
import sphinx_bootstrap_theme

sys.path.insert(0, os.path.abspath("../"))

# import your package to obtain the version info to display on the docs website
import spopt


# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [  #'sphinx_gallery.gen_gallery',
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinxcontrib.bibtex",
    "sphinx.ext.mathjax",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "nbsphinx",
    "numpydoc",
    "matplotlib.sphinxext.plot_directive",
]
bibtex_bibfiles = ["_static/references.bib"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "spopt"
copyright = "2020-, pysal developers"
author = "pysal developers"

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The full version.
version = spopt.__version__
release = spopt.__version__

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "tests/*"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
html_theme = "bootstrap"
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()
html_title = "%s v%s Manual" % (project, version)

# (Optional) Logo of your package. Should be small enough to fit the navbar (ideally 24x24).
# Path should be relative to the ``_static`` files directory.
# html_logo = "_static/images/package_logo.jpg"

# (Optional) PySAL favicon
html_favicon = "_static/images/pysal_favicon.ico"


# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    # Navigation bar title. (Default: ``project`` value)
    "navbar_title": project,  # string of your project name, for example, 'spopt'
    # Render the next and previous page links in navbar. (Default: true)
    "navbar_sidebarrel": False,
    # Render the current pages TOC in the navbar. (Default: true)
    #'navbar_pagenav': True,
    #'navbar_pagenav': False,
    # No sidebar
    "nosidebar": True,
    # Tab name for the current pages TOC. (Default: "Page")
    #'navbar_pagenav_name': "Page",
    # Global TOC depth for "site" navbar tab. (Default: 1)
    # Switching to -1 shows all levels.
    "globaltoc_depth": 2,
    # Include hidden TOCs in Site navbar?
    #
    # Note: If this is "false", you cannot have mixed ``:hidden:`` and
    # non-hidden ``toctree`` directives in the same page, or else the build
    # will break.
    #
    # Values: "true" (default) or "false"
    "globaltoc_includehidden": "true",
    # HTML navbar class (Default: "navbar") to attach to <div> element.
    # For black navbar, do "navbar navbar-inverse"
    #'navbar_class': "navbar navbar-inverse",
    # Fix navigation bar to top of page?
    # Values: "true" (default) or "false"
    "navbar_fixed_top": "true",
    # Location of link to source.
    # Options are "nav" (default), "footer" or anything else to exclude.
    "source_link_position": "footer",
    # Bootswatch (http://bootswatch.com/) theme.
    #
    # Options are nothing (default) or the name of a valid theme
    # such as "amelia" or "cosmo", "yeti", "flatly".
    "bootswatch_theme": "yeti",
    # Choose Bootstrap version.
    # Values: "3" (default) or "2" (in quotes)
    "bootstrap_version": "3",
    # Navigation bar menu
    "navbar_links": [
        ("Installation", "installation"),
        ("Tutorials", "tutorials"),
        ("API", "api"),
        ("References", "references"),
    ],
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}
# html_sidebars = {'sidebar': ['localtoc.html', 'sourcelink.html', 'searchbox.html']}

# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "%sdoc" % project


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        "%sdoc.tex" % project,
        u"%s Documentation" % project,
        u"%s developers" % project,
        "manual",
    )
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, project, u"%s Documentation" % project, [author], 1)]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        project,
        u"%s Documentation" % project,
        author,
        project,
        "Spatial Optimization with PySAL",
        "Miscellaneous",
    ),
]


# -----------------------------------------------------------------------------
# Autosummary
# -----------------------------------------------------------------------------

# Generate the API documentation when building
autosummary_generate = True

# Avoid showing members twice
numpydoc_show_class_members = False
numpydoc_use_plots = True
class_members_toctree = True
numpydoc_show_inherited_class_members = True
numpydoc_xref_param_type = True

# automatically document class members
autodoc_default_options = {"members": True, "undoc-members": True}

# display the source code for Plot directive
plot_include_source = True


def setup(app):
    app.add_css_file("pysal-styles.css")


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "esda": ("https://pysal.org/esda/", None),
    "geopandas": ("https://geopandas.readthedocs.io/en/latest/", None),
    "giddy": ("https://giddy.readthedocs.io/en/latest/", None),
    "hdbscan": ("https://hdbscan.readthedocs.io/en/latest/", None),
    "libpysal": ("https://pysal.org/libpysal/", None),
    "numpy": ("https://docs.scipy.org/doc/numpy", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "pulp": ("https://coin-or.github.io/pulp/", None),
    "python": ("https://docs.python.org/3.9/", None),
    "region": ("https://region.readthedocs.io/en/latest/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/reference/", None),
    "sklearn": ("https://scikit-learn.org/stable/", None),
}

numpydoc_xref_ignore = {
    "type",
    "optional",
    "default",
    "shape",
    "fitted",
    "instance",
    "cluster",
    "of",
    "or",
    "if",
    "using",
    "otherwise",
    "required",
    "from",
}


# This is processed by Jinja2 and inserted before each notebook
nbsphinx_prolog = r"""
{% set docname = env.doc2path(env.docname, base=None) %}

.. only:: html

    .. role:: raw-html(raw)
        :format: html

    .. nbinfo::

        This page was generated from `{{ docname }}`__.
        Interactive online version:
        :raw-html:`<a href="https://mybinder.org/v2/gh/pysal/spopt/main?filepath={{ docname }}"><img alt="Binder badge" src="https://mybinder.org/badge_logo.svg" style="vertical-align:text-bottom"></a>`

    __ https://github.com/pysal/spopt/blob/main/{{ docname }}

.. raw:: latex

    \nbsphinxstartnotebook{\scriptsize\noindent\strut
    \textcolor{gray}{The following section was generated from
    \sphinxcode{\sphinxupquote{\strut {{ docname | escape_latex }}}} \dotfill}}
"""

# This is processed by Jinja2 and inserted after each notebook
nbsphinx_epilog = r"""
.. raw:: latex

    \nbsphinxstopnotebook{\scriptsize\noindent\strut
    \textcolor{gray}{\dotfill\ \sphinxcode{\sphinxupquote{\strut
    {{ env.doc2path(env.docname, base='doc') | escape_latex }}}} ends here.}}
"""

# List of arguments to be passed to the kernel that executes the notebooks:
nbsphinx_execute_arguments = [
    "--InlineBackend.figure_formats={'svg', 'pdf'}",
    "--InlineBackend.rc={'figure.dpi': 96}",
]

mathjax_config = {
    "TeX": {"equationNumbers": {"autoNumber": "AMS", "useLabelIds": True}},
}
