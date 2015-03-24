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

from scipy.optimize import basinhopping


def shapely_point(x, y):
    return geo.Point([(x, y)])


def shapely_cutout(XCoords, YCoords):
    """Returns the shapely cutout defined by the x and y coordinates.
    """
    return geo.Polygon(np.transpose((XCoords, YCoords)))


def shapely_ellipse(ellipseRaw):
    """Given raw ellipse values create a shapely ellipse."""
    xPosition = ellipseRaw[0]
    yPosition = ellipseRaw[1]

    width = ellipseRaw[2]
    length = ellipseRaw[3]

    rotation = ellipseRaw[4]

    unitCircle = geo.Point(0, 0).buffer(1)
    stretched = aff.scale(unitCircle, xfact=width/2, yfact=length/2)
    translated = aff.translate(
        stretched,
        xoff=xPosition,
        yoff=yPosition)
    rotated = aff.rotate(translated, rotation)

    ellipse = rotated

    return ellipse


def shapely_circle(radii):
    return geo.Point(0, 0).buffer(radii)


def create_zones(numZones, maxRadii):
    zoneBoundaryRadii = np.linspace(0, maxRadii, numZones + 1)
    zoneBoundaries = [0]*(numZones+1)
    zoneRegions = [0]*numZones
    zoneMidDist = (zoneBoundaryRadii[0:-1] + zoneBoundaryRadii[1:])/2

    for i in range(numZones + 1):
        zoneBoundaries[i] = geo.Point(0, 0).buffer(zoneBoundaryRadii[i])

    for i in range(numZones):
        zoneRegions[i] = zoneBoundaries[i+1].difference(zoneBoundaries[i])

    return zoneMidDist, zoneRegions


def align(to_be_aligned, alighn_to_this):
    initial = np.array([0])
    step_noise = np.array([90])

    def to_minimise(optimiser_input):
        rotated = aff.rotate(to_be_aligned, optimiser_input[0])

        disjoint_area = (
            rotated.difference(alighn_to_this).area +
            alighn_to_this.difference(rotated).area
        )
        return disjoint_area

    optimiser = _CustomBasinhopping(
        to_minimise=to_minimise,
        initial=initial,
        step_noise=step_noise,
        n=2,
        confidence=0.0001
    )

    rotation_angle = optimiser.result[0]

    return rotation_angle


class _CustomBasinhopping(object):

    def __init__(self, n=5, confidence=0.00001, **kwargs):
        self.to_minimise = kwargs['to_minimise']
        self.n = n
        self.confidence = confidence

        self.initial = kwargs['initial']
        self.step_noise = kwargs['step_noise']

        if len(self.initial) != len(self.step_noise):
            raise Exception(
                "Step noise and initial conditions must be equal length."
            )

        self.result = self.custom_basinhopping()

    def step_function(self, optimiser_input):
        for i, noise in enumerate(self.step_noise):
            optimiser_input[i] += np.random.normal(scale=noise)

        return optimiser_input

    def callback_function(self,
                          optimiser_output,
                          minimise_function_result,
                          was_accepted):
        if not(was_accepted):
            return

        if self.current_success_number == 0:
            # First result
            self.successful_results[0] = minimise_function_result
            self.current_success_number = 1

        elif (minimise_function_result >=
              np.nanmin(self.successful_results) + self.confidence):
            # Reject result
            0

        elif (minimise_function_result >=
              np.nanmin(self.successful_results) - self.confidence):
            # Agreeing result
            self.successful_results[
                self.current_success_number
            ] = minimise_function_result

            self.current_success_number += 1

        elif (minimise_function_result <
              np.nanmin(self.successful_results) - self.confidence):
            # New result
            self.successful_results[0] = minimise_function_result
            self.current_success_number = 1

        if self.current_success_number >= self.n:
            return True

    def custom_basinhopping(self):
        self.successful_results = np.empty(self.n)
        self.successful_results[:] = np.nan
        self.current_success_number = 0

        minimizer_config = {
            "method": 'BFGS',
            "options": {'gtol': self.confidence}
        }

        output = basinhopping(
            self.to_minimise,
            self.initial,
            niter=1000,
            minimizer_kwargs=minimizer_config,
            take_step=self.step_function,
            callback=self.callback_function
        )

        return output.x
