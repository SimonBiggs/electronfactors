#!/usr/bin/env python

from distutils.core import setup

setup(
    name='electronfactors',
    version='0.1.0.dev1',
    description='Electron factor equivalent ellipse spline modelling',
    author='Simon Biggs',
    author_email='mail@simonbiggs.net',
    url='https://github.com/SimonBiggs/equivalent-ellipse-spline-modelling',
    download_url='https://github.com/SimonBiggs/equivalent-ellipse-spline-modelling/tarball/0.1.0.dev2',
    license='AGPLv3',
    classifiers=[
        'Development Status :: 1 - Development',
        'Intended Audience :: Medical Physicits',
        'Topic :: Medical Physics :: Quality Assuarance Tools',
        'License :: OSI Approved :: Affero General Public License Version 3.0',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        ],
    keywords='electron cutout output factors equivalent ellipse',
    install_requires=['numpy', 'scipy', 'pandas', 'shapely', 'PyYAML'],
    packages=[
        'electronfactors',
        'electronfactors.ellipse',
        'electronfactors.inputs',
        'electronfactors.model'],
     )
