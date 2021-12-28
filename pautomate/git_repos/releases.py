"""
Get latest stable release of repositories in the current directory.
"""
from multiprocessing import Manager
from multiprocessing import Pool
from typing import Dict
from typing import List
from typing import Optional

from pautomate.common.get_repos import filter_list
from pautomate.common.get_repos import get_repos
from pautomate.common.git import get_lastest_stable_release


def get_releases(
        working_directory: str,
        filter_args: Optional[List[str]],
) -> None:
    """Get latest stale releases

    Arguments:
        working_directory {str} -- path to the projects
        filter_args {[str]} -- projects name (full/partial)
    """
    repos = get_repos(working_directory)

    if filter_args:
        repos = filter_list(repos, filter_args)

    manager = Manager()
    summery_info: Dict[str, str] = manager.dict()

    pool = Pool(processes=8)
    for repo_path in repos:
        pool.apply_async(
            get_lastest_stable_release, args=(repo_path, summery_info),
        )
    pool.close()
    pool.join()

    for repo_name, release in summery_info.items():
        print(f'{repo_name}: {release}')
