#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='anillo_auth',
    version=":versiontools:anillo_auth:",
    description="Authentication middleware for anillo",
    long_description="",
    keywords='web, anillo, authentication',
    author='Jesús Espino García',
    author_email='jespinog@gmail.com',
    url='https://github.com/jespino/anillo_auth',
    license='BSD',
    packages=['anillo_auth', 'anillo_auth.backends'],
    install_requires=[
        'itsdangerous',
    ],
    setup_requires=[
        'versiontools >= 1.9.1',
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
