# -*- coding: utf-8 *-
"""
Run Git commands in separate processes
"""
import shlex
import subprocess
from os import path
from typing import Dict

from ..common.logger import logger, pass_logger


def shell(command: str) -> str:
    """Execute shell command

    Arguments:
        command {str} -- to execute in shell

    Returns:
        str -- output of the shell
    """
    cmd = shlex.split(command)
    output_lines = subprocess.check_output(cmd).decode("utf-8").split('\n')
    return [line.strip() for line in output_lines if line]


def shell_first(command: str) -> str:
    """Execute in shell

    Arguments:
        command {str} -- to execute in shell

    Returns:
        str -- first line of output
    """
    cmd = shlex.split(command)
    return subprocess.check_output(cmd).decode("utf-8").split('\n')[0]


def hard_reset(repo_path: str) -> str:
    """reset --hard

    Arguments:
        repo_path {str} -- path to repo to reset
    """
    return shell(f'git -C {repo_path} reset --hard')


def get_branches_info(repo_path: str) -> str:
    """git branch -a

    Arguments:
        repo_path {str} -- path to repo
    """
    return shell(f'git -C {repo_path} branch -a')


@pass_logger(logger)
def fetch_repo(working_directory: str, name: str, url: str, summery_info: Dict[str, str]) -> None:
    """Clone / Fetch repo

    Arguments:
        working_directory {str} -- target directory
        name {str} -- repo name
        url {str} -- repo url in gitlab
        summery_info {Dict[str, str]} -- the result of the cloning/fetching
    """
    repo_path = path.join(working_directory, name)
    if path.isdir(repo_path):
        logger.info(f'Fetching {name}')
        shell_first(f'git -C {repo_path} fetch')
        remote_banches = shell_first(f'git -C {repo_path} ls-remote --heads')
        current_branch = shell_first(
            f'git -C {repo_path} rev-parse --abbrev-ref HEAD --')
        if f'refs/heads/{current_branch}' in remote_banches:
            shell_first(
                f'git -C {repo_path} fetch -u origin {current_branch}:{current_branch}')
        else:
            logger.warning(f'{current_branch} does not exist on remote')

        if ('refs/heads/develop' in remote_banches and current_branch != 'develop'):
            shell_first(f'git -C {repo_path} fetch origin develop:develop')
    else:
        logger.info(f'Cloning {name}')
        shell_first(f'git clone {url} {name}')
        current_branch = shell_first(
            f'git -C {repo_path} rev-parse --abbrev-ref HEAD --')
    summery_info.update({name: current_branch})
