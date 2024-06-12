from __future__ import annotations

import click

from .sys_info import run as sys_info


@click.group()
def run():
    """Main package entry-point."""


run.add_command(sys_info)
