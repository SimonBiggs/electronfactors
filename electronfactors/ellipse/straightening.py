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

from .utilities import shapely_cutout, create_zones


# This could likely be flattened and made functional instead of an object.
class Straighten(object):
    """Returns a straightened cutout. Requires defined centre and shape
    defining X and Y coords.
    """
    def __init__(self, numZones=1000, debug=False, **kwargs):
        self.debug = debug

        self.cutoutXCoords = kwargs['x']
        self.cutoutYCoords = kwargs['y']
        self.cutout = shapely_cutout(self.cutoutXCoords, self.cutoutYCoords)

        self.centre = kwargs['centre']

        self.centredCutout = aff.translate(self.cutout,
                                           xoff=-self.centre[0],
                                           yoff=-self.centre[1])

        self.maxRadii = np.max(self.centredCutout.bounds) * np.sqrt(2)
        self.numZones = numZones

        self.zoneMidDist, self.zoneRegions = create_zones(
            self.numZones, self.maxRadii)

        self._straighten()

    def _straighten(self):
        self.zoneRatioAreas = np.zeros(self.numZones)

        for i in range(self.numZones):
            self.zoneRatioAreas[i] = (
                self.centredCutout.intersection(self.zoneRegions[i]).area /
                self.zoneRegions[i].area)

        self.placementAngles = 90 - 90*self.zoneRatioAreas

        placePointRef = (
            self.placementAngles > 0) & (self.placementAngles < 90)

        numSectorPoints = sum(placePointRef)
        straightenedSectorX = np.zeros(numSectorPoints)
        straightenedSectorY = np.zeros(numSectorPoints)

        for i in range(numSectorPoints):
            hypot = self.zoneMidDist[placePointRef][i]
            angle = self.placementAngles[placePointRef][i]

            straightenedSectorX[i] = hypot * np.cos(np.pi/180 * angle)
            straightenedSectorY[i] = hypot * np.sin(np.pi/180 * angle)

        self.straightenedRawXCoords = np.concatenate(
            (straightenedSectorX,
             -straightenedSectorX[::-1],
             -straightenedSectorX,
             straightenedSectorX[::-1]))

        self.straightenedRawYCoords = np.concatenate(
            (straightenedSectorY,
             straightenedSectorY[::-1],
             -straightenedSectorY,
             -straightenedSectorY[::-1]))

        self.rawStraightenedCutout = aff.rotate(shapely_cutout(
            self.straightenedRawXCoords,
            self.straightenedRawYCoords), -45)

        self.straightenedCutout = self.rawStraightenedCutout.simplify(0.01)

        x, y = self.straightenedCutout.exterior.xy
        self.straightenedXCoords = x
        self.straightenedYCoords = y
