"""
Clone/Fetch repositories from GitLab using personal token
"""
import json
import os
import sys
from multiprocessing import Manager
from multiprocessing import Pool
from typing import Dict
from typing import List
from typing import Optional
from urllib.request import urlopen
from urllib.error import URLError
from pautomate.common.git import fetch_repo
from pautomate.common.printing import print_green
from pautomate.common.printing import print_yellow
from pautomate.common.printing import print_red
from pautomate.common.read import read_configs


def cache_repos(all_projects: List[str]) -> None:
    print('caching repos on disk');
    repos_file = 'repos'
    try:
        os.remove(f'{repos_file}_bk')
    except(FileNotFoundError):
        pass
    try:
        os.rename(repos_file, f'{repos_file}_bk')
    except(FileNotFoundError):
        pass
    with open(repos_file, 'x') as fi:
        for project in all_projects:
            repo_path = project.get('path_with_namespace').replace(' ', '-').replace('.', '-')
            fi.write(f'{repo_path}\n')


def get_repos_from_gitlab(working_directoy: str, args: Optional[List[str]])-> List[str]:
    configs = read_configs(working_directoy)
    gitlab_url = configs.get('gitlab_url')
    gitlab_token = configs.get('gitlab_token')
    if not(gitlab_url and gitlab_token):
        print('Please provide gitlab configs in your config.json')
        sys.exit(1)

    try:
        projects = urlopen(
            f'https://{gitlab_url}/api/v4/projects?membership=1&order_by=path&per_page=1000&private_token={gitlab_token}',  # noqa
        )
    except(URLError):
        print_red('No route to gitlab, check your internet/VPN connection')
        exit(1)
    all_projects = json.loads(projects.read().decode())

    if args:
        all_projects = [
            pro for pro in all_projects
            if any(arg in pro.get('path_with_namespace') for arg in args)
        ]

    ignore_list = configs.get('ignore_list')
    if isinstance(ignore_list, List):
        all_projects = [
            pro for pro in all_projects
            if all(
                ignored_repo not in pro.get('path_with_namespace')
                for ignored_repo in ignore_list
            )
        ]
    print(all_projects)
    return all_projects

def fetch_gitlab(working_directoy: str, args: Optional[List[str]]) -> None:
    """Clone/Fetch from GitLab

    Arguments:
        working_directoy {str} -- target workspace
        args {[str]} -- projects name (full/partial)
    """
    all_projects = get_repos_from_gitlab(working_directoy, args)
    cache_repos(all_projects)

    manager = Manager()
    summery_info: Dict[str, str] = manager.dict()

    pool = Pool(processes=8)
    for project in all_projects:
        url = project.get('ssh_url_to_repo')
        repo_path = project.get('path_with_namespace')
        repo_path = repo_path.replace(' ', '-').replace('.', '-')
        pool.apply_async(
            fetch_repo, args=(
                working_directoy, repo_path, url, summery_info,
            ),
        )
    pool.close()
    pool.join()

    print('==============')
    print_green('Summery:')
    for repo_name, current_branch in summery_info.items():
        print_yellow(f'{repo_name} => {current_branch}')
