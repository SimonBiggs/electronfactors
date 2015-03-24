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
import matplotlib.pyplot as plt

from .poi import find_poi
from .straightening import straighten
from .utilities import shapely_cutout, _CustomBasinhopping

from ..visuals.shape_display import display_shapely, display_equivalent_ellipse


def equivalent_ellipse(**kwargs):
    XCoords = kwargs['XCoords']
    YCoords = kwargs['YCoords']

    poi = find_poi(XCoords=XCoords, YCoords=YCoords)
    width, length = fitting(XCoords=XCoords, YCoords=YCoords, poi=poi)
    output = {
        'poi': poi,
        'width': width,
        'length': length
    }

    return output


def fitting(n=5, confidence=0.00001, **kwargs):
    cutout_XCoords = kwargs['XCoords']
    cutout_YCoords = kwargs['YCoords']
    poi = kwargs['poi']

    staightened_XCoords, staightened_YCoords = straighten(
        poi=poi, XCoords=cutout_XCoords, YCoords=cutout_YCoords
    )

    straightened = shapely_cutout(staightened_XCoords, staightened_YCoords)

    if True:
        cutout = shapely_cutout(cutout_XCoords, cutout_YCoords)

        fig = plt.figure()
        ax = fig.add_subplot(111)

        display_shapely(cutout, ax=ax)
        display_shapely(straightened, ax=ax)

        plt.scatter(*poi)

    initial = np.array([3, 4])
    step_noise = np.array([2, 2])

    circle = geo.Point(*poi).buffer(0.5)

    def to_minimise(optimiser_input):
        width = optimiser_input[0]
        length = optimiser_input[1]
        ellipse = aff.scale(circle, xfact=width, yfact=length)

        disjoint_area = (
            ellipse.difference(straightened).area +
            straightened.difference(ellipse).area
        )
        return disjoint_area

    optimiser = _CustomBasinhopping(
        to_minimise=to_minimise,
        initial=initial,
        step_noise=step_noise,
        n=n,
        confidence=confidence
    )

    width = optimiser.result[0]
    length = optimiser.result[1]

    if True:
        display_equivalent_ellipse(ax=ax, poi=poi, width=width, length=length)
        plt.show()

    return width, length


# from .width import find_width
# from .length import find_length
#
#
# def equivalent_ellipse(**kwargs):
#     XCoords = kwargs['XCoords']
#     YCoords = kwargs['YCoords']
#
#     poi = find_poi(XCoords=XCoords, YCoords=YCoords)
#     width = find_width(XCoords=XCoords, YCoords=YCoords, poi=poi)
#     length = find_length(XCoords=XCoords, YCoords=YCoords,
#                          poi=poi, width=width)
#
#     output = {
#         'poi': poi,
#         'width': width,
#         'length': length
#     }
#
#     return output


# import shapely.affinity as aff
# from .centre import FindCentre
# from .straightening import straighten
# from .fitting import StandardFitEllipse
# from .utilities import shapely_cutout


# class EquivalentEllipse(object):
#     """Returns an equivalent ellipse. Requires the input of cutout X and
#        Y coords along with the centre_fit function.
#     """
#     def __init__(self, n=5, weighted=False, poi=None, **kwargs):
#         self.cutoutXCoords = kwargs['XCoords']
#         self.cutoutYCoords = kwargs['YCoords']
#         # self.circle_fit = kwargs['circle_fit']
#         # self.min_distance = kwargs['min_distance']
#         self.inputCutout = shapely_cutout(
#             self.cutoutXCoords,
#             self.cutoutYCoords
#         )
#
#         # if poi is None:
#         #     self._FoundCentre = FindCentre(x=self.cutoutXCoords,
#         #                                    y=self.cutoutYCoords,
#         #                                    n=n,
#         #                                    min_distance=self.min_distance,
#         #                                    circle_fit=self.circle_fit)
#         #
#         #     self.centre = self._FoundCentre.centre
#         # else:
#         #     self.centre = poi
#
#         self.poi = find_poi(
#             XCoords=self.cutoutXCoords,
#             YCoords=self.cutoutYCoords
#         )
#
#         x, y = straighten(
#             XCoords=self.cutoutXCoords,
#             YCoords=self.cutoutYCoords,
#             poi=self.poi
#         )
#
#         self.straightenedXCoords = x
#         self.straightenedYCoords = y
#
#         # if weighted:
#         #     self._FittedEllipse = WeightedFitEllipse(
#         #         x=self.straightenedXCoords,
#         #         y=self.straightenedYCoords,
#         #         n=n,
#         #         circle_fit=self.circle_fit)
#         # else:
#         #     self._FittedEllipse = StandardFitEllipse(
#         #         x=self.straightenedXCoords,
#         #         y=self.straightenedYCoords,
#         #         n=n)
#
#         self._FittedEllipse = StandardFitEllipse(
#             x=self.straightenedXCoords,
#             y=self.straightenedYCoords,
#             n=n)
#
#         self.centredCutout = aff.translate(
#             self.inputCutout,
#             xoff=-self.poi[0],
#             yoff=-self.poi[1]
#         )
#         self.straightenedCutout = shapely_cutout(
#             self.straightenedXCoords,
#             self.straightenedYCoords
#         )
#
#         self.eqEllipse = self._FittedEllipse.ellipse
#         self.eqEllipseXCoords = self._FittedEllipse.ellipseXCoords
#         self.eqEllipseYCoords = self._FittedEllipse.ellipseYCoords
#
#         self.width = self._FittedEllipse.width
#         self.length = self._FittedEllipse.length
