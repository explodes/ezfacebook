# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2011, Evan Leis
#
# Distributed under the terms of the Lesser GNU General Public License (LGPL)
#-----------------------------------------------------------------------------

from setuptools import setup, find_packages

with open('README.md') as readme:
    long_description = readme.read()

setup(
    name='ezfacebook',
    version='0.0.1',
    description="Django Tools to use facebook seamlessly",
    long_description=long_description,
    author='Evan Leis',
    author_email='engineergod@yahoo.com',
    url='',
    install_requires=[
        'django>=1.3'
    ],
    setup_requires=[
    ],
    packages=find_packages(exclude=[
    ]),
    include_package_data=True,
    test_suite=None,
    package_data={},
    zip_safe=True,
    entry_points="""
    """,
    license="Lesser GNU General Public License (LGPL)",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
    ],
)
