#!/usr/bin/env python

from distutils.core import setup

setup(
    name='electronfactors',
    version='0.1.0.dev1',
    description='Electron factor equivalent ellipse spline modelling',
    author='Simon Biggs',
    author_email='mail@simonbiggs.net',
    url='https://github.com/SimonBiggs/equivalent-ellipse-spline-modelling',
    license='AGPLv3+',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Scientific/Engineering :: Physics',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        ],
    keywords='electron cutout output factors equivalent ellipse',
    packages=[
        'electronfactors',
        'electronfactors.ellipse',
        'electronfactors.inputs',
        'electronfactors.model'],
     )
