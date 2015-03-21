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
    'redis-simple-cache==0.0.7'
]

test_requirements = [
    'ipdb==0.8',
    'nose',
    'flake8'
]

setup(
    name='geocoder-cache',
    version='0.1.0',
    description="Multiple geocoders, spiced up with persistent cache",
    long_description=readme,
    author="Marco Milanesi",
    author_email='kpanic@gmail.com',
    url='https://github.com/kpanic/geocoder-cache',
    packages=[
        'geocoder_cache',
    ],
    package_dir={'geocoder_cache':
                 'geocoder_cache'},
    include_package_data=True,
    install_requires=requirements,
    license="LGPL3",
    zip_safe=False,
    keywords='geocoder cache',
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
