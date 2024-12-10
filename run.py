import logging
import os
import json

from internal import setup_workdir
from internal import setup_library
from internal import setup_example_1
from internal import setup_example_2
from internal import setup_project_starter

if __name__ == '__main__':

    file_path = 'config.json'

    with open(file_path, 'r') as file:
        config = json.load(file)

    logging.basicConfig(level=config['logging_level'])

    if config['dry_run']:
        logging.info("Performing dry run...")

    setup_workdir(config)
    setup_library(config)
    setup_example_1(config)
    setup_example_2(config)

    workdir = os.path.abspath(config['root'])
    capddir = f'{workdir}/{config["targets"]["CAPD"]["local_url"]}'
    project_starter_dir = f'{capddir}/capdMake/examples/projectStarter'
    setup_project_starter(project_starter_dir, config)
