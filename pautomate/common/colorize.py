# -*- coding: utf-8 *-
"""
Colorize text for stdout, stderr
"""
import functools
from typing import List

from .logger import logger, pass_logger

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
ENDING = '\033[0m'


@pass_logger(logger)
def colorize(color_code: str, text: str) -> str:
    """
    Add colors to text when showed on the command line
    Note that this works only for xterm conole, for it
    adds a prefix and a suffix to the text.

    Arguments:
        color_code {str} -- e.g.: for red '\033[91m'
        text {str}: text to colorize

    Return:
        {str}: a colored text for console output
    """
    logger.debug(f'coloring with {color_code}')
    logger.debug(f'text to colorize {text}')
    return f'{color_code}{text}{ENDING}'


@pass_logger(logger)
def colorize_lines(color_code: str, text: List[str]) -> str:
    """
    Joins muliline string into one, giving the line with
    a * different color.
    Note that this works only for xterm conole, for it
    adds a prefix and a suffix to the text.

    Arguments:
        color_code {str} -- e.g.: for red '\033[91m'
        text {List[str]}: lines to act on

    Return:
        {str}: a multilines colored text for console output
    """
    logger.debug(f'text to colorize {text}')
    output_lines = text
    for index, line in enumerate(text):
        if '*' in line:
            output_lines[index] = colorize(color_code, line)
    return '\n'.join(output_lines)


def with_color(color_code: str):
    """Coloring decorator

    Arguments:
        color_code {str} -- e.g.: for red '\033[91m'
    """
    def wrapper(func):
        @functools.wraps(func)
        def inner(args):
            result = func(colorize(color_code, args))
            return result
        return inner
    return wrapper


@with_color(RED)
def print_red(*args, **kwags):
    print(*args, **kwags)


@with_color(GREEN)
def print_green(*args, **kwags):
    print(*args, **kwags)


@with_color(YELLOW)
def print_yellow(*args, **kwags):
    print(*args, **kwags)
