#!/usr/bin/env python

from distutils.core import setup

setup(
    name='electronfactors',
    version='0.1.0',
    description='Electron factor equivalent ellipse spline modelling',
    author='Simon Biggs',
    author_email='mail@simonbiggs.net',
    url='https://github.com/SimonBiggs/equivalent-ellipse-spline-modelling',
    packages=[
        'electronfactors',
        'electronfactors.ellipseutilities',
        'electronfactors.inpututilities'],
     )
