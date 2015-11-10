# Copyright (C) 2015 Simon Biggs
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public
# License along with this program. If not, see
# http://www.gnu.org/licenses/.

import yaml
import numpy as np

import matplotlib.pyplot as plt
import traceback
from glob import glob

from scipy.interpolate import SmoothBivariateSpline
from scipy.stats import shapiro, probplot, ttest_1samp
from scipy.special import gamma

from electronfactors.inputs.convert_merge import convert_merge
from electronfactors.model.parameterise import parameterise
from electronfactors.model.sort import create_cache
from electronfactors.ellipse.equivalent import equivalent_ellipse
from electronfactors.model.threshold import fit_give


def create_model(width, eqPonA, factor):

    def model(x, y):

        spline = SmoothBivariateSpline(
            width, eqPonA, factor, kx=2, ky=1)

        result = spline.ev(x, y)

        return result

    return model


def c4(n):

    output = np.sqrt(2/(n-1)) * gamma(n/2) / gamma((n-1)/2)
    if np.isnan(output):
        output = 1

    return output


def test_partial_end_to_end():

    convert_merge(
        input_directory="paper/user_inputs/",
        output_directory="paper/imported_data/")
    parameterise(working_directory="paper/imported_data/")

    energy_list = [6, 9, 12, 15, 18]
    for energy in energy_list:
        create_cache(
            input_directory="paper/imported_data/",
            output_directory="paper/model_cache/",
            energy=energy,
            applicator=10)

    with open("paper/model_cache/12MeV_10app_100ssd.yml", 'r') as file:
        cutout_data = yaml.load(file)

    custom_label = np.array([key for key in cutout_data])
    width = np.array([cutout_data[key]['width'] for key in custom_label])
    length = np.array([cutout_data[key]['length'] for key in custom_label])
    factor = np.array([cutout_data[key]['factor'] for key in custom_label])
    ratio = width/length
    eqPonA = 2*(3*(ratio+1) - np.sqrt((3*ratio+1)*(ratio+3))) / width

    predictionValue = np.zeros(len(custom_label))

    for i in range(len(custom_label)):

        widthTest = np.delete(width, i)
        eqPonATest = np.delete(eqPonA, i)
        factorTest = np.delete(factor, i)

        modelTest = create_model(widthTest, eqPonATest, factorTest)

        predictionValue[i] = modelTest(width[i], eqPonA[i])

    percentDifference = 100*(factor - predictionValue) / factor
    residualStd = (
        np.std(percentDifference, ddof=1) / c4(len(percentDifference)))

    assert residualStd < 0.5
    assert residualStd > 0.45
