# -*- coding: utf-8 -*-
"""CLI for pautomate."""
from os import getcwd

import click

from pautomate.common.printing import print_green
from pautomate.common.timeit import timeit
from pautomate.git_repos.branches import get_branches
from pautomate.git_repos.fetch_gitlab import fetch_gitlab
from pautomate.multi_dotnet.dotnet_exec import dotnet_exec

ROOT = getcwd()


class WorkingDirectory:
    """
    Target working directory, shared between sub-commands
    """

    def __init__(self):
        self.path = ROOT


PASS_WORKING_DIRECTORY = click.make_pass_decorator(
    WorkingDirectory, ensure=True,
)


@click.group()
@click.option(
    '-t', '--target', type=click.Path(), default=ROOT,
    help='[.] Target workspace.',
)
@PASS_WORKING_DIRECTORY
def cli(working_directory, target):
    """Console interface for pautomate"""
    working_directory.path = target


@cli.command()
@click.option('-r', '--reset', is_flag=True, default=False, help='reset --hard')
@click.option('-d', '--develop', is_flag=True, default=False, help='checkout develop && reset --hard origin/develop')
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@PASS_WORKING_DIRECTORY
@timeit(print_green)
def branches(working_directory, reset, develop, args):
    """
    Get branches infos in the local workspace

    Arguments:

        - args {[str]} -- projects name (full/partial)
    """
    get_branches(working_directory.path, reset, develop, args)


@cli.command()
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@PASS_WORKING_DIRECTORY
@timeit(print_green)
def fetch(working_directory, args):
    """
    Clone/fetch projects from Gitlab using the private token

    Arguments:

        - args {[str]} -- projects name (full/partial)

    NOTE:
    The gitlab url, token should be provided in a config.json
    file, which should exist in the current working direcotry.
    """
    fetch_gitlab(working_directory.path, args)


@cli.command()
@click.option('-w', '--watch', is_flag=True, default=False, help='Run in watch mode')
@click.argument('command', type=click.STRING)
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@PASS_WORKING_DIRECTORY
def dotnet(working_directory, command, watch, args):
    """
    Run dotnet services in parallel via dotnet core CLI

    Arguments:

        - command {str} -- [run, test, restore, build, clean]

        - args {[str]} -- projects name (full/partial)
    """
    dotnet_exec(working_directory.path, command, watch, args)
