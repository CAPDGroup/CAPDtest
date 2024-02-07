import subprocess
import os
import logging
import shutil

logging.basicConfig(level=logging.DEBUG)

trace = logging.getLogger(__file__)

workdir = 'workdir'
capddir = f'{workdir}/CAPD'
builddir = f'{capddir}/build'
installdir = os.path.abspath(f'{workdir}/CAPD_install')
exampledir = f'{workdir}/CAPD.example.1'
example_builddir = f'{exampledir}/build'

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
ret = subprocess.call(['cmake', '-S', capddir, '-B', builddir,
                       '-DCAPD_ENABLE_MULTIPRECISION=OFF',
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

trace.debug('Cloning CAPD example 1 repository...')
ret = subprocess.call(['git', 'clone', 'https://github.com/CAPDGroup/CAPD.example.1'], cwd=workdir)
if ret:
    raise Exception(f'Failed to clone CAPD example 1 repository (error code: {ret})')

trace.debug('Configuring the example...')
ret = subprocess.call(['cmake', '-S', exampledir, '-B', example_builddir,
                       f'-DCMAKE_PREFIX_PATH={installdir}'])
if ret:
    raise Exception(f'Failed to configure CAPD example (error code: {ret})')

trace.debug('Building the example...')
ret = subprocess.call(['make', '-j', str(4)], cwd=example_builddir)
if ret:
    raise Exception(f'Failed to build CAPD example (error code: {ret})')

trace.debug('Executing example app...')
ret = subprocess.call(['./capd_example'], cwd=example_builddir)
if ret:
    raise Exception(f'CAPD example execution failed (error code: {ret})')

