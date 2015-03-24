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
from scipy.optimize import basinhopping

import shapely.affinity as aff

from .utilities import shapely_cutout, shapely_ellipse, create_zones

#
# class WeightedFitEllipse(object):
#     """An equivalent ellipse given the x and y coordinates of a cutout.
#     """
#     def __init__(self, n=5,
#                  debug=False,
#                  numZones=100,
#                  **kwargs):
#         self.debug = debug
#
#         self.cutoutXCoords = kwargs['x']
#         self.cutoutYCoords = kwargs['y']
#         self.cutout = shapely_cutout(
#             self.cutoutXCoords,
#             self.cutoutYCoords)
#
#         self.circle_fit = kwargs['circle_fit']
#
#         self.maxRadii = np.max(self.cutout.bounds) * np.sqrt(2)
#         self.numZones = numZones
#
#         self.zoneMidDist, self.zones = create_zones(
#             self.numZones, self.maxRadii)
#
#         circltFitValues = self.circle_fit(self.zoneMidDist)
#         self.zoneWeights = np.diff(np.append([0], circltFitValues))
#
#         self.basinRequiredSuccess = n
#         optimiserResults = self._ellipse_basinhopping()
#         self.ellipseRaw = np.append(np.array([0, 0]), optimiserResults)
#
#         if abs(self.ellipseRaw[2]) < abs(self.ellipseRaw[3]):
#             self.width = abs(self.ellipseRaw[2])
#             self.length = abs(self.ellipseRaw[3])
#
#         else:
#             self.width = abs(self.ellipseRaw[3])
#             self.length = abs(self.ellipseRaw[2])
#
#         self.ellipse = shapely_ellipse(self.ellipseRaw)
#
#         ellipseXCoords, ellipseYCoords = self.ellipse.exterior.xy
#         self.ellipseXCoords = ellipseXCoords
#         self.ellipseYCoords = ellipseYCoords
#
#     def _minimise_function(self, inputs):
#         """Returns the sum of area differences between the an ellipse
#         and the given cutout.
#         """
#         ellipseRaw = np.append(np.array([0, 0]), inputs)
#         ellipse = shapely_ellipse(ellipseRaw)
#
#         disjoint1 = self._weighted_area(self.cutout.difference(ellipse))
#         disjoint2 = self._weighted_area(ellipse.difference(self.cutout))
#
#         return disjoint1 + disjoint2
#
#     def _weighted_area(self, input_region):
#
#         result = 0.
#
#         for i in range(len(self.zones)):
#             result += (
#                 input_region.intersection(self.zones[i]).area *
#                 self.zoneWeights[i])
#
#         return result
#
#     def _ellipse_basinhopping(self):
#         """Fitting the ellipse to the cutout via
#         scipy.optimize.basinhopping.
#         """
#         self.functionReturns = np.empty(self.basinRequiredSuccess)
#         self.functionReturns[:] = np.nan
#
#         self.numSuccess = 0
#
#         minimizerConfig = {"method": 'BFGS'}
#
#         initial_input = np.array([3, 4, 0])
#
#         basinhoppingOutput = basinhopping(
#             self._minimise_function,
#             initial_input,
#             niter=1000,
#             minimizer_kwargs=minimizerConfig,
#             take_step=self._step_function,
#             callback=self._callback_function)
#
#         return basinhoppingOutput.x
#
#     def _step_function(self, optimiserInput):
#         """Step function used by self._ellipse_basinhopping."""
#
#         optimiserInput[0] += np.random.normal(scale=3)     # width
#         optimiserInput[1] += np.random.normal(scale=4)     # length
#         optimiserInput[2] += np.random.normal(scale=90)    # rotation
#
#         return optimiserInput
#
#     def _callback_function(self,
#                            optimiserOutput,
#                            minimiseFunctionOutput,
#                            minimiseAccepted):
#         """Callback function used by self._ellipse_basinhopping."""
#         if self.debug:
#             print(optimiserOutput)
#             print(minimiseFunctionOutput)
#             print(minimiseAccepted)
#             print(" ")
#
#         if minimiseAccepted:
#
#             if self.numSuccess == 0:
#                 # First result
#                 self.functionReturns[0] = minimiseFunctionOutput
#                 self.numSuccess = 1
#
#             elif (minimiseFunctionOutput >=
#                   np.nanmin(self.functionReturns) + 0.0001):
#                 # Reject result
#                 0
#
#             elif (minimiseFunctionOutput >=
#                   np.nanmin(self.functionReturns) - 0.0001):
#                 # Agreeing result
#                 self.functionReturns[self.numSuccess] = minimiseFunctionOutput
#                 self.numSuccess += 1
#
#             elif (minimiseFunctionOutput <
#                   np.nanmin(self.functionReturns) - 0.0001):
#                 # New result
#                 self.functionReturns[0] = minimiseFunctionOutput
#                 self.numSuccess = 1
#
#         if self.numSuccess >= self.basinRequiredSuccess:
#             return True


class VisualFit(object):
    def __init__(self, rigid_shape, fluid_shape, n=2):

        self.rigid_shape = rigid_shape
        self.fluid_shape = fluid_shape

        self.basinRequiredSuccess = n
        self.result = self._shapely_basinhopping()

        self.fitted_shape = self._adjust_shape(self.result)

    def _adjust_shape(self, input):
        translated = aff.translate(
            self.fluid_shape,
            xoff=input[0],
            yoff=input[1])
        rotated = aff.rotate(translated, input[2])
        adjusted = rotated

        return adjusted

    def _minimise_function(self, input):
        """Returns the sum of area differences between the an ellipse
        and the given cutout.
        """
        adjusted = self._adjust_shape(input)

        return (adjusted.difference(self.rigid_shape).area +
                self.rigid_shape.difference(adjusted).area)

    def _shapely_basinhopping(self):
        """Fitting the ellipse to the cutout via
        scipy.optimize.basinhopping.
        """
        self.functionReturns = np.empty(self.basinRequiredSuccess)
        self.functionReturns[:] = np.nan

        self.numSuccess = 0

        minimizerConfig = {"method": 'BFGS'}

        initial_input = np.array([0, 0, 0])

        basinhoppingOutput = basinhopping(
            self._minimise_function,
            initial_input,
            niter=1000,
            minimizer_kwargs=minimizerConfig,
            take_step=self._step_function,
            callback=self._callback_function)

        return basinhoppingOutput.x

    def _step_function(self, optimiserInput):
        """Step function used by self._ellipse_basinhopping."""

        optimiserInput[0] += np.random.normal(scale=1.5)   # x-position
        optimiserInput[1] += np.random.normal(scale=1.5)   # y-position
        optimiserInput[2] += np.random.normal(scale=90)     # rotation

        return optimiserInput

    def _callback_function(self,
                           optimiserOutput,
                           minimiseFunctionOutput,
                           minimiseAccepted):
        """Callback function used by self._ellipse_basinhopping."""

        if minimiseAccepted:

            if self.numSuccess == 0:
                # First result
                self.functionReturns[0] = minimiseFunctionOutput
                self.numSuccess = 1

            elif (minimiseFunctionOutput >=
                  np.nanmin(self.functionReturns) + 0.0001):
                # Reject result
                0

            elif (minimiseFunctionOutput >=
                  np.nanmin(self.functionReturns) - 0.0001):
                # Agreeing result
                self.functionReturns[self.numSuccess] = minimiseFunctionOutput
                self.numSuccess += 1

            elif (minimiseFunctionOutput <
                  np.nanmin(self.functionReturns) - 0.0001):
                # New result
                self.functionReturns[0] = minimiseFunctionOutput
                self.numSuccess = 1

        if self.numSuccess >= self.basinRequiredSuccess:
            return True


class VisualRotate(object):
    def __init__(self, rigid_shape, fluid_shape, n=2):

        self.rigid_shape = rigid_shape
        self.fluid_shape = fluid_shape

        self.basinRequiredSuccess = n
        self.result = self._shapely_basinhopping()

        self.fitted_shape = self._adjust_shape(self.result)

    def _adjust_shape(self, input):
        rotated = aff.rotate(self.fluid_shape, input[0])
        adjusted = rotated

        return adjusted

    def _minimise_function(self, input):
        """Returns the sum of area differences between the an ellipse
        and the given cutout.
        """
        adjusted = self._adjust_shape(input)

        return (adjusted.difference(self.rigid_shape).area +
                self.rigid_shape.difference(adjusted).area)

    def _shapely_basinhopping(self):
        """Fitting the ellipse to the cutout via
        scipy.optimize.basinhopping.
        """
        self.functionReturns = np.empty(self.basinRequiredSuccess)
        self.functionReturns[:] = np.nan

        self.numSuccess = 0

        minimizerConfig = {"method": 'BFGS'}

        initial_input = np.array([0])

        basinhoppingOutput = basinhopping(
            self._minimise_function,
            initial_input,
            niter=1000,
            minimizer_kwargs=minimizerConfig,
            take_step=self._step_function,
            callback=self._callback_function)

        return basinhoppingOutput.x

    def _step_function(self, optimiserInput):
        """Step function used by self._ellipse_basinhopping."""
        optimiserInput[0] += np.random.normal(scale=90)     # rotation

        return optimiserInput

    def _callback_function(self,
                           optimiserOutput,
                           minimiseFunctionOutput,
                           minimiseAccepted):
        """Callback function used by self._ellipse_basinhopping."""

        if minimiseAccepted:

            if self.numSuccess == 0:
                # First result
                self.functionReturns[0] = minimiseFunctionOutput
                self.numSuccess = 1

            elif (minimiseFunctionOutput >=
                  np.nanmin(self.functionReturns) + 0.0001):
                # Reject result
                0

            elif (minimiseFunctionOutput >=
                  np.nanmin(self.functionReturns) - 0.0001):
                # Agreeing result
                self.functionReturns[self.numSuccess] = minimiseFunctionOutput
                self.numSuccess += 1

            elif (minimiseFunctionOutput <
                  np.nanmin(self.functionReturns) - 0.0001):
                # New result
                self.functionReturns[0] = minimiseFunctionOutput
                self.numSuccess = 1

        if self.numSuccess >= self.basinRequiredSuccess:
            return True


class StandardFitEllipse(object):
    """An equivalent ellipse given the x and y coordinates of a cutout.
    """
    def __init__(self, n=5, debug=False, **kwargs):
        self.debug = debug

        self.cutoutXCoords = kwargs['x']
        self.cutoutYCoords = kwargs['y']
        self.cutout = shapely_cutout(
            self.cutoutXCoords,
            self.cutoutYCoords)

        self.basinRequiredSuccess = n
        self.ellipseRaw = self._ellipse_basinhopping()

        if abs(self.ellipseRaw[2]) < abs(self.ellipseRaw[3]):
            self.width = abs(self.ellipseRaw[2])
            self.length = abs(self.ellipseRaw[3])

        else:
            self.width = abs(self.ellipseRaw[3])
            self.length = abs(self.ellipseRaw[2])

        self.ellipse = shapely_ellipse(self.ellipseRaw)

        ellipseXCoords, ellipseYCoords = self.ellipse.exterior.xy
        self.ellipseXCoords = ellipseXCoords
        self.ellipseYCoords = ellipseYCoords

    def _minimise_function(self, ellipseRaw):
        """Returns the sum of area differences between the an ellipse
        and the given cutout.
        """
        ellipse = shapely_ellipse(ellipseRaw)

        return (ellipse.difference(self.cutout).area +
                self.cutout.difference(ellipse).area)

    def _ellipse_basinhopping(self):
        """Fitting the ellipse to the cutout via
        scipy.optimize.basinhopping.
        """
        self.functionReturns = np.empty(self.basinRequiredSuccess)
        self.functionReturns[:] = np.nan

        self.numSuccess = 0

        minimizerConfig = {"method": 'BFGS'}

        initial_input = np.array([0, 0, 3, 4, 0])

        basinhoppingOutput = basinhopping(
            self._minimise_function,
            initial_input,
            niter=1000,
            minimizer_kwargs=minimizerConfig,
            take_step=self._step_function,
            callback=self._callback_function)

        return basinhoppingOutput.x

    def _step_function(self, optimiserInput):
        """Step function used by self._ellipse_basinhopping."""

        optimiserInput[0] += np.random.normal(scale=1.5)   # x-position
        optimiserInput[1] += np.random.normal(scale=1.5)   # y-position
        optimiserInput[2] += np.random.normal(scale=3)     # width
        optimiserInput[3] += np.random.normal(scale=4)     # length
        optimiserInput[4] += np.random.normal(scale=90)    # rotation

        return optimiserInput

    def _callback_function(self,
                           optimiserOutput,
                           minimiseFunctionOutput,
                           minimiseAccepted):
        """Callback function used by self._ellipse_basinhopping."""
        if self.debug:
            print(optimiserOutput)
            print(minimiseFunctionOutput)
            print(minimiseAccepted)
            print(" ")

        if minimiseAccepted:

            if self.numSuccess == 0:
                # First result
                self.functionReturns[0] = minimiseFunctionOutput
                self.numSuccess = 1

            elif (minimiseFunctionOutput >=
                  np.nanmin(self.functionReturns) + 0.0001):
                # Reject result
                0

            elif (minimiseFunctionOutput >=
                  np.nanmin(self.functionReturns) - 0.0001):
                # Agreeing result
                self.functionReturns[self.numSuccess] = minimiseFunctionOutput
                self.numSuccess += 1

            elif (minimiseFunctionOutput <
                  np.nanmin(self.functionReturns) - 0.0001):
                # New result
                self.functionReturns[0] = minimiseFunctionOutput
                self.numSuccess = 1

        if self.numSuccess >= self.basinRequiredSuccess:
            return True
