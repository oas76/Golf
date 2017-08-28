#!/usr/local/bin/python2

from setuptools import setup, find_packages
version = '1.0'

setup(
    name='WebApp',
    version=version,
    description="Front End for Golf App",
    long_description=(""),
    author='oddaskaf',
    author_email='oaskaflestad@gmail.com',
    classifiers=['Programming Language :: Python :: 2.7'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,

    install_requires=[
        'Django',
    ]
)