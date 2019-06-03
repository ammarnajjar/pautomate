# -*- coding: utf-8 -*-
"""
Clone/Fetch repositories from GitLab using personal token
"""
import json
import sys
from multiprocessing import Manager
from multiprocessing import Pool
from typing import Dict
from typing import List
from typing import Optional
from urllib.request import urlopen

from ..common.colorize import print_red
from ..common.colorize import print_yellow
from ..common.git import fetch_repo
from ..common.logger import logger
from ..common.logger import pass_logger
from ..common.read import read_configs


@pass_logger(logger)
def fetch_gitlab(working_directoy: str, args: Optional[List[str]]) -> None:
    """Clone/Fetch from GitLab

    Arguments:
        working_directoy {str} -- target workspace
        args {[str]} -- projects name (full/partial)
    """
    configs = read_configs(working_directoy)
    gitlab_url = configs.get('gitlab_url')
    gitlab_token = configs.get('gitlab_token')
    if not(gitlab_url and gitlab_token):
        logger.error('No gitlab configs are provided in config.json')
        print_red('Please provide gitlab configs in your config.json')
        sys.exit(1)

    projects = urlopen(
        f'https://{gitlab_url}/api/v4/projects?membership=1&order_by=path&per_page=1000&private_token={gitlab_token}',
    )
    all_projects = json.loads(projects.read().decode())
    logger.debug('All projects list:')
    for pro in all_projects:
        logger.debug(pro.get('path_with_namespace'))

    if args:
        all_projects = list(filter(
            lambda pro: any(
                [arg in pro.get('name') for arg in args],
            ), all_projects,
        ))
        logger.debug(f'all projects: {all_projects}')

    ignore_list = configs.get('ignore_list')
    if isinstance(ignore_list, List):
        all_projects = list(filter(
            lambda pro: all(
                [
                    ignored_repo not in pro.get('name')
                    for ignored_repo in ignore_list
                ],
            ), all_projects,
        ))
        logger.debug(f'projects after ignore list: {all_projects}')

    manager = Manager()
    summery_info: Dict[str, str] = manager.dict()

    processes_count = 8
    logger.debug(f'using ({processes_count}) processes')
    pool = Pool(processes=processes_count)
    for project in all_projects:
        logger.debug(f'project: {project}')
        url = project.get('ssh_url_to_repo')
        name = project.get('name').replace(' ', '-').replace('.', '-')
        pool.apply_async(
            fetch_repo, args=(
                working_directoy, name, url, summery_info,
            ),
        )
    pool.close()
    pool.join()

    for repo_name, current_branch in summery_info.items():
        logger.warning(f'{repo_name} => {current_branch}')
        print_yellow(f'{repo_name} => {current_branch}')
