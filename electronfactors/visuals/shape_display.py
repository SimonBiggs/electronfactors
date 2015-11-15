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
import matplotlib.pyplot as plt
import descartes as des

from .utilities import make_ellipse
from ..ellipse.utilities import shapely_cutout


def display_equivalent_ellipse(ax=None, **kwargs):
    poi = kwargs['poi']

    ellipse = make_ellipse(**kwargs)
    display_shapely(ellipse, ax=ax, random_colours=False)

    plt.scatter(*poi)


def display_shapely(shape, ax=None, random_colours=True, alpha=0.3):
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)

    if random_colours:
        colours = np.append(
            np.random.uniform(size=3), alpha)
    else:
        colours = [0, 0, 0, alpha]

    patch = des.PolygonPatch(
        shape,
        fc=colours)
    ax.add_patch(patch)

    ax.axis("equal")
    plt.grid(True)


def display_stored_cutout(**kwargs):
    XCoords = kwargs['XCoords']
    YCoords = kwargs['YCoords']
    poi = kwargs['poi']
    width = kwargs['width']
    length = kwargs['length']

    cutout = shapely_cutout(XCoords, YCoords)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    display_shapely(cutout, ax=ax)

    plt.scatter(*poi)
    display_equivalent_ellipse(ax=ax, poi=poi, width=width, length=length)
    plt.show()
