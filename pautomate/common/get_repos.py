"""
Get repositories in the current directory.
"""
import glob
from os import pardir
from os import path
from typing import List, Set


def get_repos(working_directory: str) -> List[str]:
    """get repos if already cached, else search recursivly

    Arguments:
        working_directoy {str} -- target workspace
    """
    try:
        with open('repos', 'r') as fo:
            repo_paths = [x.strip() for x in fo.read().strip().split('\n')]
        return repo_paths
    except(FileNotFoundError):
        return [path.abspath(path.join(repo, pardir))
                for repo in glob.iglob(f'{working_directory}/**/**/.git', recursive=True)]

def filter_repos(repos: List[str], filter: str) -> Set[str]:
    return set(repo for repo in repos
            if any(arg in repo for arg in filter))

