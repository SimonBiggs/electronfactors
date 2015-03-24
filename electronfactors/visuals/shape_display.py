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

# from ..ellipse.utilities import _CustomBasinhopping, shapely_ellipse
from ..ellipse.utilities import shapely_ellipse


def display_equivalent_ellipse(ax=None, **kwargs):
    poi = kwargs['poi']
    width = kwargs['width']
    length = kwargs['length']

    ellipse = shapely_ellipse([poi[0], poi[1], width, length, 0])

    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)

    patch = des.PolygonPatch(
        ellipse,
        fc=np.random.uniform(size=3),
        alpha=0.5)
    ax.add_patch(patch)

    plt.scatter(*poi)
    ax.axis("equal")
    plt.grid(True)


def display_shapely(shape, ax=None, **kwargs):
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)

    patch = des.PolygonPatch(
        shape,
        fc=np.random.uniform(size=3),
        alpha=0.5)
    ax.add_patch(patch)

    ax.axis("equal")
    plt.grid(True)
