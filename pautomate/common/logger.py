# -*- coding: utf-8 *-
"""
Custom logger
"""
import functools
import logging
import os

from .logjson import filelogger

LOGS_FILENAME = 'pautimate.log'
LOGS_DIR = '.logs'
if not os.path.isdir(os.path.join(os.getcwd(), LOGS_DIR)):
    os.mkdir(LOGS_DIR)

logger = filelogger(
    __name__,
    [
        'levelname',
        'asctime',
        'name',
        'lineno',
    ],
    filename=os.path.join(LOGS_DIR, LOGS_FILENAME),
    level=logging.DEBUG,
)


def pass_logger(logger: filelogger):
    """Pass Logger decorator
    When used with a function, it changes the
    name of the logger (singleton) to match
    the name of the function temporarly, then
    it restore it to its original value.

    Arguments:
        logger: {filelogger}
    """
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            save_logger_name = logger.name
            logger.name = func.__name__
            result = func(*args, **kwargs)
            logger.name = save_logger_name
            return result
        return inner
    return wrapper
