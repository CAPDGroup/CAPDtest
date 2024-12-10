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


def run_command(args : List[str], cwd : str, config : dict):
    if not config["dry_run"]:
        subprocess.call(args, cwd=cwd)
    else:
        trace.info('Run command:\n' +
                   '\t' + ' '.join(args) + '\n' +
                   '\t' + f'cwd={cwd}\n')


def setup_workdir(config):

    workdir = os.path.abspath( config['root'] )
    if not config["dry_run"]:
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
    local_url : str,
    build_dir : str,
    cmake_options : List[str],
    jobs : int,
    dry_run : bool):

    __run_command_with_trace(
        args=['git', 'clone', remote_url],
        cwd=workspace_root,
        dry_run=dry_run,
        debug_message='Cloning repository...',
        error_message='Cloning failed')
    
    __run_command_with_trace(
        args=['cmake', '-S', local_url, '-B', build_dir, *cmake_options],
        cwd=workspace_root,
        dry_run=dry_run,
        debug_message='Configuration...',
        error_message='Configuration failed')

    __run_command_with_trace(
        args=['make', '-j', jobs],
        cwd=build_dir,
        dry_run=dry_run,
        debug_message='Building...',
        error_message='Building failed')

    __run_command_with_trace(
        args=['make', 'test', '-j', jobs],
        cwd=build_dir,
        dry_run=dry_run,
        debug_message='Executing tests...',
        error_message='Test execution failed')

    __run_command_with_trace(
        args=['make', 'install'],
        cwd=build_dir,
        dry_run=dry_run,
        debug_message='Installation...',
        error_message='Installation failed')


def setup_library(config : dict):

    target_config = config["targets"]["CAPD"]

    if target_config['enabled']:
        trace.info(f'Building target: {target_config["desc"]} ...')

        workdir = os.path.abspath(config['root'])
        repodir = f'{workdir}/{target_config["local_url"]}'
        builddir = f'{repodir}/{config["builddir"]}'
        installdir = f'{workdir}/{config["installdir"]}'
        jobs = str(config['jobs'])
        dry_run = config['dry_run']

        remote_url = target_config["remote_url"]

        trace.debug(f'CAPD installation path: {installdir}')

        execute_stage_library(
            workspace_root=workdir,
            remote_url=remote_url,
            local_url=repodir,
            build_dir=builddir,
            cmake_options=['-DCAPD_BUILD_ALL=ON', f'-DCMAKE_INSTALL_PREFIX={installdir}'],
            jobs=jobs,
            dry_run=dry_run)

    else:
        trace.info(f'Skipping target: {target_config["desc"]} ...')


def setup_example_1(config : dict):

    target_config = config["targets"]["CAPD_standalone"]

    if target_config['enabled']:
        trace.info(f'Building target: {target_config["desc"]} ...')

        workdir = os.path.abspath(config['root'])
        repodir = f'{workdir}/{target_config["local_url"]}'
        builddir = f'{repodir}/{config["builddir"]}'
        jobs = str(config["jobs"])

        trace.debug('Cloning repository...')
        remote_url = target_config["remote_url"]
        ret = run_command(['git', 'clone', remote_url], workdir, config)
        if ret:
            raise Exception(f'Cloning failed (error code: {ret})')
        
        trace.debug('Updating submodules...')
        ret = run_command(['git', 'submodule', 'update', '--init', '--recursive'], repodir, config)
        if ret:
            raise Exception(f'Failed to update submodules (error code: {ret})')

        trace.debug('Configuring ...')
        ret = run_command(['cmake', '-S', repodir, '-B', builddir], workdir, config)
        if ret:
            raise Exception(f'Configuration failed (error code: {ret})')

        trace.debug('Building ...')
        ret = run_command(['make', '-j', jobs], builddir, config)
        if ret:
            raise Exception(f'Build failed (error code: {ret})')

        trace.debug('Executing program ...')
        ret = run_command(['./capd_example'], builddir, config)
        if ret:
            raise Exception(f'Execution failed (error code: {ret})')

    else:
        trace.info(f'Skipping target: {target_config["desc"]} ...')


def setup_example_2(config : dict):

    target_config = config["targets"]["CAPD_standard"]

    if target_config['enabled']:
        trace.info(f'Building target: {target_config["desc"]} ...')

        workdir = os.path.abspath(config['root'])
        repodir = f'{workdir}/{target_config["local_url"]}'
        builddir = f'{repodir}/{config["builddir"]}'
        installdir = f'{workdir}/{config["installdir"]}'
        jobs = str(config["jobs"])

        trace.debug('Cloning repository...')
        remote_url = target_config["remote_url"]
        ret = run_command(['git', 'clone', remote_url], workdir, config)
        if ret:
            raise Exception(f'Cloning failed (error code: {ret})')
        
        trace.debug('Configuring ...')
        ret = run_command(['cmake', '-S', repodir, '-B', builddir,
                            f'-DCMAKE_PREFIX_PATH={installdir}'], workdir, config)
        if ret:
            raise Exception(f'Configuration failed (error code: {ret})')

        trace.debug('Building ...')
        ret = run_command(['make', '-j', jobs], builddir, config)
        if ret:
            raise Exception(f'Build failed (error code: {ret})')

        trace.debug('Executing program ...')
        ret = run_command(['./capd_example'], builddir, config)
        if ret:
            raise Exception(f'Execution failed (error code: {ret})')
    
    else:
        trace.info(f'Skipping target: {target_config["desc"]} ...')


def setup_project_starter(project_starter_dir : str, config : dict):

    target_config = config["targets"]["CAPD_projectstarter"]

    if target_config['enabled']:
        trace.info(f'Building target: {target_config["desc"]} ...')

        trace.debug('Building project starter...')
        ret = run_command(['make'], project_starter_dir, config)
        if ret:
            raise Exception(f'Failed to build project starter (error code: {ret})')
        
        trace.debug('Executing project starter app...')
        ret = run_command(['./MyProgram'], project_starter_dir, config)
        if ret:
            raise Exception(f'Project starter execution failed (error code: {ret})')
    
    else:
        trace.info(f'Skipping target: {target_config["desc"]} ...')
