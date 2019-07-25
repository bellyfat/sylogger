#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='sylogger',
    version='0.2',
    author='Pavel Kardash',
    author_email='pavel@kardash.su',
    license='APACHE 2.0',
    packages=find_packages(),
    description='Conversation logger application service for matrix-org/synapse',
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    install_requires=[
        'Flask>=1.0.0',
        'waitress',
        'configparser'
    ],
    data_files = [
        ("", ["LICENSE"]),
        ("/lib/systemd/system", ["contrib/systemd/matrix-sylogger.service"]),
        ("/opt/synapse", ["sylogger.conf", "as_sylogger.yaml"])
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Framework :: Flask',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Topic :: Communications :: Chat'
    ]
)