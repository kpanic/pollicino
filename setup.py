#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'geopy==1.9.1',
    'elasticsearch==1.4.0',
    'six==1.9.0'
]

test_requirements = [
    'ipdb==0.8',
    'nose',
    'flake8'
]

setup(
    name='pollicino',
    version='0.1.0',
    description="Street search, spiced up with multiple storage and geocoders",
    long_description=readme,
    author="Marco Milanesi",
    author_email='kpanic@gmail.com',
    url='https://github.com/kpanic/pollicino',
    packages=[
        'pollicino',
    ],
    package_dir={'pollicino':
                 'pollicino'},
    include_package_data=True,
    install_requires=requirements,
    license="LGPL3",
    zip_safe=False,
    keywords='geocoder elasticsearch openstreetmap pluggable pollicino',
    classifiers=['License :: OSI Approved :: '
                 'GNU Lesser General Public License v3 (LGPLv3)',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4'],
    test_suite='tests',
    tests_require=test_requirements
)
