# -*- coding: utf-8 -*-
"""
Run dotnet services in parallel via dotnet core CLI
"""
from typing import List, Optional

from ..common.colorize import print_red, print_yellow
from ..common.logger import logger, pass_logger
from ..common.read import read_configs
from ..common.services import start_service


@pass_logger(logger)
def dotnet_exec(working_directory: str, command: str, watch_mode: bool, args: Optional[List[str]]):
    """Execute dotnet command

    Arguments:
        working_directory {str} -- path to the projects
        command {str} -- [run, test, restore, build, clean]
        watch_mode {bool} -- watch code changes
        args {[str]} -- projects name (full/partial)
    """
    configs = read_configs(working_directory)
    dotnet_projects = configs.get('dotnet_projects')

    if watch_mode:
        logger.info('Watch mode enabled')
        print_yellow('Watch mode enabled')

    if args:
        dotnet_projects = list(filter(lambda pro: any(
            [arg in pro for arg in args]), dotnet_projects))
        logger.info('Chosen dotnet projects: %r', dotnet_projects)

    try:
        for dotnet_project in dotnet_projects:
            start_service(working_directory, dotnet_project,
                          command, watch_mode)
    except TypeError:
        logger.error('No dotnet projects were configured in ./config.json')
        print_red('No dotnet projects were configured in ./config.json')
