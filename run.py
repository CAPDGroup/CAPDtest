import logging
import os

from internal import run_command_with_trace
from internal import setup_workdir
from internal import execute_stage_executable
from internal import execute_stage_library
from internal import process_file_line_by_line

def setup_project_starter_internal(
        project_starter_dir : str,
        dry_run : bool):
    
    run_command_with_trace(
        args=['git', 'clean', '-fd'],
        cwd=project_starter_dir,
        dry_run=dry_run,
        debug_message='Cleaning build output...',
        error_message='Cleaning build output failed')

    run_command_with_trace(
        args=['make'],
        cwd=project_starter_dir,
        dry_run=dry_run,
        debug_message='Building project starter...',
        error_message='Failed to build project starter')

    run_command_with_trace(
        args=['./MyProgram'],
        cwd=project_starter_dir,
        dry_run=dry_run,
        debug_message='Executing project starter app...',
        error_message='Project starter execution failed')


def comment_out_capddir_line(path : str):

    def parser(line : str):
        if line.startswith('CAPDBINDIR'):
            return '# ' + line
        else:
            return line
    
    process_file_line_by_line(path, parser)


def setup_project_starter_external(
        workspace_root : str,
        project_starter_dir : str,
        install_dir : str,
        dry_run : bool):

    local_path = f'{workspace_root}/projectStarter'

    run_command_with_trace(
        args=['git', 'clean', '-fd'],
        cwd=project_starter_dir,
        dry_run=dry_run,
        debug_message='Cleaning build output...',
        error_message='Cleaning build output failed')

    run_command_with_trace(
        args=['cp', '-r', project_starter_dir, workspace_root],
        cwd=workspace_root,
        dry_run=dry_run,
        debug_message='Copying project starter...',
        error_message='Copying failed')
    
    comment_out_capddir_line(f'{local_path}/Makefile')
    
    env = os.environ.copy()
    env['CAPDBINDIR'] = f'{install_dir}/bin/'

    run_command_with_trace(
        args=['make'],
        cwd=local_path,
        dry_run=dry_run,
        debug_message='Building project starter...',
        error_message='Failed to build project starter',
        env=env)

    run_command_with_trace(
        args=['./MyProgram'],
        cwd=local_path,
        dry_run=dry_run,
        debug_message='Executing project starter app...',
        error_message='Project starter execution failed')
    

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
        setup_project_starter_internal(
            project_starter_dir=project_starter_dir,
            dry_run=dry_run)
        
    if True:
        setup_project_starter_external(
            workspace_root=workspace_root,
            project_starter_dir=project_starter_dir,
            install_dir=install_dir,
            dry_run=dry_run)

