# -*- coding: utf-8 *-
"""
Custom logger
"""
import functools
import logging

from . import logjson

logger = logjson.streamlogger(
    __name__,
    [
        'levelname',
        'asctime',
        'name',
        'lineno',
    ],
    level=logging.DEBUG,
)


def pass_logger(logger: logjson.streamlogger):
    """Pass Logger decorator
    When used with a function, it changes the
    name of the logger (singleton) to match
    the name of the function temporarly, then
    it restore it to its original value.

    Arguments:
        logger: {streamlogger}
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
