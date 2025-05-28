from collections.abc import Callable
from typing import IO

from packaging.requirements import Requirement

from ._checks import check_type as check_type

def sys_info(
    fid: IO | None = None,
    *,
    extra: bool = False,
    developer: bool = False,
    package: str | None = None,
) -> None:
    """Print the system information for debugging.

    Parameters
    ----------
    fid : file-like | None
        The file to write to, passed to :func:`print`. Can be None to use
        :data:`sys.stdout`.
    extra : bool
        If True, display information about optional dependencies.
    developer : bool
        If True, display information about optional dependencies. Only available for
        the package installed in editable mode.
    package : str | None
        The package to display information about. If None, display information about the
        current package.
    """

def _list_dependencies_info(
    out: Callable, ljust: int, package: str, dependencies: list[Requirement]
) -> None:
    """List dependencies names and versions."""

def _get_gpu_info() -> tuple[str | None, str | None]:
    """Get the GPU information."""
