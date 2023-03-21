"""
=======
Logging
=======

This package uses the logging module.
"""

#%%
# The logger and its utilities can be imported from the package namespace.

import logging
from pathlib import Path
from tempfile import TemporaryDirectory

from template import add_file_handler, logger, set_log_level

# sphinx_gallery_thumbnail_path = '_static/logging/flowchart-light.png'

#%%
# The logger can be used to send logs at different levels:
# ``DEBUG``, ``INFO``, ``WARNING``, ``ERROR`` and ``CRITICAL``. Each of this
# level is equal to an integer value. If the logger level is at least equal to
# the emitted report level, the log is displayed. Else, it is omitted. By
# default, the logger is set to the ``WARNING`` level.

print (f"The level 'INFO' corresponds to the value {logging.INFO}.")
print (f"The level 'ERROR' corresponds to the value {logging.ERROR}.")
logger.debug("This is a debug log that will not be displayed.")
logger.warning("This is a warning log that will be displayed.")

#%%
# The function `~template.set_log_level` can be used to edit the level of the
# logger.

set_log_level("DEBUG")
logger.debug("This is a debug log that will now be displayed.")

#%%
# By default, the logger has one `~logging.StreamHandler` which outputs in
# ``sys.stdout``. The level of both the logger and of this first handler can be
# changed with `~template.set_log_level`.
# Additional file handlers can be added with `~template.add_file_handler`.
# Each handler can be set to a different level than the logger (and than the
# first `~logging.StreamHandler`).
#
# .. note::
#
#     For the purpose of this example, a temporary file is used. Logs can be
#     saved to any text file, e.g. a ``.txt`` or ``.log`` file.

directory = TemporaryDirectory()
file = Path(directory.name) / "mylogs.log"
add_file_handler(file, verbose="INFO")  # different level than the logger
logger.debug(
    "This is a debug log that will not be saved to file but will be displayed."
)
logger.info(
    "This is an info log that will both be displayed and saved to file."
)

#%%
# Since the file handler we added is set to the ``INFO`` level, it should
# capture only the second log.

with open(file, "r") as f:
    lines = f.readlines()
for line in lines:
    print (line)

#%%
# A message level must be equal or above both the logger and the handler level
# to be emitted on a specific handler. More information on the
# `Python logging documentation <pyLogging_>`_ and on the flowchart below:
#
# .. figure:: ../../_static/logging/flowchart-light.png
#     :class: only-light
#
# .. figure:: ../../_static/logging/flowchart-dark.png
#     :class: only-dark
#
# .. _pyLogging: https://docs.python.org/3/library/logging.html
