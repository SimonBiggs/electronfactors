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

from .utilities import shapely_cutout, shapely_point


def test_min_distance(**kwargs):
    min_distance = kwargs['min_distance']
    point_of_interest = kwargs['point_of_interest']
    cutout = kwargs['cutout']

    is_within = cutout.contains(point_of_interest)

    distance = point_of_interest.distance(cutout.boundary)

    if not(is_within):
        return False

    elif distance < min_distance:
        return False

    else:
        return True


def furthest_possible_distance(point_of_interest, cutout):
    x = point_of_interest.xy[0][0]
    y = point_of_interest.xy[1][0]

    translated_cutout = aff.translate(cutout, xoff=-x, yoff=-y)
    max_bound = np.max(np.abs(translated_cutout.boundary))
    furthest_distance = max_bound * np.sqrt(2)

    return furthest_distance


def make_rays(point_of_interest, cutout, num_rays):
    x_POI = point_of_interest.xy[0][0]
    y_POI = point_of_interest.xy[1][0]

    ray_length = furthest_possible_distance(point_of_interest, cutout)

    dtheta = 2*np.pi / num_rays
    theta = np.arange(-np.pi, np.pi, dtheta) - 0.009365454751752392

    x_points = x_POI + ray_length * np.cos(theta)
    y_points = y_POI + ray_length * np.sin(theta)

    coords = [
        ((x_POI, y_POI), (x_points[i], y_points[i])) for i in range(num_rays)
    ]

    rays = geo.MultiLineString(coords)

    return rays


def determine_line_segmentation(distances):

    begin_at_POI = np.array(
        [distances[i][0] == 0.0 for i in range(len(distances))]
    )

    segment_groups_indices = []
    full_lines_index = np.arange(len(begin_at_POI)).astype('float')

    for i in range(1, len(begin_at_POI)):

        if (~begin_at_POI[i]) & (begin_at_POI[i-1]):
            j = int(i)
            new_segment = [j - 1]
            full_lines_index[j - 1] = np.nan

            while ~(begin_at_POI[j]):
                new_segment.append(j)
                full_lines_index[j] = np.nan
                j += 1
                if j == len(begin_at_POI):
                    break

            segment_groups_indices.append(new_segment)

    full_lines_index = full_lines_index[
        ~np.isnan(full_lines_index)
    ].astype('int')

    return full_lines_index, segment_groups_indices


def sector_integration(num_rays=200, **kwargs):
    x = kwargs['x']
    y = kwargs['y']
    circle_fit = kwargs['circle_fit']
    min_distance = kwargs['min_distance']
    point_of_interest = shapely_point(*kwargs['point_of_interest'])

    cutout = shapely_cutout(x, y)

    if not(test_min_distance(min_distance=min_distance,
                             point_of_interest=point_of_interest,
                             cutout=cutout)):
        raise Exception("Point of interest is too close"
                        " to edge or is outside of cutout")

    rays = make_rays(point_of_interest, cutout, num_rays)
    intersection = cutout.intersection(rays)

    line_ends = [
        geo.MultiPoint(
            intersection[i].coords
        ) for i in range(len(intersection))
    ]

    distances = [
        [
            line_ends[j][i].distance(point_of_interest) for i in range(2)
        ] for j in range(len(intersection))
    ]

    full_lines_index, segment_groups_indices = determine_line_segmentation(
        distances)

    ray_factor = []
    for i in full_lines_index:
        ray_factor.append(
            circle_fit(distances[i][1]) - circle_fit(distances[i][0])
        )

    for item in segment_groups_indices:
        new_segment_factor = []
        for i in item:
            new_segment_factor.append(
                circle_fit(distances[i][1]) - circle_fit(distances[i][0])
            )

        ray_factor.append(np.sum(new_segment_factor))

    factor = np.mean(ray_factor)

    return factor
