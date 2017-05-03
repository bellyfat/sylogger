#!/usr/bin/env python

from setuptools import setup, find_packages
from os.path import join, dirname
import sys
if not sys.version_info[0] == 2:
    sys.exit("Python 3 is not supported")

setup(
    name='sylogger',
    version='0.1',
    author='Slipeer',
    author_email='Slipeer+sylogger@gmail.com',
    license='APACHE 2.0',
    packages=find_packages(),
    description='Conversation logger application service for matrix-org/sydent',
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    install_requires=[
        'Flask==0.8'
    ],
    data_files = [
        ("", ["LICENSE"]),
        ("/lib/systemd/system", ["contrib/systemd/matrix-sylogger.service"]),
        ("/etc/matrix-synapse", ["sylogger.conf", "sylogger.yaml"])
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