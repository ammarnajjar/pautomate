"""
Get latest stable release of repositories in the current directory.
"""
from os.path import basename

from typing import List
from typing import Optional

from pautomate.common.get_repos import get_repos, filter_repos
from pautomate.common.git import get_lastest_stable_release
from pautomate.common.printing import print_green
from pautomate.common.printing import print_red
from pautomate.common.printing import print_yellow


def get_releases(
        working_directory: str,
        args: Optional[List[str]],
) -> None:
    """Get stale releases

    Arguments:
        working_directory {str} -- path to the projects
        args {[str]} -- projects name (full/partial)
    """
    repos = get_repos(working_directory)

    if args:
        repos = filter_repos(repos, args)

    for repo_path in repos:
        print(f'{basename(repo_path)}: {get_lastest_stable_release(repo_path)}')

