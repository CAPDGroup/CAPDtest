import subprocess
import os
import logging
import shutil

trace = logging.getLogger(__file__)

def setup_library(workdir, repodir, builddir, installdir):

    trace.debug(f'Does {workdir} already exist?')
    if os.path.isdir(workdir):
        trace.debug(f'Removing {workdir}')
        shutil.rmtree(workdir)
        trace.debug('Done.')

    trace.debug(f'Creating {workdir}')
    os.mkdir(workdir)

    trace.debug('Cloning CAPD repository...')
    ret = subprocess.call(['git', 'clone', 'https://github.com/CAPDGroup/CAPD'], cwd=workdir)
    if ret:
        raise Exception(f'Failed to clone CAPD repository (error code: {ret})')

    trace.debug('Configuring the library...')
    trace.debug(f'CAPD installation path: {installdir}')
    ret = subprocess.call(['cmake', '-S', repodir, '-B', builddir,
                        '-DCAPD_BUILD_ALL=ON',
                        f'-DCMAKE_INSTALL_PREFIX={installdir}'])
    if ret:
        raise Exception(f'Failed to configure CAPD library (error code: {ret})')

    trace.debug('Building the library...')
    ret = subprocess.call(['make', '-j', str(4)], cwd=builddir)
    if ret:
        raise Exception(f'Failed to build CAPD library (error code: {ret})')

    trace.debug('Executing test cases...')
    ret = subprocess.call(['make', 'test', '-j', str(4)], cwd=builddir)
    if ret:
        raise Exception(f'CAPD test execution failed (error code: {ret})')

    trace.debug('Performing local library installation...')
    ret = subprocess.call(['make', 'install'], cwd=builddir)
    if ret:
        raise Exception(f'CAPD installation failed (error code: {ret})')


def setup_example_1(workdir, repodir, builddir, installdir):

    trace.debug('Cloning CAPD example 1 repository...')
    ret = subprocess.call(['git', 'clone', 'https://github.com/CAPDGroup/CAPD.example.1'], cwd=workdir)
    if ret:
        raise Exception(f'Failed to clone CAPD example 1 repository (error code: {ret})')

    trace.debug('Configuring the example 1...')
    ret = subprocess.call(['cmake', '-S', repodir, '-B', builddir,
                        f'-DCMAKE_PREFIX_PATH={installdir}'])
    if ret:
        raise Exception(f'Failed to configure CAPD example 1 (error code: {ret})')

    trace.debug('Building the example 1...')
    ret = subprocess.call(['make', '-j', str(4)], cwd=builddir)
    if ret:
        raise Exception(f'Failed to build CAPD example 1 (error code: {ret})')

    trace.debug('Executing example 1 app...')
    ret = subprocess.call(['./capd_example'], cwd=builddir)
    if ret:
        raise Exception(f'CAPD example 1 execution failed (error code: {ret})')


def setup_example_2(workdir, repodir, builddir):

    trace.debug('Cloning CAPD example 2 repository...')
    ret = subprocess.call(['git', 'clone', 'https://github.com/CAPDGroup/CAPD.example.2'], cwd=workdir)
    if ret:
        raise Exception(f'Failed to clone CAPD example 2 repository (error code: {ret})')

    trace.debug('CAPD example 2 submodules updating...')
    ret = subprocess.call(['git', 'submodule', 'update', '--init', '--recursive'], cwd=repodir)
    if ret:
        raise Exception(f'Failed to update git submodules for CAPD example 2 (error code: {ret})')

    trace.debug('Configuring the example 2...')
    ret = subprocess.call(['cmake', '-S', repodir, '-B', builddir,
                           '-DCAPD_ENABLE_MULTIPRECISION=OFF'])
    if ret:
        raise Exception(f'Failed to configure CAPD example 2 (error code: {ret})')

    trace.debug('Building the example 2...')
    ret = subprocess.call(['make', '-j', str(4)], cwd=builddir)
    if ret:
        raise Exception(f'Failed to build CAPD example 2 (error code: {ret})')

    trace.debug('Executing example 2 app...')
    ret = subprocess.call(['./capd_example'], cwd=builddir)
    if ret:
        raise Exception(f'CAPD example 2 execution failed (error code: {ret})')
