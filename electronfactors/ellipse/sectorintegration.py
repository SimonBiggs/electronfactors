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


def shapely_cutout(XCoords, YCoords):
    """Returns the shapely cutout defined by the x and y coordinates.
    """
    return geo.Polygon(np.transpose((XCoords, YCoords)))


# This doesn't need to be an object. I need to flatten this and turn it into
# a clear set of functions.
class SectorIntegration(object):

    def __init__(self,
                 sectors=100,
                 bound=25,
                 ignoreErrors=False,
                 debug=False,
                 **kwargs):

        self.ignoreErrors = ignoreErrors

        if ignoreErrors:
            self.minDistance = 0
        else:
            self.minDistance = kwargs['minDistance']

        self.cutoutXCoords = kwargs['x']
        self.cutoutYCoords = kwargs['y']
        self.cutout = shapely_cutout(self.cutoutXCoords, self.cutoutYCoords)

        self.circle_fit = kwargs['circle_fit']

        self.centre = [tuple(kwargs['centre'])]
        self.centreIsWithin = self.cutout.contains(geo.Point(self.centre))

        self.numSectors = sectors
        resolution = int(self.numSectors/4)
        self.boundary = geo.Point(self.centre).buffer(bound*np.sqrt(2),
                                                      resolution=resolution)

        self.debug = debug

        self.factor = self._factor_calculate()

    # This function is too complex.
    def _factor_calculate(self):

        self.sectorMidline = [0]*self.numSectors
        self.intersectionSet = [0]*self.numSectors

        self.sectorFactors = np.zeros(self.numSectors)
        self.dist = [0]*self.numSectors

        for i in range(self.numSectors):
            self.sectorMidline[i] = geo.LineString(
                self.centre + [self.boundary.exterior.coords[i]])
            self.intersectionSet[i] = self.sectorMidline[i].intersection(
                self.cutout.exterior)

            if type(self.intersectionSet[i]) is geo.point.Point:
                # One intersection occured

                if self.centreIsWithin:
                    # One intersection should only happen if
                    # the centre is within the shape
                    self.dist[i] = self.sectorMidline[i].project(
                        self.intersectionSet[i])
                    self.sectorFactors[i] = self.circle_fit(self.dist[i])

                    if self.dist[i] < self.minDistance and not(
                        self.ignoreErrors):
                        raise Exception("Centre too close to edge")

                else:
                    if self.ignoreErrors:
                        self.sectorFactors[i] = np.nan
                    else:
                        raise Exception("Unexpected intersection result")

            elif type(self.intersectionSet[i]) is geo.multipoint.MultiPoint:
                # Multiple intersections have occured
                self.dist[i] = np.zeros(len(self.intersectionSet[i]))

                for j in range(len(self.intersectionSet[i])):
                    point = self.intersectionSet[i][j]
                    self.dist[i][j] = self.sectorMidline[i].project(point)

                self.dist[i] = np.sort(self.dist[i])

                if ((np.mod(len(self.intersectionSet[i]), 2) == 1 ) &
                    (self.centreIsWithin)):
                    # If the centre is within the shape,
                    # number of intersections must be odd
                    self.sectorFactors[i] = (
                        sum(self.circle_fit(self.dist[i][::2])) -
                        sum(self.circle_fit(self.dist[i][1::2])))
                elif ((np.mod(len(self.intersectionSet[i]), 2) == 0 ) &
                      (not(self.centreIsWithin))):
                    # If the centre is outside the shape,
                    # number of intersections must be even
                    self.sectorFactors[i] = (
                        sum(self.circle_fit(self.dist[i][1::2])) -
                        sum(self.circle_fit(self.dist[i][::2])))
                else:
                    if self.ignoreErrors:
                        self.sectorFactors[i] = np.nan
                    else:
                        raise Exception("Unexpected intersection result")

                if (self.dist[i][0] <
                    self.minDistance and not(self.ignoreErrors)):

                    raise Exception("Centre too close to edge")

            elif ((self.sectorMidline[i].disjoint(self.cutout.exterior)) &
                  (not(self.centreIsWithin))):
                # No intersection
                0

            else:
                if self.ignoreErrors:
                    self.sectorFactors[i] = np.nan
                else:
                    raise Exception("Unexpected intersection result")

        if self.ignoreErrors:
            factor = np.nanmean(self.sectorFactors)
        else:
            factor = np.mean(self.sectorFactors)

        return factor
