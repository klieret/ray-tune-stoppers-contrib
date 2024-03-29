# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from __future__ import annotations

from pathlib import Path

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "ray-tune-stoppers-contrib"
copyright = "2022, Kilian Lieret"
author = "Kilian Lieret"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.napoleon"]

extensions.append("autoapi.extension")
extensions.append("recommonmark")

autoapi_type = "python"
autoapi_dirs = ["../../src/rt_stoppers_contrib"]
autoapi_ignore = ["*/no_improvement.py", "*/threshold_by_epoch.py", "*/util/*"]
autoapi_python_class_content = "init"
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "special-members",
    "imported-members",
]

templates_path = ["_templates"]
exclude_patterns = []

html_title = "Ray Tune Stoppers"
html_logo = "_static/logo.png"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"
html_static_path = ["_static"]

# -- Copy readme

readme_path = Path(__file__).parent.resolve().parent.parent / "README.md"
readme_target = Path(__file__).parent / "readme.md"

with readme_target.open("w") as outf:
    outf.write(
        "\n".join(
            [
                "Readme",
                "======",
            ]
        )
    )
    lines = []
    for line in readme_path.read_text().splitlines():
        if line.startswith("# "):
            # Skip title, because we now use "Readme"
            continue
        if "<div" in line or "</div" in line:
            continue
        if "logo.png" in line:
            continue
        lines.append(line)
    outf.write("\n".join(lines))
