import subprocess
import os
import logging
import shutil

from internal import setup_library
from internal import setup_example_1

logging.basicConfig(level=logging.DEBUG)

trace = logging.getLogger(__file__)

workdir = 'workdir'
capddir = f'{workdir}/CAPD'
builddir = f'{capddir}/build'
installdir = os.path.abspath(f'{workdir}/CAPD_install')
exampledir = f'{workdir}/CAPD.example.1'
example_builddir = f'{exampledir}/build'

setup_library(workdir, capddir, builddir, installdir)
setup_example_1(workdir, exampledir, example_builddir, installdir)
