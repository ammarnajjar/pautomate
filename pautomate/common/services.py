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

from .colorize import print_green
from .logger import logger, pass_logger


@pass_logger(logger)
def run(project: str, command_type: str, watch_mode: bool, filter: bytes = b"Waiting for"):
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

    logger.debug(f'dotnet command: {command}')
    proc = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        while True:
            line = proc.stdout.readline()
            if line != b'' and filter not in line:
                print(line.rstrip().decode('utf-8'))
    except KeyboardInterrupt:
        logger.info(f'dotnet command {command} exited by KeyboardInterrupt')


@pass_logger(logger)
def start_service(working_directory: str, service_name: str, command: str, watch_mode: bool):
    """Start process container

    Arguments:
        working_directory {str} -- path to the projects
        command {str} -- [run, test, restore, build, clean]
        watch_mode {bool} -- watch code changes
        args {[str]} -- projects name (full/partial)
    """
    repo_path = path.join(working_directory, service_name)
    logger.debug(f'repo path: {repo_path}')
    test_projects = list(
        filter(lambda pro: 'test' in pro.lower(), glob.iglob(f'{repo_path}/**/*.csproj', recursive=True)))
    logger.debug(f'test projects: {test_projects}')
    runnable_projects = list(
        filter(lambda pro: 'test' not in pro.lower(), glob.iglob(f'{repo_path}/**/*.csproj', recursive=True)))
    logger.debug(f'runnable projects: {runnable_projects}')

    exec_pros: List[str] = []
    if command == 'test':
        exec_pros = test_projects
    else:
        exec_pros = runnable_projects

    logger.debug(f'projects to execute: {exec_pros}')
    for project in exec_pros:
        logger.info(f'service_name: {service_name}')
        print_green(service_name)
        job = Process(target=run, args=(project, command, watch_mode))
        job.start()
