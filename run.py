import logging
import os

from internal import setup_workdir
from internal import execute_stage_executable
from internal import execute_stage_library

import project_starter

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    dry_run = False
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
        branch='master',
        local_dir='CAPD',
        build_dir=build_dir,
        cmake_options=['-DCAPD_BUILD_ALL=ON', f'-DCMAKE_INSTALL_PREFIX={install_dir}'],
        jobs=jobs,
        dry_run=dry_run)
    
    if False:
        execute_stage_executable(
            workspace_root=workspace_root,
            remote_url='https://github.com/CAPDGroup/CAPD_example_standalone',
            branch='master',
            local_dir='CAPD_example_standalone',
            build_dir=build_dir,
            cmake_options=[],
            executable_args=['./capd_example'],
            jobs=jobs,
            dry_run=dry_run)

    if False:
        execute_stage_executable(
            workspace_root=workspace_root,
            remote_url='https://github.com/CAPDGroup/CAPD_example_standard',
            branch='master',
            local_dir='CAPD_example_standard',
            build_dir=build_dir,
            cmake_options=[f'-DCMAKE_PREFIX_PATH={install_dir}'],
            executable_args=['./capd_example'],
            jobs=jobs,
            dry_run=dry_run)

    project_starter_dir = f'{workspace_root}/CAPD/capdMake/examples/projectStarter'

    if True:
        project_starter.execute_internal_test(
            project_starter_dir=project_starter_dir,
            dry_run=dry_run)
        
    if True:
        project_starter.execute_external_test(
            workspace_root=workspace_root,
            project_starter_dir=project_starter_dir,
            install_dir=install_dir,
            dry_run=dry_run)

