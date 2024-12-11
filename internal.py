import subprocess
import os
import logging
import shutil
from typing import List

trace = logging.getLogger(__file__)

def __run_command(args : List[str], cwd : str, dry_run : bool):

    if type(dry_run) is not bool:
        raise Exception("Unexpected dry_run test!")

    if not dry_run:
        subprocess.call(args, cwd=cwd)
    else:
        trace.info('Run command:\n' +
                   '\t' + ' '.join(args) + '\n' +
                   '\t' + f'cwd={cwd}\n')


def __run_command_with_trace(
        args : List[str],
        cwd : str,
        dry_run : bool,
        debug_message : str,
        error_message : str):
    
    trace.debug(debug_message)
    ret = __run_command(args, cwd, dry_run)
    if ret:
        raise Exception(f'{error_message} (error code: {ret})')


def setup_workdir(
        workspace_root : str,
        dry_run : bool):

    workdir = os.path.abspath( workspace_root )
    if not dry_run:
        trace.debug(f'Does {workdir} already exist?')
        if os.path.isdir(workdir):
            trace.debug(f'Removing {workdir}')
            shutil.rmtree(workdir)
            trace.debug('Done.')
        
        trace.debug(f'Creating {workdir}')
        os.mkdir(workdir)
    else:
        trace.info(f'Workspace root: {workdir}')


def execute_stage_library(
        workspace_root : str,
        remote_url : str,
        local_dir : str,
        build_dir : str,
        cmake_options : List[str],
        jobs : int,
        dry_run : bool):
    
    local_path = f'{workspace_root}/{local_dir}'
    build_path = f'{local_path}/{build_dir}'

    __run_command_with_trace(
        args=['git', 'clone', remote_url],
        cwd=workspace_root,
        dry_run=dry_run,
        debug_message='Cloning repository...',
        error_message='Cloning failed')
    
    __run_command_with_trace(
        args=['cmake', '-S', local_path, '-B', build_path, *cmake_options],
        cwd=workspace_root,
        dry_run=dry_run,
        debug_message='Configuration...',
        error_message='Configuration failed')

    __run_command_with_trace(
        args=['make', '-j', str(jobs)],
        cwd=build_path,
        dry_run=dry_run,
        debug_message='Building...',
        error_message='Building failed')

    __run_command_with_trace(
        args=['make', 'test', '-j', str(jobs)],
        cwd=build_path,
        dry_run=dry_run,
        debug_message='Executing tests...',
        error_message='Test execution failed')

    __run_command_with_trace(
        args=['make', 'install'],
        cwd=build_path,
        dry_run=dry_run,
        debug_message='Installation...',
        error_message='Installation failed')


def execute_stage_executable(
        workspace_root : str,
        remote_url : str,
        local_dir : str,
        build_dir : str,
        cmake_options : List[str],
        executable_args : List[str],
        jobs : int,
        dry_run : bool):
    
    local_path = f'{workspace_root}/{local_dir}'
    build_path = f'{local_path}/{build_dir}'

    __run_command_with_trace(
        args=['git', 'clone', remote_url],
        cwd=workspace_root,
        dry_run=dry_run,
        debug_message='Cloning repository...',
        error_message='Cloning failed')
    
    __run_command_with_trace(
        args=['git', 'submodule', 'update', '--init', '--recursive'],
        cwd=local_path,
        dry_run=dry_run,
        debug_message='Updating submodules...',
        error_message='Failed to update submodules')

    __run_command_with_trace(
        args=['cmake', '-S', local_path, '-B', build_path, *cmake_options],
        cwd=workspace_root,
        dry_run=dry_run,
        debug_message='Configuration...',
        error_message='Configuration failed')

    __run_command_with_trace(
        args=['make', '-j', str(jobs)],
        cwd=build_path,
        dry_run=dry_run,
        debug_message='Building...',
        error_message='Building failed')
    
    __run_command_with_trace(
        args=executable_args,
        cwd=build_path,
        dry_run=dry_run,
        debug_message='Executing program...',
        error_message='Execution failed')


def setup_project_starter(project_starter_dir : str, dry_run : bool):

    __run_command_with_trace(
        args=['make'],
        cwd=project_starter_dir,
        dry_run=dry_run,
        debug_message='Building project starter...',
        error_message='Failed to build project starter')

    __run_command_with_trace(
        args=['./MyProgram'],
        cwd=project_starter_dir,
        dry_run=dry_run,
        debug_message='Executing project starter app...',
        error_message='Project starter execution failed')
        