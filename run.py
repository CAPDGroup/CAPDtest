import logging

from internal import setup_library
from internal import setup_example_1
from internal import setup_example_2

logging.basicConfig(level=logging.DEBUG)

workdir = 'workdir'
capddir = f'{workdir}/CAPD'
builddir = f'{capddir}/build'
installdir = os.path.abspath(f'{workdir}/CAPD_install')

setup_library(workdir, capddir, builddir, installdir)

exampledir = f'{workdir}/CAPD.example.1'
example_builddir = f'{exampledir}/build'

setup_example_1(workdir, exampledir, example_builddir, installdir)

example2_dir = f'{workdir}/CAPD.example.2'
example2_builddir = f'{example2_dir}/build'

setup_example_2(workdir, example2_dir, example2_builddir)
