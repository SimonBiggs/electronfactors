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
from electronfactors.ellipse.equivalent import EquivalentEllipse

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


XCoords = np.array([-1, -0.2, 0, 0.7, 1, 0])*4
YCoords = np.array([0, -1, -.8, 0, .6, 1])*4

equivalentEllipse = EquivalentEllipse(
    x=XCoords, y=YCoords, circle_fit=circle_fit, quick=True)


def test_ellipse_dimensions():
    assert np.abs(equivalentEllipse.width - 5.15) < 0.1
    assert np.abs(equivalentEllipse.length - 7.99) < 0.1
