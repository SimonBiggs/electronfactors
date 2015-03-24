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
# import shapely.geometry as geo
# import shapely.affinity as aff
import matplotlib.pyplot as plt

from .poi import find_poi
from .straightening import straighten
# from .utilities import shapely_cutout, _CustomBasinhopping
from .utilities import shapely_cutout

from ..visuals.shape_display import display_shapely, display_equivalent_ellipse


def equivalent_ellipse(display=False, **kwargs):
    XCoords = kwargs['XCoords']
    YCoords = kwargs['YCoords']

    poi = find_poi(XCoords=XCoords, YCoords=YCoords)
    staightened_XCoords, staightened_YCoords = straighten(
        poi=poi, XCoords=XCoords, YCoords=YCoords
    )

    width = find_width(XCoords=staightened_XCoords)
    length = find_length(XCoords=staightened_XCoords,
                         YCoords=staightened_YCoords,
                         poi=poi, width=width)

    if display:
        cutout = shapely_cutout(XCoords, YCoords)
        straightened = shapely_cutout(staightened_XCoords, staightened_YCoords)

        fig = plt.figure()
        ax = fig.add_subplot(111)

        display_shapely(cutout, ax=ax)
        display_shapely(straightened, ax=ax)

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
    width = np.ptp(XCoords)

    return width


def find_length(**kwargs):
    XCoords = kwargs['XCoords']
    YCoords = kwargs['YCoords']
    width = kwargs['width']

    cutout = shapely_cutout(XCoords, YCoords)
    area = cutout.area

    length = 4 * area / (np.pi * width)

    return length


# def find_length(n=5, confidence=0.00001, **kwargs):
#     XCoords = kwargs['XCoords']
#     YCoords = kwargs['YCoords']
#     poi = kwargs['poi']
#     width = kwargs['width']
#
#     straightened = shapely_cutout(XCoords, YCoords)
#
#     initial = np.array([4])
#     step_noise = np.array([2])
#
#     circle = geo.Point(*poi).buffer(0.5)
#     width_stretched = aff.scale(circle, xfact=width)
#
#     def to_minimise(optimiser_input):
#         length = optimiser_input[0]
#         ellipse = aff.scale(width_stretched, yfact=length)
#
#         disjoint_area = (
#             ellipse.difference(straightened).area +
#             straightened.difference(ellipse).area
#         )
#         return disjoint_area
#
#     optimiser = _CustomBasinhopping(
#         to_minimise=to_minimise,
#         initial=initial,
#         step_noise=step_noise,
#         n=n,
#         confidence=confidence
#     )
#
#     length = optimiser.result[0]
#
#     return length
