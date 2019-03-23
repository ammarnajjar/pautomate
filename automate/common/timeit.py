
# -*- coding: utf-8 *-

"""
Timing Decorator
"""
import functools
import time


def timeit(print_func):
    """Timing Decorator

    Arguments:
        print_func {Function} -- printing function to show the result
    """
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            time_elapsed = end - start
            print_func(f'Time needed = {time_elapsed:.2f} seconds.')
            return result
        return inner
    return wrapper
