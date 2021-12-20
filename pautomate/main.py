"""CLI for pautomate. """
import argparse
import sys
from os import getcwd
from typing import Optional
from typing import Sequence

from pautomate.common.printing import print_green
from pautomate.common.timeit import timeit
from pautomate.git_repos.branches import get_branches
from pautomate.git_repos.fetch_gitlab import fetch_gitlab
from pautomate.git_repos.releases import get_releases
from pautomate.multi_dotnet.dotnet_exec import dotnet_exec


def _add_target_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        '-t', '--target',
        default=getcwd(),
        required=False,
        dest='target',
        help='[.] Target workspace',
    )


def _add_reset_flag(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        '-r', '--reset',
        action='store_true',
        required=False,
        help='reset --hard',
    )


def _add_develop_flag(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        '-d', '--develop',
        action='store_true',
        required=False,
        help='checkout develop && reset --hard origin/develop',
    )


def _add_watch_flag(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        '-w', '--watch',
        action='store_true',
        required=False,
        help='watch for changes',
    )


def _add_command_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        'command',
        metavar='command',
        nargs=1,
        choices=['run', 'test', 'restore', 'build', 'clean'],
        help='dotnet command',
    )


def _add_pros_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        'pros',
        metavar='pros',
        nargs='*',
        default=None,
        help='project names to filter',
    )


@timeit(print_green)
def releases():
    """
    Get latest stable releases in the local workspace

    Arguments:

        - pros {[str]} -- projects name (full/partial)
    """
    parser = argparse.ArgumentParser(
        description='Get lastest stable releases in the local workspace',
    )
    _add_target_option(parser)
    _add_pros_option(parser)

    _args = parser.parse_args()
    return get_releases(
        _args.target,
        _args.pros,
    )


@timeit(print_green)
def branches():
    """
    Get branches infos in the local workspace

    Arguments:

        - pros {[str]} -- projects name (full/partial)
    """
    parser = argparse.ArgumentParser(
        description='Get branches infos in the local workspace',
    )
    _add_target_option(parser)
    _add_reset_flag(parser)
    _add_develop_flag(parser)
    _add_pros_option(parser)

    _args = parser.parse_args()
    return get_branches(
        _args.target,
        _args.reset,
        _args.develop,
        _args.pros,
    )


@timeit(print_green)
def fetch():
    """
    Clone/fetch projects from Gitlab using the private token

    Arguments:

        - pros {[str]} -- projects name (full/partial)

    NOTE:
    The gitlab url, token should be provided in a config.json
    file, which should exist in the current working direcotry.
    """
    parser = argparse.ArgumentParser(
        description='Clone/fetch projects from Gitlab using the private token',
    )
    _add_target_option(parser)
    _add_pros_option(parser)

    _args = parser.parse_args()
    return fetch_gitlab(_args.target, _args.pros)


def dotnet():
    """
    Run dotnet services in parallel via dotnet core CLI

    Arguments:

        - command {str} -- [run, test, restore, build, clean]

        - args {[str]} -- projects name (full/partial)
    """
    parser = argparse.ArgumentParser(
        description='Clone/fetch projects from Gitlab using the private token',
    )
    _add_target_option(parser)
    _add_watch_flag(parser)
    _add_command_option(parser)
    _add_pros_option(parser)

    _args = parser.parse_args()
    dotnet_exec(
        _args.target,
        _args.command[0],
        _args.watch,
        _args.pros,
    )


def main(argv: Optional[Sequence[str]] = None) -> None:
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(description='Automate my boring stuff')
    subparsers = parser.add_subparsers(dest='cmd')

    fetch_parser = subparsers.add_parser(
        'fetch',
        help='Clone/fetch projects from Gitlab using the private token',
    )
    _add_target_option(fetch_parser)
    _add_pros_option(fetch_parser)

    releases_parser = subparsers.add_parser(
        'releases',
        help='Get lastest stable releases in the local workspace',
    )
    _add_target_option(releases_parser)
    _add_pros_option(releases_parser)

    branches_parser = subparsers.add_parser(
        'branches',
        help='Get branches infos in the local workspace',
    )
    _add_target_option(branches_parser)
    _add_reset_flag(branches_parser)
    _add_develop_flag(branches_parser)
    _add_pros_option(branches_parser)

    dotnet_parser = subparsers.add_parser(
        'dotnet',
        help='operate on dotnet projects',
    )
    _add_target_option(dotnet_parser)
    _add_watch_flag(dotnet_parser)
    _add_command_option(dotnet_parser)
    _add_pros_option(dotnet_parser)

    main_args = parser.parse_args(argv)
    if main_args.cmd == 'fetch':
        return fetch_gitlab(main_args.target, args=main_args.pros)
    elif main_args.cmd == 'releases':
        return get_releases(
            main_args.target,
            main_args.pros,
        )
    elif main_args.cmd == 'branches':
        return get_branches(
            main_args.target,
            main_args.reset,
            main_args.develop,
            main_args.pros,
        )
    elif main_args.cmd == 'dotnet':
        return dotnet_exec(
            main_args.target,
            main_args.command[0],
            main_args.watch,
            main_args.pros,
        )


if __name__ == '__main__':
    main()
