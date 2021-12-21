"""
Get repositories in the current directory.
"""
import glob
from os import pardir
from os import path
from typing import List
from typing import Set


def get_repos(working_directory: str) -> List[str]:
    """get repos if already cached, else search recursivly in the directory

    Arguments:
        working_directoy {str} -- target workspace
    """
    try:
        with open('repos', 'r') as fo:
            repo_paths = [x.strip() for x in fo.read().strip().split('\n')]
        return repo_paths
    except(FileNotFoundError):
        return [
            path.abspath(path.join(repo, pardir))
            for repo in glob.iglob(f'{working_directory}/**/**/.git', recursive=True)
        ]


def filter_list(source: List[str], filter_args: str) -> Set[str]:
    """filter list items to contain fully or paritally specific text

    Arguments:
        source {List[str]} -- list to be filtered
        filter_args {str} -- the string for items to contain
    """
    return set(
        item for item in source
        if any(arg in item for arg in filter_args)
    )
