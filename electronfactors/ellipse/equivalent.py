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

import shapely.affinity as aff

from .centre import FindCentre
from .straightening import straighten
from .fitting import WeightedFitEllipse, StandardFitEllipse
from .utilities import shapely_cutout


class EquivalentEllipse(object):
    """Returns an equivalent ellipse. Requires the input of cutout X and
       Y coords along with the centre_fit function.
    """
    def __init__(self, n=5, weighted=False, **kwargs):
        self.cutoutXCoords = kwargs['x']
        self.cutoutYCoords = kwargs['y']
        self.circle_fit = kwargs['circle_fit']
        self.min_distance = kwargs['min_distance']
        self.inputCutout = shapely_cutout(
            self.cutoutXCoords,
            self.cutoutYCoords
        )

        self._FoundCentre = FindCentre(x=self.cutoutXCoords,
                                       y=self.cutoutYCoords,
                                       n=n,
                                       min_distance=self.min_distance,
                                       circle_fit=self.circle_fit)

        self.centre = self._FoundCentre.centre

        x, y = straighten(
            XCoords=self.cutoutXCoords,
            YCoords=self.cutoutYCoords,
            centre=self.centre
        )

        self.straightenedXCoords = x
        self.straightenedYCoords = y

        if weighted:
            self._FittedEllipse = WeightedFitEllipse(
                x=self.straightenedXCoords,
                y=self.straightenedYCoords,
                n=n,
                circle_fit=self.circle_fit)
        else:
            self._FittedEllipse = StandardFitEllipse(
                x=self.straightenedXCoords,
                y=self.straightenedYCoords,
                n=n)

        self.centredCutout = aff.translate(
            self.inputCutout,
            xoff=-self.centre[0],
            yoff=-self.centre[1]
        )
        self.straightenedCutout = shapely_cutout(
            self.straightenedXCoords,
            self.straightenedYCoords
        )

        self.eqEllipse = self._FittedEllipse.ellipse
        self.eqEllipseXCoords = self._FittedEllipse.ellipseXCoords
        self.eqEllipseYCoords = self._FittedEllipse.ellipseYCoords

        self.width = self._FittedEllipse.width
        self.length = self._FittedEllipse.length
