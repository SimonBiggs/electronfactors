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

from .centre import FindCentre
from .straightening import Straighten
from .fitting import FitEllipse


class EquivalentEllipse(object):
    """Returns an equivalent ellipse. Requires the input of cutout X and
       Y coords along with the centre_fit function.
    """
    def __init__(self, quick=False, **kwargs):
        self.cutoutXCoords = kwargs['x']
        self.cutoutYCoords = kwargs['y']
        self.circle_fit = kwargs['circle_fit']

        if quick:
            n = 1
        else:
            n = 5

        self._FoundCentre = FindCentre(x=self.cutoutXCoords,
                                       y=self.cutoutYCoords,
                                       n=n,
                                       circle_fit=self.circle_fit)

        self.centre = self._FoundCentre.centre

        self._Straightened = Straighten(x=self.cutoutXCoords,
                                        y=self.cutoutYCoords,
                                        centre=self.centre)

        self._FittedEllipse = FitEllipse(
            x=self._Straightened.straightenedXCoords,
            y=self._Straightened.straightenedYCoords,
            n=n)

        self.inputCutout = self._Straightened.cutout
        self.centredCutout = self._Straightened.centredCutout
        self.straightenedCutout = self._Straightened.straightenedCutout

        self.eqEllipse = self._FittedEllipse.ellipse
        self.eqEllipseXCoords = self._FittedEllipse.ellipseXCoords
        self.eqEllipseYCoords = self._FittedEllipse.ellipseYCoords

        self.width = self._FittedEllipse.width
        self.length = self._FittedEllipse.length
