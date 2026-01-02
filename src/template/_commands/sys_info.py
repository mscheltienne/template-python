from __future__ import annotations

import click

from template.utils.config import sys_info


@click.command(name="sys-info")
@click.option(
    "--extra",
    help="Display information for optional dependencies.",
    is_flag=True,
)
@click.option(
    "--developer",
    help="Display information for developer dependencies.",
    is_flag=True,
)
@click.option(
    "--package",
    help="The package to display information about.",
    type=str,
)
def run(extra: bool, developer: bool, package: str | None) -> None:
    """Run sys_info() command."""
    sys_info(extra=extra, developer=developer, package=package)
