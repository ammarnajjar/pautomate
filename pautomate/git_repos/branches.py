# -*- coding: utf-8 *-
"""
Get branches informations of repositories in the current directory.
"""
import glob
from os import pardir, path
from typing import List, Optional

from pautomate.common.git import get_branches_info, hard_reset

from ..common.colorize import YELLOW, colorize_lines, print_green, print_red
from ..common.logger import logger, pass_logger


@pass_logger(logger)
def get_branches(working_directory: str, reset_mode: bool, args: Optional[List[str]]) -> None:
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
    logger.debug(f'repos: {repos}')

    if reset_mode:
        logger.warning('Reset mode enabled')
        print_red('Reset mode enabled'.upper())

    if args:
        repos = list(filter(lambda repo: any(
            [arg in repo for arg in args]), [path.basename(repo) for repo in repos]))
        logger.debug(f'repos after filtering: {repos}')

    for repo_path in repos:
        logger.info(repo_path)
        print_green(repo_path)
        if reset_mode:
            stdout = hard_reset(repo_path)
            logger.warning(stdout)
            print_red(colorize_lines(YELLOW, stdout))
        stdout = get_branches_info(repo_path)
        logger.info(stdout)
        print(colorize_lines(YELLOW, stdout))
