
# -*- coding: utf-8 *-
"""
Custom Printing functions
"""


def print_green(text: str) -> None:
    """Print in Green

    Arguments:
        text {str} -- Text to print
    """
    print(f'\033[92m* {text}\033[0m')


def print_red(text: str) -> None:
    """Print in Red

    Arguments:
        text {str} -- Text to print
    """
    print(f'\033[91m* {text}\033[0m')


def print_yellow(text: str) -> None:
    """Print in Yellow

    Arguments:
        text {str} -- Text to print
    """
    print(f'\033[93m* {text}\033[0m')
