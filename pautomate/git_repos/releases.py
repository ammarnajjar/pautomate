"""
Get latest stable release of repositories in the current directory.
"""
from os.path import basename
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

    for repo_path in repos:
        latest_stable_release = get_lastest_stable_release(repo_path)
        if latest_stable_release != '':
            print(f'{basename(repo_path)}: {latest_stable_release}')
