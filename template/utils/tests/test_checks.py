from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pytest

from .._checks import check_type, check_value, ensure_int, ensure_path, ensure_verbose


def test_ensure_int() -> None:
    """Test ensure_int checker."""
    # valids
    assert ensure_int(101) == 101

    # invalids
    with pytest.raises(TypeError, match="Item must be an int"):
        ensure_int(101.0)
    with pytest.raises(TypeError, match="Item must be an int"):
        ensure_int(True)
    with pytest.raises(TypeError, match="Item must be an int"):
        ensure_int([101])


def test_check_type() -> None:
    """Test check_type checker."""
    # valids
    check_type(101, ("int-like",))
    check_type(101, ("int-like", str))
    check_type("101.fif", ("path-like",))

    def foo() -> None:
        pass

    check_type(foo, ("callable",))

    check_type(101, ("numeric",))
    check_type(101.0, ("numeric",))
    check_type((1, 0, 1), ("array-like",))
    check_type([1, 0, 1], ("array-like",))
    check_type(np.array([1, 0, 1]), ("array-like",))

    # invalids
    with pytest.raises(TypeError, match="Item must be an instance of"):
        check_type(101, (float,))
    with pytest.raises(TypeError, match="Item must be an instance of"):
        check_type(101, ("array-like",))
    with pytest.raises(TypeError, match="'number' must be an instance of"):
        check_type(101, (float,), "number")


def test_check_value() -> None:
    """Test check_value checker."""
    # valids
    check_value(5, (5,))
    check_value(5, (5, 101))
    check_value(5, [1, 2, 3, 4, 5])
    check_value((1, 2), [(1, 2), (2, 3, 4, 5)])

    # invalids
    with pytest.raises(ValueError, match="Invalid value for the parameter."):
        check_value(5, [1, 2, 3, 4])
    with pytest.raises(ValueError, match="Invalid value for the 'number' parameter."):
        check_value(5, [1, 2, 3, 4], "number")


def test_ensure_verbose() -> None:
    """Test ensure_verbose checker."""
    # valids
    assert ensure_verbose(12) == 12
    assert ensure_verbose("INFO") == logging.INFO
    assert ensure_verbose("DEBUG") == logging.DEBUG
    assert ensure_verbose(True) == logging.INFO
    assert ensure_verbose(False) == logging.WARNING
    assert ensure_verbose(None) == logging.WARNING

    # invalids
    with pytest.raises(TypeError, match="must be an instance of"):
        ensure_verbose(("INFO",))
    with pytest.raises(ValueError, match="Invalid value"):
        ensure_verbose("101")
    with pytest.raises(ValueError, match="negative integer, -101 is invalid."):
        ensure_verbose(-101)


def test_ensure_path() -> None:
    """Test ensure_path checker."""
    # valids
    cwd = Path.cwd()
    path = ensure_path(cwd, must_exist=False)
    assert isinstance(path, Path)
    path = ensure_path(cwd, must_exist=True)
    assert isinstance(path, Path)
    path = ensure_path(str(cwd), must_exist=False)
    assert isinstance(path, Path)
    path = ensure_path(str(cwd), must_exist=True)
    assert isinstance(path, Path)
    path = ensure_path("101", must_exist=False)
    assert isinstance(path, Path)

    with pytest.raises(FileNotFoundError, match="does not exist."):
        ensure_path("101", must_exist=True)

    # invalids
    with pytest.raises(TypeError, match="'101' is invalid"):
        ensure_path(101, must_exist=False)

    class Foo:
        def __str__(self) -> None:
            pass

    with pytest.raises(TypeError, match="path is invalid"):
        ensure_path(Foo(), must_exist=False)
