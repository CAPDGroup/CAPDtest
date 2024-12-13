import subprocess
import os
import logging
import shutil
from typing import List

trace = logging.getLogger(__file__)

def __run_command(args : List[str], cwd : str, dry_run : bool, env=None):

    if type(dry_run) is not bool:
        raise Exception("Unexpected dry_run test!")

    if not dry_run:
        subprocess.call(args, cwd=cwd, env=env)
    else:
        trace.info('Run command:\n' +
                   '\t' + ' '.join(args) + '\n' +
                   '\t' + f'cwd={cwd}\n')


def run_command_with_trace(
        args : List[str],
        cwd : str,
        dry_run : bool,
        debug_message : str,
        error_message : str,
        env=None):
    
    trace.debug(debug_message)
    ret = __run_command(args, cwd, dry_run, env)
    if ret:
        raise Exception(f'{error_message} (error code: {ret})')


def setup_workdir(
        workspace_root : str,
        dry_run : bool,
        incremental_run : bool):

    if type(dry_run) != bool:
        raise Exception("Unexpected dry_run parameter type!")
    
    if type(incremental_run) != bool:
        raise Exception("Unexpected incremental_run parameter type!")
    
    workdir = os.path.abspath( workspace_root )
    if not dry_run:
        if not incremental_run:
            trace.debug(f'Does {workdir} already exist?')
            if os.path.isdir(workdir):
                trace.debug(f'Removing {workdir}')
                shutil.rmtree(workdir)
                trace.debug('Done.')
            
            trace.debug(f'Creating {workdir}')
            os.mkdir(workdir)
        else:
            trace.debug(f'Does {workdir} already exist?')
            if not os.path.isdir(workdir):
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

    run_command_with_trace(
        args=['git', 'clone', remote_url],
        cwd=workspace_root,
        dry_run=dry_run,
        debug_message='Cloning repository...',
        error_message='Cloning failed')
    
    run_command_with_trace(
        args=['cmake', '-S', local_path, '-B', build_path, *cmake_options],
        cwd=workspace_root,
        dry_run=dry_run,
        debug_message='Configuration...',
        error_message='Configuration failed')

    run_command_with_trace(
        args=['make', '-j', str(jobs)],
        cwd=build_path,
        dry_run=dry_run,
        debug_message='Building...',
        error_message='Building failed')

    run_command_with_trace(
        args=['make', 'test', '-j', str(jobs)],
        cwd=build_path,
        dry_run=dry_run,
        debug_message='Executing tests...',
        error_message='Test execution failed')

    run_command_with_trace(
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

    run_command_with_trace(
        args=['git', 'clone', remote_url],
        cwd=workspace_root,
        dry_run=dry_run,
        debug_message='Cloning repository...',
        error_message='Cloning failed')
    
    run_command_with_trace(
        args=['git', 'submodule', 'update', '--init', '--recursive'],
        cwd=local_path,
        dry_run=dry_run,
        debug_message='Updating submodules...',
        error_message='Failed to update submodules')

    run_command_with_trace(
        args=['cmake', '-S', local_path, '-B', build_path, *cmake_options],
        cwd=workspace_root,
        dry_run=dry_run,
        debug_message='Configuration...',
        error_message='Configuration failed')

    run_command_with_trace(
        args=['make', '-j', str(jobs)],
        cwd=build_path,
        dry_run=dry_run,
        debug_message='Building...',
        error_message='Building failed')
    
    run_command_with_trace(
        args=executable_args,
        cwd=build_path,
        dry_run=dry_run,
        debug_message='Executing program...',
        error_message='Execution failed')


def process_file_line_by_line(path : str, parser):
    file_tmp = path + '.tmp'
    with open(path, 'r', newline='') as ifs:
        with open(file_tmp, 'w', newline='') as ofs:

            try:
                while True:
                    line = ifs.readline()

                    line = parser(line)

                    if line == '':
                        break

                    ofs.write(line)
            except Exception as e:
                print(e)
    
    status = os.stat(path)
    permissions = status.st_mode & 0o777
    os.remove(path)
    os.rename(file_tmp, path)
    os.chmod(path, permissions)
