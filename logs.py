import traceback
from functools import wraps
from typing import Callable
import os
import sys
import logging


def create_logger() -> str:
    """Create Logger function to setups logger for this file."""
    # Logging variables
    logger_name = "ticket_feeder_logger"
    script_name_bare = os.path.splitext(sys.argv[0])[0].replace("./", "")
    logfile_name = script_name_bare + ".log"
    logging_filename = logfile_name
    logging_level = logging.INFO
    # Logging Configuration
    log_format = "[%(asctime)s] - %(levelname) - 8s %(name) - -12s %(message)s"
    logging.basicConfig(
        level=logging_level,
        format=log_format,
        handlers=[logging.StreamHandler(), logging.FileHandler(logging_filename)],
    )
    return logger_name

def log_exception(func: Callable):
    """Logging declarator to ensure any exceptions seen are logged."""

    @wraps(func)
    def exception_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"There was a problem in {func.__name__}:\n{str(e)}")
            logger.error(traceback.format_exc())
            raise Exception(traceback.format_exc())

    return exception_wrapper


logger = logging.getLogger(create_logger())