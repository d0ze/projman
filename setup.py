import os

from itertools import chain
from setuptools import find_packages, setup

DIRS = ['progman/']


def _get_dirs(dir_):
    data_files = []
    start_point = dir_
    for root, dirs, files in os.walk(start_point):
        root_files = [os.path.join(root, i) for i in files]
        data_files.append((root, root_files))
    return data_files


files_ = list(chain.from_iterable([_get_dirs(dir_) for dir_ in DIRS]))

setup(
    name='projman',
    version='0.1',
    packages=find_packages(),
    dependency_links=[],
    include_package_data=True,
    entry_points={'console_scripts': ['projman = projman.projman:main']},

)
