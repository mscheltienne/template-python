from __future__ import annotations

import inspect
import logging
from functools import wraps
from importlib import import_module
from pathlib import Path
from typing import TYPE_CHECKING
from warnings import warn_explicit

from ._checks import ensure_verbose
from ._fixes import WrapStdOut

if TYPE_CHECKING:
    from collections.abc import Callable


_PACKAGE: str = __package__.split(".")[0]


def _init_logger(*, verbose: bool | str | int | None = None) -> logging.Logger:
    """Initialize a logger.

    Assigns sys.stdout as the first handler of the logger.

    Parameters
    ----------
    verbose : int | str | bool | None
        Sets the verbosity level. The verbosity increases gradually between
        ``"CRITICAL"``, ``"ERROR"``, ``"WARNING"``, ``"INFO"`` and ``"DEBUG"``. If
        ``None`` is provided, the verbosity is set to ``"WARNING"``. If a bool is
        provided, the verbosity is set to ``"WARNING"`` for ``False`` and to ``"INFO"``
        for ``True``.

    Returns
    -------
    logger : Logger
        The initialized logger.
    """
    # create logger
    verbose = ensure_verbose(verbose)
    logger = logging.getLogger(__package__.split(".utils", maxsplit=1)[0])
    logger.propagate = False
    logger.setLevel(verbose)
    # add the main handler
    handler = logging.StreamHandler(WrapStdOut())
    handler.setFormatter(_LoggerFormatter())
    logger.addHandler(handler)
    return logger


def add_file_handler(
    fname: str | Path,
    mode: str = "a",
    encoding: str | None = None,
    *,
    verbose: bool | str | int | None = None,
) -> None:
    """Add a file handler to the logger.

    Parameters
    ----------
    fname : str | Path
        Path to the file where the logging output is saved.
    mode : str
        Mode in which the file is opened.
    encoding : str | None
        If not None, encoding used to open the file.
    verbose : int | str | bool | None
        Sets the verbosity level of the file handler. The verbosity increases gradually
        between ``"CRITICAL"``, ``"ERROR"``, ``"WARNING"``, ``"INFO"`` and ``"DEBUG"``.
        If a bool is provided, the verbosity is set to ``"WARNING"`` for False and to
        ``"INFO"`` for True. If None is provided, the verbosity of the logger is used.

    Notes
    -----
    Don't forget to close added file handlers by iterating on ``logger.handlers`` and
    calling ``handler.close()``.
    """
    handler = logging.FileHandler(fname, mode, encoding)
    handler.setFormatter(_LoggerFormatter())
    if verbose is not None:
        verbose = ensure_verbose(verbose)
        handler.setLevel(verbose)
    logger.addHandler(handler)


def set_log_level(verbose: bool | str | int | None) -> None:
    """Set the log level for the logger.

    Parameters
    ----------
    verbose : int | str | bool | None
        Sets the verbosity level. The verbosity increases gradually between
        ``"CRITICAL"``, ``"ERROR"``, ``"WARNING"``, ``"INFO"`` and ``"DEBUG"``. If
        ``None`` is provided, the verbosity is set to ``"WARNING"``. If a bool is
        provided, the verbosity is set to ``"WARNING"`` for ``False`` and to ``"INFO"``
        for ``True``.
    """
    verbose = ensure_verbose(verbose)
    logger.setLevel(verbose)


class _LoggerFormatter(logging.Formatter):
    """Format string syntax."""

    # Format string syntax for the different Log levels
    _formatters = {}
    _formatters[logging.DEBUG] = logging.Formatter(
        fmt="[%(module)s:%(funcName)s:%(lineno)d] %(levelname)s: %(message)s "
        "(%(asctime)s)"
    )
    _formatters[logging.INFO] = logging.Formatter(
        fmt="[%(module)s.%(funcName)s] %(levelname)s: %(message)s"
    )
    _formatters[logging.WARNING] = logging.Formatter(
        fmt="[%(module)s.%(funcName)s] %(levelname)s: %(message)s"
    )
    _formatters[logging.ERROR] = logging.Formatter(
        fmt="[%(module)s:%(funcName)s:%(lineno)d] %(levelname)s: %(message)s"
    )

    def __init__(self):
        super().__init__(fmt="%(levelname): %(message)s")

    def format(self, record: logging.LogRecord):  # noqa: A003
        """Format the received log record.

        Parameters
        ----------
        record : logging.LogRecord
        """
        if record.levelno <= logging.DEBUG:
            return self._formatters[logging.DEBUG].format(record)
        elif record.levelno <= logging.INFO:
            return self._formatters[logging.INFO].format(record)
        elif record.levelno <= logging.WARNING:
            return self._formatters[logging.WARNING].format(record)
        else:
            return self._formatters[logging.ERROR].format(record)


def verbose(f: Callable) -> Callable:
    """Set the verbose for the function call from the kwargs.

    Parameters
    ----------
    f : callable
        The function with a verbose argument.

    Returns
    -------
    f : callable
        The function.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        if "verbose" in kwargs:
            with _use_log_level(kwargs["verbose"]):
                return f(*args, **kwargs)
        else:
            return f(*args, **kwargs)

    return wrapper


class _use_log_level:  # noqa: N801
    """Context manager to change the logging level temporary.

    Parameters
    ----------
    verbose : int | str | bool | None
        Sets the verbosity level. The verbosity increases gradually between
        ``"CRITICAL"``, ``"ERROR"``, ``"WARNING"``, ``"INFO"`` and ``"DEBUG"``. If
        ``None`` is provided, the verbosity is set to ``"WARNING"``. If a bool is
        provided, the verbosity is set to ``"WARNING"`` for ``False`` and to ``"INFO"``
        for ``True``.
    """

    def __init__(self, verbose: bool | str | int | None = None):
        self._old_level = logger.level
        self._level = verbose

    def __enter__(self):
        set_log_level(self._level)

    def __exit__(self, *args):
        set_log_level(self._old_level)


def warn(
    message: str,
    category: type[Warning] = RuntimeWarning,
    module: str = _PACKAGE,
    ignore_namespaces: tuple[str, ...] | list[str] = (_PACKAGE,),
) -> None:
    """Emit a warning with trace outside the requested namespace.

    This function takes arguments like :func:`warnings.warn`, and sends messages
    using both :func:`warnings.warn` and :func:`logging.warn`. Warnings can be
    generated deep within nested function calls. In order to provide a
    more helpful warning, this function traverses the stack until it
    reaches a frame outside the ignored namespace that caused the error.

    This function is inspired from the MNE-Python package and behaves as a smart
    'stacklevel' argument.

    Parameters
    ----------
    message : str
        Warning message.
    category : type of Warning
        The warning class. Defaults to ``RuntimeWarning``.
    module : str
        The name of the module emitting the warning.
    ignore_namespaces : list of str | tuple of str
        Namespaces to ignore when traversing the stack.
    """
    if logging.WARNING < logger.level:
        return None
    root_dirs = [
        Path(import_module(namespace).__file__).parent
        for namespace in ignore_namespaces
    ]
    frame = inspect.currentframe()
    while frame:  # at some point it will be None and exit the loop
        fname = Path(frame.f_code.co_filename)
        if fname.parent.name == "tests":
            break  # treat tests as outside of the namespace
        lineno = frame.f_lineno
        if not (any(str(fname).startswith(str(rd)) for rd in root_dirs)):
            break
        frame = frame.f_back
    del frame
    # we need to use this instead of warn(message, category, stacklevel) because we
    # move out of our stack, so warnings won't properly recognize the module name
    # (and warnings.simplefilter will fail).
    warn_explicit(
        message,
        category,
        str(fname),
        lineno,
        module,
        globals().get("__warningregistry__", {}),
    )
    # now we emit the warning to the logger, except to the default StreamHandler on
    # stdout registered as the first handler.
    logger.handlers[0].setLevel(logging.WARNING + 1)
    logger.warning(message)
    logger.handlers[0].setLevel(0)


logger = _init_logger()
