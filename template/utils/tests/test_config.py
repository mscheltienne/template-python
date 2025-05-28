from __future__ import annotations

from io import StringIO

import pytest

from ..config import _get_gpu_info, sys_info


def test_sys_info() -> None:
    """Test info-showing utility."""
    out = StringIO()
    sys_info(fid=out)
    value = out.getvalue()
    out.close()
    assert "Platform:" in value
    assert "Executable:" in value
    assert "CPU:" in value
    assert "Physical cores:" in value
    assert "Logical cores" in value
    assert "RAM:" in value
    assert "SWAP:" in value

    assert "numpy" in value
    assert "psutil" in value

    assert "style" not in value
    assert "test" not in value

    out = StringIO()
    sys_info(fid=out, developer=True)
    value = out.getvalue()
    out.close()

    assert "style" in value
    assert "test" in value


def test_gpu_info() -> None:
    """Test getting GPU info."""
    pytest.importorskip("pyvista")
    version, renderer = _get_gpu_info()
    assert version is not None
    assert renderer is not None


def test_sys_info_invalid() -> None:
    """Test getting information on package without requirements."""
    out = StringIO()
    with pytest.raises(RuntimeError, match="could not be retrieved"):
        sys_info(fid=out, package="numpy")
    out.close()


def test_sys_info_other_package() -> None:
    """Test getting information on another package."""
    out = StringIO()
    sys_info(fid=out, package="psutil")
    value = out.getvalue()
    out.close()
    assert "psutil" in value


def test_sys_info_other_package_dev() -> None:
    """Test getting developer information on another package."""
    out = StringIO()
    with pytest.raises(RuntimeError, match="from source in an editable install"):
        sys_info(fid=out, package="psutil", developer=True)
    out.close()
