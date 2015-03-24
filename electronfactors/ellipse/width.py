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

from .utilities import shapely_cutout, _CustomBasinhopping


def find_width(n=5, confidence=0.00001, **kwargs):
    XCoords = kwargs['XCoords']
    YCoords = kwargs['YCoords']
    poi = kwargs['poi']

    cutout = shapely_cutout(XCoords, YCoords)

    initial = np.array([3])
    step_noise = np.array([1])

    def to_minimise(optimiser_input):
        radii = optimiser_input[0]
        circle = geo.Point(*poi).buffer(radii)

        disjoint_area = (
            100 * circle.difference(cutout).area +
            cutout.difference(circle).area
        )
        return disjoint_area

    optimiser = _CustomBasinhopping(
        to_minimise=to_minimise,
        initial=initial,
        step_noise=step_noise,
        n=n,
        confidence=confidence
    )

    width = optimiser.result[0] * 2

    return width
