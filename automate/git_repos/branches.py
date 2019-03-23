# -*- coding: utf-8 *-
"""
Get branches informations of repositories in the current directory.
"""
import glob
from os import pardir, path

from automate.common.git import hard_reset, print_branches_info
from automate.common.printing import print_green, print_red


def get_branches(working_directory, reset_mode, args) -> None:
    """Get branches info

    Arguments:
        working_directory {str} -- path to the projects
        reset_mode {bool} -- reset --hard repository
        args {[str]} -- projects name (full/partial)
    """
    repos = []
    for repo in glob.iglob(f'{working_directory}/**/.git', recursive=True):
        repo_path = path.abspath(path.join(repo, pardir))
        repos.append(repo_path)

    if reset_mode:
        print_red('Reset mode enabled')

    if args:
        repos = list(filter(lambda repo: any(
            [arg in repo for arg in args]), [path.basename(repo) for repo in repos]))

    for repo_path in repos:
        print_green(repo_path)
        if reset_mode:
            hard_reset(repo_path)
        print_branches_info(repo_path)
