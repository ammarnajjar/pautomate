# -*- coding: utf-8 *-
"""
Execute dotnet projects in parallel separate processes
"""
import glob
import shlex
import subprocess
from multiprocessing import Process
from os import path
from typing import List

from .printing import print_green


def run(project: str, command_type: str, watch_mode: bool):
    """Execute dotnet command

    Arguments:
        project {str} -- project name
        command_type {str} -- [run, test, restore, build, clean]
        watch_mode {bool} -- watch code changes
    """
    command: List[str] = []
    if command_type in ['run']:
        command = shlex.split(f'dotnet {command_type} -p {project}')
        if watch_mode:
            command = shlex.split(f'dotnet watch -p {project} {command_type}')
    else:
        command = shlex.split(f'dotnet {command_type} {project}')

    process = subprocess.Popen(command)
    process.communicate(input=None)


def start_service(working_directory: str, service_name: str, command: str, watch_mode: bool):
    """Start process container

    Arguments:
        working_directory {str} -- path to the projects
        command {str} -- [run, test, restore, build, clean]
        watch_mode {bool} -- watch code changes
        args {[str]} -- projects name (full/partial)
    """
    repo_path = path.join(working_directory, service_name)
    test_projects = list(
        filter(lambda pro: 'test' in pro.lower(), glob.iglob(f'{repo_path}/**/*.csproj', recursive=True)))
    runnable_projects = list(
        filter(lambda pro: 'test' not in pro.lower(), glob.iglob(f'{repo_path}/**/*.csproj', recursive=True)))

    exec_pros: List[str] = []
    if command == 'test':
        exec_pros = test_projects
    else:
        exec_pros = runnable_projects

    for project in exec_pros:
        print_green(service_name)
        job = Process(target=run, args=(project, command, watch_mode))
        job.start()
