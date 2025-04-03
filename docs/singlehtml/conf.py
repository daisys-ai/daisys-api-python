# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
import pathlib

project = 'daisys-api'
copyright = '2025, Daisys AI'
author = 'Daisys AI'
release = next(line.split('"')[1]
               for line in open(pathlib.Path(__file__).parent.parent.parent / 'pyproject.toml')
               if line.startswith('version = '))

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']

templates_path = ['_templates']
exclude_patterns = []

autodoc_default_flags = ['members']

# -- Path setup --
sys.path.insert(0, os.path.abspath('../..'))
