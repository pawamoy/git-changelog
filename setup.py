# -*- coding: utf8 -*-

"""
Setup script.

Uses setuptools.
Long description is a concatenation of README.md and CHANGELOG.md.
"""

from __future__ import absolute_import, print_function

import io
import os
from glob import glob

from setuptools import find_packages, setup


def read(*names, **kwargs):
    """Read a file in current directory."""
    return io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


setup(
    name='gitolog',
    version='0.1.1',
    license='ISC',
    description='Automatic Changelog generator using Jinja2 templates.',
    long_description='%s\n%s' % (read('README.md'), read('CHANGELOG.md')),
    author='Timothée Mazzucotelli',
    author_email='timothee.mazzucotelli@protonmail.com',
    url='https://gitlab.com/pawamoy/gitolog',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[os.path.splitext(os.path.basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
    ],
    keywords=[
        'automatic', 'changelog', 'generator', 'automatic-changelog-generator',
        'keep-a-changelog', 'git', 'git-logs'
    ],
    install_requires=[
        'jinja2'
    ],
    entry_points={
        'console_scripts': [
            'gitolog = gitolog.cli:main',
        ],
        # 'gitolog': [
        #     'style.atom = gitolog.styles:AtomStyle',
        #     'style.angular = gitolog.styles:AngularStyle',
        #     'template.angular = gitolog.templates:AngularTemplate',
        #     'template.keepachangelog = gitolog.templates:KeepAChangelogTemplate',
        # ]
    },
)
