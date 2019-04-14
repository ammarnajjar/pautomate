# -*- coding: utf-8 *-
"""
Read JSON configurations
"""
import json
from typing import Dict, List, Union

from ..common.logger import logger, pass_logger


@pass_logger(logger)
def read_configs(config_path: str) -> Dict[str, Union[List[str], str, None]]:
    """Read JSON configurations

    Arguments:
        config_path {str} -- path to the config.json file

    Returns:
        Dict[str, str] -- parsed configurations as a dict
    """
    configs: Dict[str, Union[List[str], str, None]] = {}
    try:
        with open(f'{config_path}/config.json', 'r') as config_file:
            configs = json.loads(config_file.read())
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        logger.error('config.json cannot be read or found')
    return configs
