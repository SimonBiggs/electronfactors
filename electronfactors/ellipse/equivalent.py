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

from .poi import find_poi
from .utilities import shapely_cutout

from ..visuals.shape_display import display_shapely, display_equivalent_ellipse


def equivalent_ellipse(display=False, **kwargs):
    XCoords = kwargs['XCoords']
    YCoords = kwargs['YCoords']

    poi = find_poi(XCoords=XCoords, YCoords=YCoords)

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
