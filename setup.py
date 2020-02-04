#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import os 

from setuptools import find_packages, setup, Command

# Meta.
NAME = 'animask'
DESCRIPTION = 'Visualization of the predictions of the network during training.'
URL = 'https://github.com/sankovalev/animask'
EMAIL = 'sankovalev@gmail.com'
AUTHOR = 'Alexander Kovalev'
REQUIRES_PYTHON = '>=3.0.0'
VERSION = None

base = os.path.abspath(os.path.dirname(__file__))

# What packages are required for this module to be executed?
try:
    with open(os.path.join(base, 'requirements.txt'), encoding='utf-8') as f:
        REQUIRED = f.read().split('\n')
except:
    REQUIRED = []

# What packages are optional?
EXTRAS = {
    'test': ['pytest']
}

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(base, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
meta = {}
if not VERSION:
    with open(os.path.join(base, NAME, '__version__.py')) as f:
        exec(f.read(), meta)
else:
    meta['__version__'] = VERSION

# Where the magic happens:
setup(
    name=NAME,
    version=meta['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=['animask'],
    include_package_data=True,
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ]
)