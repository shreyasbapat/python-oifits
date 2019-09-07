import os
from datetime import datetime

import alabaster

project = "python-oifits"
year = datetime.now().year
copyright = "%d Shreyas Bapat" % year

version = "0.2"
release = "0.2.0"
highlight_language = "python"
pygments_style = "sphinx"
autoclass_content = "both"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "astropy": ("http://docs.astropy.org/en/stable/", None),
    "numpy": ("https://docs.scipy.org/doc/numpy/", None)
}

autodoc_member_order = "bysource"

html_theme_options = {
    "logo": "logo_small.png",
    "logo_name": True,
    "logo_text_align": "center",
    "description": "Analysing EHT Data in Python",
    "body_text_align": "left",
    "github_user": "shreyasbapat",
    "github_repo": "python-oifits",
    "show_relbars": True,
    "show_powered_by": False,
    "page_width": "80%",
    "github_banner": True,
}

add_function_parentheses = True

add_module_names = True

needs_sphinx = "1.3"
extensions = [
    "alabaster",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.mathjax",
    "sphinx.ext.intersphinx",
    "nbsphinx",
    "IPython.sphinxext.ipython_console_highlighting",
]
templates_path = ["_templates"]

source_suffix = ".rst"

master_doc = "index"

html_theme = "alabaster"

html_theme_path = [alabaster.get_path()]

html_title = "python-oifits"

html_static_path = ["_static"]

htmlhelp_basename = "oifitsdoc"

html_sidebars = {
    "**": [
        "about.html",
        "navigation.html",
        "relations.html",
        "searchbox.html",
        "donate.html",
    ]
}
