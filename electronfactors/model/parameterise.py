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
import shapely.affinity as aff

from ..visuals.shape_display import display_shapely
from ..ellipse.equivalent import equivalent_ellipse
from ..ellipse.utilities import (
    shapely_ellipse, shapely_cutout, _CustomBasinhopping)


def parameterise(display=False, working_directory="imported_data/",
                 optimise_position=False, **kwargs):

    if working_directory is not None:
        input_filepath = working_directory + "merged.yml"
        output_filepath = working_directory + "parameterised.yml"

        with open(input_filepath, 'r') as file:
            input_dict = yaml.load(file)
    else:
        input_dict = kwargs['input_dict']

    output_dict = input_dict.copy()
    for i, key in enumerate(input_dict):
        XCoords = input_dict[key]['XCoords']
        YCoords = input_dict[key]['YCoords']

        if display:
            print(str(key) + ":")

        ellipse_values = equivalent_ellipse(
            XCoords=XCoords, YCoords=YCoords)

        cutout = shapely_cutout(XCoords, YCoords)
        ellipse = shapely_ellipse([
            0, 0,
            ellipse_values['width'], ellipse_values['length'],
            0])

        if optimise_position:
            mid, angle, ellipse = calculate_optimal_position(cutout, ellipse)
            mid = [float(round(item, 2)) for item in mid]
            angle = float(round(angle, 2))

            output_dict[key]['mid'] = mid
            output_dict[key]['angle'] = angle

        if display:
            fig = plt.figure()
            ax = fig.add_subplot(111)

            display_shapely(cutout, ax=ax)
            display_shapely(ellipse, ax=ax)

            plt.show()

        width = float(round(ellipse_values['width'], 2))
        length = float(round(ellipse_values['length'], 2))
        poi = [float(round(item, 2)) for item in ellipse_values['poi']]

        output_dict[key]['width'] = width
        output_dict[key]['length'] = length
        output_dict[key]['poi'] = poi

    if working_directory is not None:
        with open(output_filepath, 'w') as file:
            file.write(yaml.dump(output_dict))
    else:
        return output_dict


def calculate_optimal_position(cutout, ellipse):
    initial = np.array([0, 0, 0])

    bound = np.hypot(
        np.diff(cutout.bounds[::2]),
        np.diff(cutout.bounds[1::2])
    )

    step_noise = [bound] * 2
    step_noise.append(90)

    def to_minimise(optimiser_input):
        rotated = aff.rotate(
            ellipse, optimiser_input[2], origin='centroid')
        translated = aff.translate(
            rotated, xoff=optimiser_input[0], yoff=optimiser_input[1])

        disjoint_area = (
            translated.difference(cutout).area +
            cutout.difference(ellipse).area
        )
        return disjoint_area

    optimiser = _CustomBasinhopping(
        to_minimise=to_minimise,
        initial=initial,
        step_noise=step_noise,
        n=2,
        confidence=0.0001
    )

    mid = optimiser.result[0:2]
    angle = optimiser.result[2]

    rotated = aff.rotate(
        ellipse, angle, origin='centroid')
    translated = aff.translate(
        rotated, xoff=mid[0], yoff=mid[1])

    return mid, angle, translated
