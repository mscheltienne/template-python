"""Fill docstrings to avoid redundant docstrings in multiple files.

Inspired from mne: https://mne.tools/stable/index.html
Inspired from mne.utils.docs.py by Eric Larson <larson.eric.d@gmail.com>
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any

# -- Documentation dictionary ----------------------------------------------------------
docdict: dict[str, str] = dict()

# -- A ---------------------------------------------------------------------------------
# -- B ---------------------------------------------------------------------------------
# -- C ---------------------------------------------------------------------------------
# -- D ---------------------------------------------------------------------------------
# -- E ---------------------------------------------------------------------------------
# -- F ---------------------------------------------------------------------------------
# -- G ---------------------------------------------------------------------------------
# -- H ---------------------------------------------------------------------------------
# -- I ---------------------------------------------------------------------------------
# -- J ---------------------------------------------------------------------------------
# -- K ---------------------------------------------------------------------------------
# -- L ---------------------------------------------------------------------------------
# -- M ---------------------------------------------------------------------------------
# -- N ---------------------------------------------------------------------------------
# -- O ---------------------------------------------------------------------------------
# -- P ---------------------------------------------------------------------------------
# -- Q ---------------------------------------------------------------------------------
# -- R ---------------------------------------------------------------------------------
# -- S ---------------------------------------------------------------------------------
# -- T ---------------------------------------------------------------------------------
# -- U ---------------------------------------------------------------------------------
# -- V ---------------------------------------------------------------------------------
docdict["verbose"] = """
verbose : int | str | bool | None
    Sets the verbosity level. The verbosity increases gradually between ``"CRITICAL"``,
    ``"ERROR"``, ``"WARNING"``, ``"INFO"`` and ``"DEBUG"``. If None is provided, the
    verbosity is set to ``"WARNING"``. If a bool is provided, the verbosity is set to
    ``"WARNING"`` for False and to ``"INFO"`` for True."""

# -- W ---------------------------------------------------------------------------------
# -- X ---------------------------------------------------------------------------------
# -- Y ---------------------------------------------------------------------------------
# -- Z ---------------------------------------------------------------------------------

# -- Documentation functions -----------------------------------------------------------
docdict_indented: dict[int, dict[str, str]] = dict()


def fill_doc(f: Callable[..., Any]) -> Callable[..., Any]:
    """Fill a docstring with docdict entries.

    Parameters
    ----------
    f : callable
        The function to fill the docstring of (modified in place).

    Returns
    -------
    f : callable
        The function, potentially with an updated __doc__.
    """
    docstring = f.__doc__
    if not docstring:
        return f

    lines = docstring.splitlines()
    indent_count = _indentcount_lines(lines)

    try:
        indented = docdict_indented[indent_count]
    except KeyError:
        indent = " " * indent_count
        docdict_indented[indent_count] = indented = dict()

        for name, docstr in docdict.items():
            lines = [
                indent + line if k != 0 else line
                for k, line in enumerate(docstr.strip().splitlines())
            ]
            indented[name] = "\n".join(lines)

    try:
        f.__doc__ = docstring % indented
    except (TypeError, ValueError, KeyError) as exc:
        funcname = f.__name__
        funcname = docstring.split("\n")[0] if funcname is None else funcname
        exc.add_note(f"Error documenting {funcname}.")
        raise

    return f


def _indentcount_lines(lines: list[str]) -> int:
    """Minimum indent for all lines in line list.

    >>> lines = [" one", "  two", "   three"]
    >>> indentcount_lines(lines)
    1
    >>> lines = []
    >>> indentcount_lines(lines)
    0
    >>> lines = [" one"]
    >>> indentcount_lines(lines)
    1
    >>> indentcount_lines(["    "])
    0
    """
    indent = sys.maxsize
    for k, line in enumerate(lines):
        if k == 0:
            continue
        line_stripped = line.lstrip()
        if line_stripped:
            indent = min(indent, len(line) - len(line_stripped))
    return indent


def copy_doc(source: Callable[..., Any]) -> Callable[..., Any]:
    """Copy the docstring from another function (decorator).

    The docstring of the source function is prepepended to the docstring of the function
    wrapped by this decorator.

    This is useful when inheriting from a class and overloading a method. This decorator
    can be used to copy the docstring of the original method.

    Parameters
    ----------
    source : callable
        The function to copy the docstring from.

    Returns
    -------
    wrapper : callable
        The decorated function.

    Examples
    --------
    >>> class A:
    ...     def m1():
    ...         '''Docstring for m1'''
    ...         pass
    >>> class B(A):
    ...     @copy_doc(A.m1)
    ...     def m1():
    ...         '''this gets appended'''
    ...         pass
    >>> print(B.m1.__doc__)
    Docstring for m1 this gets appended
    """

    def wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
        if source.__doc__ is None or len(source.__doc__) == 0:
            raise RuntimeError(
                f"The docstring from {source.__name__} could not be copied because it "
                "was empty."
            )
        doc = source.__doc__
        if func.__doc__ is not None:
            doc += func.__doc__
        func.__doc__ = doc
        return func

    return wrapper
