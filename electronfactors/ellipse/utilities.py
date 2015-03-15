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


def shapely_point(x, y):
    return geo.Point([(x, y)])


def shapely_cutout(XCoords, YCoords):
    """Returns the shapely cutout defined by the x and y coordinates.
    """
    return geo.Polygon(np.transpose((XCoords, YCoords)))


def shapely_ellipse(ellipseRaw):
    """Given raw ellipse values create a shapely ellipse."""
    xPosition = ellipseRaw[0]
    yPosition = ellipseRaw[1]

    width = ellipseRaw[2]
    length = ellipseRaw[3]

    rotation = ellipseRaw[4]

    unitCircle = geo.Point(0, 0).buffer(1)
    stretched = aff.scale(unitCircle, xfact=width/2, yfact=length/2)
    translated = aff.translate(
        stretched,
        xoff=xPosition,
        yoff=yPosition)
    rotated = aff.rotate(translated, rotation)

    ellipse = rotated

    return ellipse


def shapely_circle(radii):
    return geo.Point(0, 0).buffer(radii)


def create_zones(numZones, maxRadii):
    zoneBoundaryRadii = np.linspace(0, maxRadii, numZones + 1)
    zoneBoundaries = [0]*(numZones+1)
    zoneRegions = [0]*numZones
    zoneMidDist = (zoneBoundaryRadii[0:-1] + zoneBoundaryRadii[1:])/2

    for i in range(numZones + 1):
        zoneBoundaries[i] = geo.Point(0, 0).buffer(zoneBoundaryRadii[i])

    for i in range(numZones):
        zoneRegions[i] = zoneBoundaries[i+1].difference(zoneBoundaries[i])

    return zoneMidDist, zoneRegions
