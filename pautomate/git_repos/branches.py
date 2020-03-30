"""
Get branches informations of repositories in the current directory.
"""
import glob
from os import pardir
from os import path
from typing import List
from typing import Optional

from pautomate.common.git import get_branches_info
from pautomate.common.git import hard_reset
from pautomate.common.git import reset_to_origin_develop
from pautomate.common.printing import print_green
from pautomate.common.printing import print_red
from pautomate.common.printing import print_yellow


def get_branches(
        working_directory: str,
        reset_mode: bool,
        develop: bool,
        args: Optional[List[str]],
) -> None:
    """Get branches info

    Arguments:
        working_directory {str} -- path to the projects
        reset_mode {bool} -- reset --hard repository
        develop_mode {bool} -- checkout develop && reset --hard origin/develop
        args {[str]} -- projects name (full/partial)
    """
    repos = []
    for repo in glob.iglob(f'{working_directory}/**/**/.git', recursive=True):
        repo_path = path.abspath(path.join(repo, pardir))
        repos.append(repo_path)

    if reset_mode:
        print_red('Reset mode is enabled')

    if develop:
        print_red('Reset develop is enabled')

    if args:
        repos = set(
            repo for repo in repos
            if any(arg in repo for arg in args)
        )

    for repo_path in repos:
        print_green(repo_path)
        if reset_mode:
            print_yellow(hard_reset(repo_path))
        if develop:
            print_yellow(reset_to_origin_develop(repo_path))
        print(get_branches_info(repo_path))
