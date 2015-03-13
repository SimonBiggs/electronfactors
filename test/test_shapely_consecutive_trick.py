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
from scipy.interpolate import UnivariateSpline
import shapely.geometry as geo

from electronfactors.ellipse.sectorintegration import make_rays
from electronfactors.ellipse.utilities import shapely_cutout, shapely_point

x = np.array([-3, -2.5, -2, 3, 3, -3, -4, -3])
y = np.array([3, -2, 3, 3, -3, -3, 3, -2])

circle_diameter = np.array([3, 4, 5, 6, 7, 8, 9])
circle_factors = np.array(
    [0.9296, 0.9562, 0.9705, 0.9858, 1.0032, 1.0067, 1.0084])


def circle_fit(radii):

    circle_radii = circle_diameter/2

    spline = UnivariateSpline(circle_radii, circle_factors)
    results = spline(radii)

    results[radii > np.max(circle_radii)] = np.max(circle_factors)
    results[radii < np.min(circle_radii)] = 0

    return results


cutout = shapely_cutout(x, y)
point_of_interest = shapely_point(*[1, 0])

rays = make_rays(point_of_interest, cutout, 100)

intersection = cutout.intersection(rays)
line_ends = [
    geo.MultiPoint(intersection[i].coords) for i in range(len(intersection))
]

distances = [[
        line_ends[j][i].distance(point_of_interest) for i in range(2)
    ] for j in range(len(intersection))]

begin_at_POI = np.array(
    [distances[i][0] == 0.0 for i in range(len(distances))]
)

segment_groups = []
for i in range(1, len(begin_at_POI)):

    if (~begin_at_POI[i]) & (begin_at_POI[i-1]):
        j = int(i)
        new_segment = [j - 1]

        while ~begin_at_POI[j]:
            new_segment.append(j)
            j += 1
            if j == len(begin_at_POI):
                break

        segment_groups.append(new_segment)


def test_shapely_consecutive_assumption():
    for j in range(len(segment_groups)):
        x = [intersection[i].xy[0] for i in segment_groups[j]]
        y = [intersection[i].xy[1] for i in segment_groups[j]]

        gradient_list = [
            (np.diff(x[i]) / np.diff(y[i]))[0] for i in range(len(x))
        ]

        unique_gradient = np.unique(np.round(np.array(gradient_list), 4))
        assert len(unique_gradient) == 1
