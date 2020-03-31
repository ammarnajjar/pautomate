"""
Run dotnet services in parallel via dotnet core CLI
"""
from typing import List
from typing import Optional

from pautomate.common.printing import print_red
from pautomate.common.printing import print_yellow
from pautomate.common.read import read_configs
from pautomate.common.services import start_service


def dotnet_exec(
    working_directory: str,
    command: str,
    watch_mode: bool,
    args: Optional[List[str]],
):
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
        print_yellow('Watch mode enabled')

    if args:
        dotnet_projects = [
            pro for pro in dotnet_projects
            if any(arg in pro for arg in args)
        ]

    try:
        for dotnet_project in dotnet_projects:
            start_service(
                working_directory,
                dotnet_project,
                command,
                watch_mode,
            )
    except TypeError:
        print_red('No dotnet projects were configured in ./config.json')
