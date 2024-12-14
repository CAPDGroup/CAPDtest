import os

from internal import run_command_with_trace
from internal import process_file_line_by_line

def execute_internal_test(
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


def __comment_out_capddir_line(path : str):

    def parser(line : str):
        if line.startswith('CAPDBINDIR'):
            return '# ' + line
        else:
            return line
    
    process_file_line_by_line(path, parser)


def execute_external_test(
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
    
    __comment_out_capddir_line(f'{local_path}/Makefile')
    
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
    