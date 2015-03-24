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
import shapely.affinity as aff
import shapely.geometry as geo
import shapely.ops as ops

from .utilities import shapely_cutout, shapely_circle


def create_intersection_cut(ratio, boundingDiagonal):
    placementAngle = np.pi/2 * (1 - ratio)
    x = boundingDiagonal * np.cos(placementAngle)
    y = boundingDiagonal * np.sin(placementAngle)

    top_cut_coords = [(-x, y), (x, y), (0, 0)]
    bottom_cut_coords = [(-x, -y), (x, -y), (0, 0)]

    top_cut = geo.Polygon(top_cut_coords)
    bottom_cut = geo.Polygon(bottom_cut_coords)

    intersection_cut = geo.MultiPolygon([top_cut, bottom_cut])

    return intersection_cut


def create_difference_cut(ratio, boundingDiagonal):
    placementAngle = np.pi/2 * (1 - ratio)

    x = boundingDiagonal * np.cos(placementAngle)
    y = boundingDiagonal * np.sin(placementAngle)

    left_cut_coords = [(-x, -y), (-x, y), (0, 0)]
    right_cut_coords = [(x, y), (x, -y), (0, 0)]

    left_cut = geo.Polygon(left_cut_coords)
    right_cut = geo.Polygon(right_cut_coords)

    difference_cut = geo.MultiPolygon([left_cut, right_cut])

    return difference_cut


def create_segment(region, ratio):
    boundingDiagonal = np.max(region.bounds) * np.sqrt(2)

    if (ratio >= 0.5) & (ratio < 1):
        cut = create_difference_cut(ratio, boundingDiagonal)
        segment = region.difference(cut)
        return segment

    elif (ratio > 0):
        cut = create_intersection_cut(ratio, boundingDiagonal)
        segment = region.intersection(cut)
        return segment

    else:
        raise Exception("Unexpected ratio")


def straighten(poi=[0, 0], **kwargs):

    XCoords = kwargs['XCoords']
    YCoords = kwargs['YCoords']
    cutout = shapely_cutout(XCoords, YCoords)
    centredCutout = aff.translate(cutout, xoff=-poi[0], yoff=-poi[1])

    numZones = int(
        np.ceil(
            100 * np.max(np.abs(centredCutout.bounds)) * np.sqrt(2)
        )
    )
    maxRadii = numZones / 100

    zoneWidth = maxRadii / numZones * 1.00001
    zoneMinBound = np.arange(0, maxRadii, 0.01)
    zoneMaxBound = zoneMinBound + zoneWidth

    zone_list = [
        shapely_circle(zoneMaxBound[i]).difference(
            shapely_circle(zoneMinBound[i])
        )
        for i in range(numZones)
        ]

    zones = [geo.Polygon(zone_list[i]) for i in range(numZones)]

    zoneRatioAreas = np.zeros(numZones)

    for i in range(numZones):
        intersectionArea = centredCutout.intersection(zones[i]).area
        zoneArea = zones[i].area
        zoneRatioAreas[i] = intersectionArea / zoneArea

    ploygon_list = []
    for i in range(numZones):
        if zoneRatioAreas[i] == 1:
            ploygon_list.append(zones[i])

        elif zoneRatioAreas[i] > 0:
            add_section = create_segment(zones[i], zoneRatioAreas[i])
            ploygon_list.append(add_section)

    straightened = ops.unary_union(ploygon_list)
    translated = aff.translate(straightened, xoff=poi[0], yoff=poi[1])
    simplified = translated.simplify(0.01)

    x, y = simplified.exterior.xy

    return x, y
