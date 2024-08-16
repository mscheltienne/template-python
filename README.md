[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![codecov](https://codecov.io/gh/mscheltienne/template-python/branch/main/graph/badge.svg?token=KRYRRUXDYY)](https://codecov.io/gh/mscheltienne/template-python)
[![tests](https://github.com/mscheltienne/template-python/actions/workflows/pytest.yaml/badge.svg?branch=main)](https://github.com/mscheltienne/template-python/actions/workflows/pytest.yaml)
[![doc](https://github.com/mscheltienne/template-python/actions/workflows/doc.yaml/badge.svg?branch=main)](https://github.com/mscheltienne/template-python/actions/workflows/doc.yaml)

# template-python

## Package

Template python repository. To bootstrap a project from this template, the
following steps are required:

- [ ] Rename the folder `template` to the package name
- [ ] Edit `pyproject.toml` and all the `template` entries
- [ ] Edit the GitHub workflows in `.github`
- [ ] Enable `pre-commit.ci` on https://pre-commit.ci/
- [ ] Edit `README.md`
- [ ] Edit `MANIFEST.in`
- [ ] Edit the package import in `tools/stubgen.py`
- [ ] Remove the conda-forge recipe from the ignored files in ``.yamllint.yaml``

The package can then be installed in a given environment with
`pip install -e .` (assuming the current working directory is the root of the
repository).

## Documentation build

If the documentation build is preserved, the following steps are required:

On the `main` branch:
- [ ] Edit the project links in `doc\links.inc`
- [ ] Edit the landing page `index.rst`
- [ ] Edit the sphinx configuration `doc/conf.py`
- [ ] Edit the API pages
    - [ ] In `doc\api\index.rst`, edit the package name
    - [ ] In `doc\api\logging.rst`, edit the current module
- [ ] Edit the logging tutorial to replace `from template import` with the correct package name

On the `gh-pages` branch:
- [ ] Edit the links in the landing page `index.html`
