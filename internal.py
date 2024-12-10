import subprocess
import os
import logging
import shutil
from typing import List

trace = logging.getLogger(__file__)

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


def setup_library(workdir, repodir, builddir, installdir, config : dict):

    target_config = config["targets"]["CAPD"]

    if target_config['enabled']:
        trace.info(f'Building target: {target_config["desc"]} ...')
                   
        trace.debug('Cloning repository...')
        remote_url = target_config["remote_url"]
        ret = run_command(['git', 'clone', remote_url], workdir, config)
        if ret:
            raise Exception(f'Failed to clone CAPD repository (error code: {ret})')

        trace.debug('Configuring the library...')
        trace.debug(f'CAPD installation path: {installdir}')
        ret = run_command(['cmake', '-S', repodir, '-B', builddir,
                            '-DCAPD_BUILD_ALL=ON',
                            f'-DCMAKE_INSTALL_PREFIX={installdir}'], workdir, config)
        if ret:
            raise Exception(f'Failed to configure CAPD library (error code: {ret})')

        trace.debug('Building the library...')
        ret = run_command(['make', '-j', str(4)], builddir, config)
        if ret:
            raise Exception(f'Failed to build CAPD library (error code: {ret})')

        trace.debug('Executing test cases...')
        ret = run_command(['make', 'test', '-j', str(4)], builddir, config)
        if ret:
            raise Exception(f'CAPD test execution failed (error code: {ret})')

        trace.debug('Performing local library installation...')
        ret = run_command(['make', 'install'], builddir, config)
        if ret:
            raise Exception(f'CAPD installation failed (error code: {ret})')

    else:
        trace.info(f'Skipping target: {target_config["desc"]} ...')


def setup_example_1(workdir, repodir, builddir, installdir, config : dict):

    target_config = config["targets"]["CAPD_standalone"]

    if target_config['enabled']:
        trace.info(f'Building target: {target_config["desc"]} ...')

        trace.debug('Cloning repository...')
        remote_url = target_config["remote_url"]
        ret = run_command(['git', 'clone', remote_url], workdir, config)
        if ret:
            raise Exception(f'Failed to clone CAPD example 1 repository (error code: {ret})')

        trace.debug('Configuring the example 1...')
        ret = run_command(['cmake', '-S', repodir, '-B', builddir,
                            f'-DCMAKE_PREFIX_PATH={installdir}'], workdir, config)
        if ret:
            raise Exception(f'Failed to configure CAPD example 1 (error code: {ret})')

        trace.debug('Building the example 1...')
        ret = run_command(['make', '-j', str(4)], builddir, config)
        if ret:
            raise Exception(f'Failed to build CAPD example 1 (error code: {ret})')

        trace.debug('Executing example 1 app...')
        ret = run_command(['./capd_example'], builddir, config)
        if ret:
            raise Exception(f'CAPD example 1 execution failed (error code: {ret})')

    else:
        trace.info(f'Skipping target: {target_config["desc"]} ...')


def setup_example_2(workdir, repodir, builddir, config : dict):

    target_config = config["targets"]["CAPD_standard"]

    if target_config['enabled']:
        trace.info(f'Building target: {target_config["desc"]} ...')

        trace.debug('Cloning repository...')
        remote_url = target_config["remote_url"]
        ret = run_command(['git', 'clone', remote_url], workdir, config)
        if ret:
            raise Exception(f'Failed to clone CAPD example 2 repository (error code: {ret})')

        trace.debug('CAPD example 2 building with build.sh ...')
        ret = run_command(['./build.sh'], repodir, config)
        if ret:
            raise Exception(f'Failed to update git submodules for CAPD example 2 (error code: {ret})')

        trace.debug('Executing example 2 app...')
        ret = run_command(['./capd_example'], builddir, config)
        if ret:
            raise Exception(f'CAPD example 2 execution failed (error code: {ret})')
    
    else:
        trace.info(f'Skipping target: {target_config["desc"]} ...')


def setup_project_starter(repodir, config : dict):

    target_config = config["targets"]["CAPD_projectstarter"]

    if target_config['enabled']:
        trace.info(f'Building target: {target_config["desc"]} ...')

        trace.debug('Building project starter...')
        ret = run_command(['make'], repodir, config)
        if ret:
            raise Exception(f'Failed to build project starter (error code: {ret})')
        
        trace.debug('Executing project starter app...')
        ret = run_command(['./MyProgram'], repodir, config)
        if ret:
            raise Exception(f'Project starter execution failed (error code: {ret})')
    
    else:
        trace.info(f'Skipping target: {target_config["desc"]} ...')
