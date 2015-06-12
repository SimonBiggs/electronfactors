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
import matplotlib.pyplot as plt

from .utilities import shapely_cutout, _CustomBasinhopping

from ..visuals.shape_display import display_shapely, display_equivalent_ellipse


def poi_distance_method(n=5, confidence=0.001, **kwargs):
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


# def poi_enclosed_circle_method(weighting=1, n=5, confidence=0.001, **kwargs):
#     XCoords = kwargs['XCoords']
#     YCoords = kwargs['YCoords']
#
#     cutout = shapely_cutout(XCoords, YCoords)
#     centroid = cutout.centroid
#
#     initial = np.array([0, 0, 1])
#
#     bound = np.hypot(
#         np.diff(cutout.bounds[::2]),
#         np.diff(cutout.bounds[1::2]))
#
#     step_noise = [bound] * 3
#
#     def to_minimise(optimiser_input):
#         x = optimiser_input[0]
#         y = optimiser_input[1]
#         width = optimiser_input[2]
#
#         point = geo.Point(x, y)
#         circle = point.buffer(width/2)
#
#         disjoint_overshoot = circle.difference(cutout).area
#         disjoint_undershoot = cutout.difference(circle).area
#
#         centroid_weighting = point.distance(centroid) / bound
#
#         return (
#             disjoint_overshoot * weighting +
#             disjoint_undershoot +
#             centroid_weighting)
#
#     optimiser = _CustomBasinhopping(
#         to_minimise=to_minimise,
#         initial=initial,
#         step_noise=step_noise,
#         n=n,
#         confidence=confidence
#     )
#
#     poi = np.array([
#         optimiser.result[0],
#         optimiser.result[1]
#     ])
#
#     width = optimiser.result[2]
#
#     return poi, width


def equivalent_ellipse(display=False, **kwargs):
    XCoords = kwargs['XCoords']
    YCoords = kwargs['YCoords']

    # poi, width = poi_enclosed_circle_method(XCoords=XCoords, YCoords=YCoords)
    poi = poi_distance_method(XCoords=XCoords, YCoords=YCoords)

    width = find_width(XCoords=XCoords, YCoords=YCoords, poi=poi)
    length = find_length(XCoords=XCoords, YCoords=YCoords, width=width)

    if display:
        cutout = shapely_cutout(XCoords, YCoords)

        fig = plt.figure()
        ax = fig.add_subplot(111)

        display_shapely(cutout, ax=ax)

        plt.scatter(*poi)
        display_equivalent_ellipse(ax=ax, poi=poi, width=width, length=length)
        plt.show()

    output = {
        'poi': poi,
        'width': width,
        'length': length
    }

    return output


def find_width(**kwargs):
    XCoords = kwargs['XCoords']
    YCoords = kwargs['YCoords']
    poi = kwargs['poi']

    cutout = shapely_cutout(XCoords, YCoords)

    point = geo.Point(*poi)
    is_within = cutout.contains(point)
    if not(is_within):
        raise Exception("POI not within cutout")

    distance = point.distance(cutout.boundary)

    return distance * 2


def find_length(**kwargs):
    XCoords = kwargs['XCoords']
    YCoords = kwargs['YCoords']
    width = kwargs['width']

    cutout = shapely_cutout(XCoords, YCoords)
    area = cutout.area

    length = 4 * area / (np.pi * width)

    return length
