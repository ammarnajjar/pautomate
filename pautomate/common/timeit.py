# -*- coding: utf-8 *-
"""
Timing Decorator
"""
import functools
import time


def timeit(logging_func):
    """Timing Decorator

    Arguments:
        logging_func {Function} -- printing function to show the result
    """
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            time_elapsed = end - start
            logging_func(f'Time needed = {time_elapsed:.2f} seconds.')
            return result
        return inner
    return wrapper
