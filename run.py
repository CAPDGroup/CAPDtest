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
    build_dir = 'build'
    jobs = 16

    for interval_type in ["NATIVE", "FILIB", "CXSC"]:

        workspace_root = os.path.abspath(f'./workdir_{interval_type}')
        install_dir = f'{workspace_root}/CAPD_install_{interval_type}'

        if dry_run:
            logging.info("Performing dry run...")

        setup_workdir(workspace_root, dry_run, incremental_run)

        execute_stage_library(
            workspace_root=workspace_root,
            remote_url='https://github.com/CAPDGroup/CAPD',
            branch='master',
            local_dir='CAPD',
            build_dir=build_dir,
            cmake_options=['-DCAPD_BUILD_ALL=ON', f'-DCAPD_INTERVAL_TYPE={interval_type}', f'-DCMAKE_INSTALL_PREFIX={install_dir}'],
            jobs=jobs,
            dry_run=dry_run)
        
        if True:
            execute_stage_executable(
                workspace_root=workspace_root,
                remote_url='https://github.com/CAPDGroup/CAPD_example_standalone',
                branch='master',
                local_dir='CAPD_example_standalone',
                build_dir=build_dir,
                cmake_options=[f'-DCAPD_INTERVAL_TYPE={interval_type}'],
                executable_args=['./capd_example'],
                jobs=jobs,
                dry_run=dry_run)

        if True:
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

