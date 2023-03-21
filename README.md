[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![codecov](https://codecov.io/gh/mscheltienne/template-python/branch/main/graph/badge.svg?token=KRYRRUXDYY)](https://codecov.io/gh/mscheltienne/template-python)
[![tests](https://github.com/mscheltienne/template-python/actions/workflows/pytest.yml/badge.svg?branch=main)](https://github.com/mscheltienne/template-python/actions/workflows/pytest.yml)
[![build](https://github.com/mscheltienne/template-python/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/mscheltienne/template-python/actions/workflows/build.yml)
[![doc](https://github.com/mscheltienne/template-python/actions/workflows/doc.yml/badge.svg?branch=main)](https://github.com/mscheltienne/template-python/actions/workflows/doc.yml)

# template-python

## Package

Template python repository. To bootstrap a project from this template, the
following steps are required:

- [ ] Rename the folder `template` to the package name
- [ ] Edit `pyproject.toml`
    - [ ] Under `[project]`, edit `name`, `description` and `keywords`
    - [ ] Under `[project.optional-dependencies]`, edit the extra-keys `all` and `full`
    - [ ] Under `[project.urls]`, edit all the URLs
    - [ ] Under `[project.scripts]`, edit the command for system information
    - [ ] Under `[tool.setuptools.packages.find]`, edit the file inclusion/exclusion patterns
    - [ ] Under `[tool.pydocstyle]`, edit the matching pattern `match-dir`
    - [ ] Under `[tool.coverage.run]`, edit the exclusion patterns `omit`
- [ ] Edit the GitHub workflows
    - [ ] In `build.yml`, edit the command for system information and uninstallation
    - [ ] In `publish.yml`, uncomment the trigger on release and edit the command for system information
    - [ ] In `pytest.yml`, edit the command for system information and pytest
- [ ] Edit `README.md`

The package can then be installed in a given environment with
`pip install -e .` (assuming the current working directory is the root of the
repository).

## Documentation build

If the documentation build is preserved, the following steps are required:

On the `main` branch:
- [ ] Edit the GitHub workflows
    - [ ] In `doc.yml`, edit the command for system information
- [ ] Edit the project links in `doc\links.inc`
- [ ] Edit the landing page `index.rst`
- [ ] Edit the sphinx configuration
    - [ ] Replace `import template` with the correct package name
    - [ ] Edit the fields `project`, `author`, `release`, `package` and `gh_url`
- [ ] Edit the API pages
    - [ ] In `doc\api\index.rst`, edit the package name
    - [ ] In `doc\api\logging.rst`, edit the current module
- [ ] Edit the logging tutorial to replace `from template import` with the correct package name

On the `gh-pages` branch:
- [ ] Edit the links in the landing page `index.html`
