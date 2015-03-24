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

    width = find_width(XCoords=XCoords, YCoords=YCoords, poi=poi)
    length = find_length(XCoords=XCoords, YCoords=YCoords, width=width)

    if display:
        staightened_XCoords, staightened_YCoords = straighten(
            poi=poi, XCoords=XCoords, YCoords=YCoords
        )
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
    YCoords = kwargs['YCoords']
    poi = kwargs['poi']

    cutout = shapely_cutout(XCoords, YCoords)

    max_radii = np.hypot(np.ptp(XCoords), np.ptp(YCoords))
    radii, thin_donuts = make_thin_donuts(poi, max_radii)

    segment_ratios = np.array([
        donut.intersection(cutout).area / donut.area for donut in thin_donuts
    ])

    possible_widths = 2 * radii * np.sin(segment_ratios * np.pi/2)
    width = np.max(possible_widths)

    return width


def make_thin_donuts(poi, max_radii, dr=0.01):
    radii = np.arange(0, max_radii, dr) + dr
    circles = [geo.Point(*poi).buffer(r) for r in np.append(0, radii)]

    thin_donuts = [
        circles[i+1].difference(circles[i]) for i in range(len(radii))
    ]

    return radii, thin_donuts


def find_length(**kwargs):
    XCoords = kwargs['XCoords']
    YCoords = kwargs['YCoords']
    width = kwargs['width']

    cutout = shapely_cutout(XCoords, YCoords)
    area = cutout.area

    length = 4 * area / (np.pi * width)

    return length
