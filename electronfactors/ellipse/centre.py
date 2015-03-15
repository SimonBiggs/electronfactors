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

from .sectorintegration import sector_integration
from .utilities import shapely_cutout, shapely_point


class FindCentre(object):

    def __init__(self,
                 n=3,
                 debug=False,
                 confidence=0.0001,
                 sectors=200,
                 **kwargs):

        self.debug = debug
        self.confidence = confidence
        self.sectors = sectors

        self.cutoutXCoords = kwargs['x']
        self.cutoutYCoords = kwargs['y']
        self.cutout = shapely_cutout(self.cutoutXCoords, self.cutoutYCoords)

        self.min_distance = kwargs['min_distance']

        # self.basinNoise = np.hypot(np.diff(self.cutout.bounds[::2]),
        #                            np.diff(self.cutout.bounds[1::2]))/3

        self.basinNoise = 1.5

        self.circle_fit = kwargs['circle_fit']

        self.numCalls = 0
        self.basinRequiredSuccess = n
        self.centre = self._centre_basinhopping()

        point_of_interest = shapely_point(*self.centre)
        is_within = self.cutout.contains(point_of_interest)
        distance = point_of_interest.distance(self.cutout.boundary)

        if not(is_within):
            distance = -distance

        if distance < self.min_distance:
            raise Exception("Centre too closer than min_distance")

    def _minimise_function(self, centre):

        point_of_interest = shapely_point(*centre)
        is_within = self.cutout.contains(point_of_interest)
        distance = point_of_interest.distance(self.cutout.boundary)

        if not(is_within):
            distance = -distance

        if distance >= self.min_distance:
            factor = sector_integration(
                x=self.cutoutXCoords,
                y=self.cutoutYCoords,
                min_distance=self.min_distance,
                circle_fit=self.circle_fit,
                point_of_interest=centre,
                num_rays=self.sectors)
            to_minimise = -factor

        else:
            to_minimise = -(distance - self.min_distance)

        self.numCalls += 1

        return to_minimise

    def _centre_basinhopping(self):

        self.functionReturns = np.empty(self.basinRequiredSuccess)
        self.functionReturns[:] = np.nan

        self.numSuccess = 0

        minimizerConfig = {"method": 'BFGS',
                           "options": {'gtol': self.confidence}}

        initial_input = np.array([0, 0])

        basinhoppingOutput = basinhopping(self._minimise_function,
                                          initial_input,
                                          niter=1000,
                                          minimizer_kwargs=minimizerConfig,
                                          take_step=self._step_function,
                                          callback=self._callback_function)

        return basinhoppingOutput.x

    def _step_function(self, optimiserInput):

        optimiserInput[0] += np.random.normal(scale=self.basinNoise)
        optimiserInput[1] += np.random.normal(scale=self.basinNoise)

        return optimiserInput

    def _callback_function(self,
                           optimiserOutput,
                           minimiseFunctionOutput,
                           minimiseAccepted):
        """Callback function used by self.ellipse_basinhopping.
        """

        if minimiseAccepted:

            if self.numSuccess == 0:
                # First result
                self.functionReturns[0] = minimiseFunctionOutput
                self.numSuccess = 1

            elif (minimiseFunctionOutput >=
                  np.nanmin(self.functionReturns) + self.confidence):
                # Reject result
                0

            elif (minimiseFunctionOutput >=
                  np.nanmin(self.functionReturns) - self.confidence):
                # Agreeing result
                self.functionReturns[self.numSuccess] = minimiseFunctionOutput
                self.numSuccess += 1

            elif (minimiseFunctionOutput <
                  np.nanmin(self.functionReturns) - self.confidence):
                # New result
                self.functionReturns[0] = minimiseFunctionOutput
                self.numSuccess = 1

        if self.debug:
            self.debug_print(optimiserOutput, minimiseFunctionOutput)

        if self.numSuccess >= self.basinRequiredSuccess:
            return True

    def debug_print(self, optimiserOutput, minimiseFunctionOutput):
        point_of_interest = shapely_point(*optimiserOutput)
        is_within = self.cutout.contains(point_of_interest)
        distance = point_of_interest.distance(self.cutout.boundary)

        if not(is_within):
            distance = -distance

        try:
            factor = sector_integration(
                x=self.cutoutXCoords,
                y=self.cutoutYCoords,
                min_distance=1.5,
                circle_fit=self.circle_fit,
                point_of_interest=optimiserOutput,
                num_rays=self.sectors)
        except:
            factor = 0

        print("Successes: %d" % (self.numSuccess))
        print("Coords: (%f, %f)" % (
            optimiserOutput[0], optimiserOutput[1]))
        print("Minimise Function: %f" % (minimiseFunctionOutput))
        print("Distance: %f" % (distance))
        print("Factor: %f" % (factor))
        print(" ")
