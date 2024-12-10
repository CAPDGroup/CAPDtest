import logging
import os
import json

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

    workdir = config['root']
    capddir = f'{workdir}/{config["targets"]["CAPD"]["local_url"]}'
    builddir = f'{capddir}/{config["builddir"]}'
    installdir = os.path.abspath(f'{workdir}/{config["installdir"]}')

    setup_library(workdir, capddir, builddir, installdir, config)

    exampledir = f'{workdir}/CAPD.example.1'
    example_builddir = f'{exampledir}/build'

    setup_example_1(workdir, exampledir, example_builddir, installdir, config)

    example2_dir = f'{workdir}/CAPD.example.2'
    example2_builddir = f'{example2_dir}/build'

    setup_example_2(workdir, example2_dir, example2_builddir, config)

    project_starter_dir = f'{capddir}/capdMake/examples/projectStarter'
    setup_project_starter(project_starter_dir, config)
