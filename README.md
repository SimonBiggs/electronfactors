# Equivalent Ellipse Spline Modelling

[![Build Status](https://travis-ci.org/SimonBiggs/equivalent-ellipse-spline-modelling.svg?branch=master)](https://travis-ci.org/SimonBiggs/equivalent-ellipse-spline-modelling)
[![Coverage Status](https://coveralls.io/repos/SimonBiggs/equivalent-ellipse-spline-modelling/badge.svg)](https://coveralls.io/r/SimonBiggs/equivalent-ellipse-spline-modelling)

## Description
Model electron output factors using the equivalent ellipse spline modelling method

## Install via pip

    pip install electronfactors

## Examples

Examples can be found [here](http://nbviewer.ipython.org/github/simonbiggs/equivalent-ellipse-spline-modelling/tree/master/examples/).

## Docker install method

To run:

    mkdir -p ~/Documents/electrons; \
    docker run \
        -p 8000:8000 \
        -v ~/Documents/electrons:/home/admin/output \
        --dns=208.67.222.222 \
        simonbiggs/electrons

Default login is user `admin`, password `admin`.

## Copyright information
Copyright &#169; 2015  Simon Biggs

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
