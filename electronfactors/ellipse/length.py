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
import shapely.geometry as geo
import shapely.affinity as aff

import matplotlib.pyplot as plt

from .utilities import shapely_cutout, _CustomBasinhopping
from .straightening import straighten

from ..visuals.shape_display import display_shapely, display_equivalent_ellipse


def find_length(n=5, confidence=0.00001, debug=True, **kwargs):
    cutout_XCoords = kwargs['XCoords']
    cutout_YCoords = kwargs['YCoords']
    poi = kwargs['poi']
    width = kwargs['width']

    debug = True

    circle = geo.Point(*poi).buffer(width/2)

    staightened_XCoords, staightened_YCoords = straighten(
        poi=poi, XCoords=cutout_XCoords, YCoords=cutout_YCoords
    )

    staightened_XCoords = staightened_XCoords + poi[0]
    staightened_YCoords = staightened_YCoords + poi[1]

    straightened = shapely_cutout(staightened_XCoords, staightened_YCoords)

    if debug:
        cutout = shapely_cutout(cutout_XCoords, cutout_YCoords)

        fig = plt.figure()
        ax = fig.add_subplot(111)

        display_shapely(cutout, ax=ax)
        display_shapely(straightened, ax=ax)
        display_shapely(circle, ax=ax)

        plt.scatter(*poi)

        # plt.show()

    initial = np.array([1.5])
    step_noise = np.array([0.2])

    def to_minimise(optimiser_input):
        stretch_factor = np.abs(optimiser_input[0] - 1) + 1
        stretched = aff.scale(circle, yfact=stretch_factor)

        disjoint_area = (
            stretched.difference(straightened).area +
            straightened.difference(stretched).area
        )
        return disjoint_area

    optimiser = _CustomBasinhopping(
        to_minimise=to_minimise,
        initial=initial,
        step_noise=step_noise,
        n=n,
        confidence=confidence
    )

    stretch_factor = np.abs(optimiser.result[0] - 1) + 1
    length = stretch_factor * width

    if debug:
        display_equivalent_ellipse(ax=ax, poi=poi, width=width, length=length)
        plt.show()

    return length
