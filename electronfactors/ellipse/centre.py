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
from scipy.optimize import basinhopping

from .sectorintegration import SectorIntegration


def shapely_cutout(XCoords, YCoords):
    """Returns the shapely cutout defined by the x and y coordinates.
    """
    return geo.Polygon(np.transpose((XCoords, YCoords)))


class FindCentre(object):

    def __init__(self,
                 n=5,
                 debug=False,
                 confidence=0.001,
                 sectors=100,
                 ignoreErrors=True,
                 **kwargs):

        self.debug = debug
        self.confidence = confidence
        self.sectors = sectors
        self.ignoreErrors = ignoreErrors

        self.cutoutXCoords = kwargs['x']
        self.cutoutYCoords = kwargs['y']
        self.cutout = shapely_cutout(self.cutoutXCoords, self.cutoutYCoords)

        self.bounds = ((np.min(self.cutoutXCoords),
                        np.max(self.cutoutXCoords)),
                       (np.min(self.cutoutYCoords),
                        np.max(self.cutoutYCoords)))

        self.basinNoise = np.hypot(np.diff(self.cutout.bounds[::2]),
                                   np.diff(self.cutout.bounds[1::2]))/3

        self.circle_fit = kwargs['circle_fit']

        self.numCalls = 0
        self.basinRequiredSuccess = n
        self.centre = self._centre_basinhopping()

    def _minimise_function(self, centre):

        sectorIntegrationInstance = SectorIntegration(
            x=self.cutoutXCoords,
            y=self.cutoutYCoords,
            circle_fit=self.circle_fit,
            centre=centre,
            sectors=self.sectors,
            ignoreErrors=self.ignoreErrors)

        self.numCalls += 1

        return -sectorIntegrationInstance.factor

    def _centre_basinhopping(self):

        self.functionReturns = np.empty(self.basinRequiredSuccess)
        self.functionReturns[:] = np.nan

        self.numSuccess = 0

        minimizerConfig = {"method": 'L-BFGS-B',
                           "options": {'gtol': self.confidence},
                           "bounds": self.bounds}

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

        if self.numSuccess >= self.basinRequiredSuccess:
            return True
