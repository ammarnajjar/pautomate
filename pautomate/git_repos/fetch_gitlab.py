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

from pautomate.common.git import fetch_repo
from pautomate.common.printing import print_green
from pautomate.common.printing import print_yellow
from pautomate.common.read import read_configs


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
        print('Please provide gitlab configs in your config.json')
        sys.exit(1)

    projects = urlopen(
        f'https://{gitlab_url}/api/v4/projects?membership=1&order_by=path&per_page=1000&private_token={gitlab_token}',  # noqa
    )
    all_projects = json.loads(projects.read().decode())

    if args:
        all_projects = list(
            filter(
                lambda pro: any(
                    [arg in pro.get('name') for arg in args],
                ), all_projects,
            ),
        )

    ignore_list = configs.get('ignore_list')
    if isinstance(ignore_list, List):
        all_projects = list(
            filter(
                lambda pro: all(
                    [
                        ignored_repo not in pro.get('name')
                        for ignored_repo in ignore_list
                    ],
                ), all_projects,
            ),
        )

    manager = Manager()
    summery_info: Dict[str, str] = manager.dict()

    pool = Pool(processes=8)
    for project in all_projects:
        url = project.get('ssh_url_to_repo')
        name = project.get('name').replace(' ', '-').replace('.', '-')
        if '/api/' in url:
            name = f'api/{name}'
        pool.apply_async(
            fetch_repo, args=(
                working_directoy, name, url, summery_info,
            ),
        )
    pool.close()
    pool.join()

    print('==============')
    print_green('Summery:')
    for repo_name, current_branch in summery_info.items():
        print_yellow(f'{repo_name} => {current_branch}')
