"""
=======
Logging
=======

This package uses the logging module.
"""

#%%
# The logger and its utilities can be imported from the package namespace.

from tempfile import NamedTemporaryFile

from template import add_file_handler, logger, set_log_level

# sphinx_gallery_thumbnail_path = '_static/logging/flowchart-light.png'

#%%
# The logger can be used to send logs at different levels:
# DEBUG, INFO, WARNING, ERROR and CRITICAL.
# If the logger level is at least equal to the emitted report level, the log is
# displayed. Else, it is omitted.

logger.debug("This is a debug log that will not be displayed.")
logger.warning("This is a warning log that will be displayed.")

#%%
# The function `~template.set_log_level` can be used to edit the level the
# logger.

set_log_level("DEBUG")
logger.debug("This is a debug log that will now be displayed.")

#%%
# Additional handler can be added with `~template.add_stream_handler` and
# `~template.add_file_handler`. For instance, logs can be saved to a file.
#
# .. note::
#
#     For the purpose of this example, a temporary file is used. Logs can be
#     saved to any text file, e.g. a ``.txt`` or ``.log`` file.

file = NamedTemporaryFile(mode="w")
add_file_handler(file.name, verbose="INFO")
logger.debug(
    "This is a debug log that will not be saved to file but will be displayed."
)
logger.info(
    "This is an info log that will both be displayed and saved to file."
)

#%%
# We can check the content of the log file:

with open(file.name, "r") as f:
    lines = f.readlines()
for line in lines:
    print (line)

#%%
# There are 2 log levels to distinct, logger and handlers, which control if a
# message is emitted or not. A message level must be equal or above both the
# logger and the handler level to be emitted on a specific handler.
#
# .. figure:: ../../_static/logging/flowchart-light.png
#     :class: only-light
#
# .. figure:: ../../_static/logging/flowchart-dark.png
#     :class: only-dark
#
# More information on the `Python logging documentation <pyLogging_>`_.
#
# .. _pyLogging: https://docs.python.org/3/library/logging.html
