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

import numpy as np
import yaml
from scipy.interpolate import SmoothBivariateSpline
from scipy.optimize import minimize

from scipy.special import gamma
from .threshold import fit_give


def to_eqPonA(width, length):
    perimeter = (
        np.pi / 2 *
        (3*(width + length) - np.sqrt((3*width + length)*(3*length + width)))
    )
    area = np.pi / 4 * width * length

    eqPonA = perimeter / area

    return eqPonA


def to_length(width_array, eqPonA_array):
    def to_minimise(length, width, eqPonA):
        return (eqPonA - to_eqPonA(width, length))**2

    length_array = np.zeros(len(width_array))

    for i, width in enumerate(width_array):
        eqPonA = eqPonA_array[i]
        length_array[i] = minimize(
            to_minimise, [1], args=(width, eqPonA),
            method='L-BFGS-B', bounds=((width, None),)).x

    return length_array


def create_model(width, eqPonA, factor):

    def model(x, y):
        bbox = [
            np.min([np.min(width), np.min(x)]),
            np.max([np.max(width), np.max(x)]),
            np.min([np.min(eqPonA), np.min(y)]),
            np.max([np.max(eqPonA), np.max(y)])]

        spline = SmoothBivariateSpline(
            width, eqPonA, factor, kx=2, ky=1, bbox=bbox)

        result = spline.ev(x, y)

        return result

    return model


def pull_data(energy=12, applicator=10, ssd=100, return_label=False):
    with open("model_cache/" +
              str(energy) + "MeV_" +
              str(applicator) + "app_" +
              str(ssd) + "ssd.yml", 'r') as file:
        cutout_data = yaml.load(file)

    label = np.array([key for key in cutout_data])
    width = np.array([cutout_data[key]['width'] for key in label])
    length = np.array([cutout_data[key]['length'] for key in label])
    factor = np.array([cutout_data[key]['factor'] for key in label])
    eqPonA = to_eqPonA(width, length)

    if return_label:
        return width, length, eqPonA, factor, label
    else:
        return width, length, eqPonA, factor


def calculate_percent_prediction_differences(width, eqPonA, factor,
                                             keep_nans=False):

    predictions = np.zeros(len(width))
    give = np.zeros(len(width))

    for i in range(len(width)):

        widthTest = np.delete(width, i)
        eqPonATest = np.delete(eqPonA, i)
        factorTest = np.delete(factor, i)

        modelTest = create_model(widthTest, eqPonATest, factorTest)

        predictions[i] = modelTest(width[i], eqPonA[i])
        give[i] = fit_give(
            width[i], eqPonA[i], widthTest, eqPonATest, factorTest)

    percent_prediction_differences = 100*(factor - predictions) / factor

    invalid = give > 0.5

    if keep_nans:
        percent_prediction_differences[invalid] = np.nan
    else:
        percent_prediction_differences = (
            percent_prediction_differences[~invalid])

    return percent_prediction_differences


def prediction_uncertainty(width, eqPonA, factor):

    percent_prediction_differences = calculate_percent_prediction_differences(
        width, eqPonA, factor)

    if len(percent_prediction_differences) > 1:
        prediction_uncertainty = (
            np.std(percent_prediction_differences, ddof=1) /
            c4(len(percent_prediction_differences)))
        total = (
            prediction_uncertainty +
            np.abs(np.mean(percent_prediction_differences)))
    else:
        total = np.nan

    return total


def estimate_population_uncertainty(data):
    uncertainty = np.std(data, ddof=1) / c4(len(data))
    return uncertainty


def c4(n):

    output = np.sqrt(2/(n-1)) * gamma(n/2) / gamma((n-1)/2)
    if np.isnan(output):
        output = 1

    return output
