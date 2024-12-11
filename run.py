import logging
import os

from internal import setup_workdir
from internal import setup_project_starter

from internal import execute_stage_executable
from internal import execute_stage_library

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    dry_run = True
    incremental_run = True
    workspace_root = os.path.abspath('./workdir')
    build_dir = 'build'
    install_dir = f'{workspace_root}/CAPD_install'
    jobs = 3

    if dry_run:
        logging.info("Performing dry run...")

    setup_workdir(workspace_root, dry_run, incremental_run)

    execute_stage_library(
        workspace_root=workspace_root,
        remote_url='https://github.com/CAPDGroup/CAPD',
        local_dir='CAPD',
        build_dir=build_dir,
        cmake_options=['-DCAPD_BUILD_ALL=ON', f'-DCMAKE_INSTALL_PREFIX={install_dir}'],
        jobs=jobs,
        dry_run=dry_run)
    
    execute_stage_executable(
        workspace_root=workspace_root,
        remote_url='https://github.com/CAPDGroup/CAPD_example_standalone',
        local_dir='CAPD_example_standalone',
        build_dir=build_dir,
        cmake_options=[],
        executable_args=['./capd_example'],
        jobs=jobs,
        dry_run=dry_run)

    execute_stage_executable(
        workspace_root=workspace_root,
        remote_url='https://github.com/CAPDGroup/CAPD_example_standard',
        local_dir='CAPD_example_standard',
        build_dir=build_dir,
        cmake_options=[f'-DCMAKE_PREFIX_PATH={install_dir}'],
        executable_args=['./capd_example'],
        jobs=jobs,
        dry_run=dry_run)

    project_starter_dir = f'{workspace_root}/CAPD/capdMake/examples/projectStarter'
    setup_project_starter(project_starter_dir, dry_run)
