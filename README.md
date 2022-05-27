[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![tests](https://github.com/mscheltienne/template-python/actions/workflows/pytest.yml/badge.svg?branch=main)](https://github.com/mscheltienne/template-python/actions/workflows/pytest.yml)

# template-python

Template python repository.

The folder name `template` should be changed to the package name.
Entries in `pyproject.toml` should be adapted to the path(s)/URL(s)/name(s)/...
involved in the package.
Entries in the CIs workflow should be updated:
- `build.yml`: name of the package
- `code-style.yml`: path to the package for the `flake8` action
- `pytest.yml`: path to the package for the `pytest` action
