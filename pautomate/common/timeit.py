# -*- coding: utf-8 *-
"""
Timing Decorator
"""
import functools
import time

from .logger import logger, pass_logger

logger.name = __name__


@pass_logger(logger)
def timeit(printing_func):
    """Timing Decorator

    Arguments:
        printing_func {Function} -- printing function to show the result
    """
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            start = time.time()
            logger.debug(f'start time for {func.__name__}: {start}')
            result = func(*args, **kwargs)
            end = time.time()
            logger.debug(f'end time for {func.__name__}: {end}')
            time_elapsed = end - start
            printing_func(f'Time needed = {time_elapsed:.2f} seconds.')
            logger.info(f'Time needed = {time_elapsed:.2f} seconds.')
            return result
        return inner
    return wrapper
