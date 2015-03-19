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

from scipy.interpolate import SmoothBivariateSpline

from ..ellipse.equivalent import EquivalentEllipse


def create_spline(width, length, factor):
    ratio = width/length
    eqPonA = 2*(3*(ratio+1) - np.sqrt((3*ratio+1)*(ratio+3))) / width

    spline = SmoothBivariateSpline(width, eqPonA, factor, kx=2, ky=2)

    return spline


def predict_factor(spline, width, length):
    ratio = width/length
    eqPonA = 2*(3*(ratio+1) - np.sqrt((3*ratio+1)*(ratio+3))) / width

    return spline.ev(width, eqPonA)


# Include a factor guess
def iteration(n=5, ssd=100, **kwargs):

    energy = kwargs['energy']
    applicator = kwargs['applicator']

    filepath = (
        "model_cache/" +
        str(energy) + "MeV_" +
        str(applicator) + "app_" +
        str(ssd) + "ssd.yml"
    )

    with open(filepath, 'r') as inputFile:
        input_dict = yaml.load(inputFile)

    label = [key for key in input_dict]
    poi = [input_dict[key]['poi'] for key in label]

    width = np.array([input_dict[key]['width'] for key in label])
    length = np.array([input_dict[key]['length'] for key in label])
    factor = np.array([input_dict[key]['factor'] for key in label])
    spline = create_spline(width, length, factor)

    min_radii = np.min(width/2)

    def circle_fit(radii):
        if radii >= min_radii:
            result = spline.ev(radii*2, 2/radii)
        else:
            result = 0.
        return result

    output_dict = dict()
    for i, key in enumerate(label):
        XCoords = input_dict[key]['XCoords']
        YCoords = input_dict[key]['YCoords']

        equivalent_ellipse = EquivalentEllipse(
            x=XCoords, y=YCoords,
            circle_fit=circle_fit, n=n,
            min_distance=min_radii,
            poi=poi[i]
        )

        output_dict[key] = dict()
        output_dict[key]['width'] = equivalent_ellipse.width
        output_dict[key]['length'] = equivalent_ellipse.length

    width_new = np.array([output_dict[key]['width'] for key in label])
    length_new = np.array([output_dict[key]['length'] for key in label])

    for i, key in enumerate(label):
        width_test = np.delete(width_new, i)
        length_test = np.delete(length_new, i)
        factor_test = np.delete(factor, i)

        spline_test = create_spline(width_test, length_test, factor_test)

        predicted_factor = predict_factor(
            spline_test, width_new[i], length_new[i])

        output_dict[key]['predicted_factor'] = round(
            float(predicted_factor), 4)

    for i, key in enumerate(label):
        output_dict[key]['XCoords'] = input_dict[key]['XCoords']
        output_dict[key]['YCoords'] = input_dict[key]['YCoords']
        output_dict[key]['factor'] = input_dict[key]['factor']
        output_dict[key]['energy'] = input_dict[key]['energy']
        output_dict[key]['applicator'] = input_dict[key]['applicator']
        output_dict[key]['ssd'] = input_dict[key]['ssd']
        output_dict[key]['poi'] = input_dict[key]['poi']

        output_dict[key]['width'] = round(
            float(output_dict[key]['width']), 2)
        output_dict[key]['length'] = round(
            float(output_dict[key]['length']), 2)

    with open(filepath, 'w') as outfile:
        outfile.write(yaml.dump(output_dict, default_flow_style=False))
