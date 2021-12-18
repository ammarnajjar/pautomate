"""
Get repositories in the current directory.
"""
import glob
from os import pardir
from os import path
from typing import List, Set


def get_repos(working_directory: str) -> List[str]:
    return [path.abspath(path.join(repo, pardir))
            for repo in glob.iglob(f'{working_directory}/**/**/.git', recursive=True)]

def filter_repos(repos: List[str], filter: str) -> Set[str]:
    return set(repo for repo in repos
            if any(arg in repo for arg in filter))

