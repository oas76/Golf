#!/usr/local/bin/python2

from setuptools import setup, find_packages
version = '1.1'

setup(
    name='GolfSetup',
    version=version,
    description="Script generating golf tournament setup",
    long_description=(""),
    author='oddaskaf',
    author_email='oaskaflestad@gmail.com',
    classifiers=['Programming Language :: Python :: 2.7'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,

    install_requires=[
        'numpy',
        'flask',
    ]
)