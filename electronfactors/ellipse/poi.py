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


def find_poi(n=5, confidence=0.001, **kwargs):
    XCoords = kwargs['XCoords']
    YCoords = kwargs['YCoords']

    cutout = shapely_cutout(XCoords, YCoords)
    center = cutout.centroid

    initial = np.array([0, 0])

    bound = np.hypot(
        np.diff(cutout.bounds[::2]),
        np.diff(cutout.bounds[1::2])
    )

    step_noise = [bound] * 2

    def to_minimise(optimiser_input):
        x = optimiser_input[0]
        y = optimiser_input[1]

        point = geo.Point(x, y)
        is_within = cutout.contains(point)
        edge_distance = point.distance(cutout.boundary)

        if not(is_within):
            edge_distance = -edge_distance

        centroid_weighting = point.distance(center) / bound

        return centroid_weighting - edge_distance

    optimiser = _CustomBasinhopping(
        to_minimise=to_minimise,
        initial=initial,
        step_noise=step_noise,
        n=n,
        confidence=confidence
    )

    poi = np.array([
        optimiser.result[0],
        optimiser.result[1]
    ])

    return poi
