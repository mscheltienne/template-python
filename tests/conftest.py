from __future__ import annotations

from typing import TYPE_CHECKING

from template.utils.logs import logger

if TYPE_CHECKING:
    import pytest


def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest options."""
    logger.propagate = True  # setup logging
