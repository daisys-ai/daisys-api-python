# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'daisys-api'
copyright = '2023, Daisys AI'
author = 'Daisys AI'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']

templates_path = ['_templates']
exclude_patterns = []

autodoc_default_flags = ['members']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']

html_theme_options = {
    "light_logo": "daisys-logo-light.png",
    "dark_logo": "daisys-logo.png",
    "light_css_variables": {
        "color-toc-background": "black",
    },
    "dark_css_variables": {
        "color-background-primary": "black",
        "color-background-secondary": "black",
        "color-foreground-primary": "white",
        "color-foreground-secondary": "#19AAD8",
    },
}

# -- Path setup --
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
