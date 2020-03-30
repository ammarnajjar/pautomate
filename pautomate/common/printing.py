"""
Custom Printing functions
"""
import functools


def with_color(color_code: str):
    """Coloring decorator

    Arguments:
        color_code {str} -- e.g.: '\033[91m'
    """
    def wrapper(func):
        @functools.wraps(func)
        def inner(args):
            result = func(f'{color_code}{args}\033[0m')
            return result
        return inner
    return wrapper


print_red = with_color('\033[91m* ')(print)
print_green = with_color('\033[92m* ')(print)
print_yellow = with_color('\033[93m* ')(print)
