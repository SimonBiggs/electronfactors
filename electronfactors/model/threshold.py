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
from scipy.interpolate import SmoothBivariateSpline


def single_angle_gap(xTest, yTest, xData, yData, xScale, yScale):

    xi = xScale * (xData - xData.min()) / xData.ptp()
    yi = yScale * (yData - yData.min()) / yData.ptp()

    xVal = xScale * (xTest - xData.min()) / xData.ptp()
    yVal = yScale * (yTest - yData.min()) / yData.ptp()

    dx = xi - xVal
    dy = yi - yVal

    same_position = (dx == 0) & (dy == 0)
    dx = dx[~same_position]
    dy = dy[~same_position]

    theta = np.arctan(dy/dx)
    theta[dx < 0] = theta[dx < 0] + np.pi
    theta[(dx > 0) & (dy < 0)] = theta[(dx > 0) & (dy < 0)] + 2*np.pi
    theta[(dx == 0) & (dy > 0)] = np.pi/2
    theta[(dx == 0) & (dy < 0)] = 3*np.pi/2

    test = np.sort(theta)
    test = np.append(test, test[0] + 2*np.pi)
    gap = np.max(np.diff(test))*180/np.pi

    return gap


def angle_gap(xTest, yTest, xData, yData, xScale, yScale):

    dim = np.core.fromnumeric.shape(xTest)

    if np.size(dim) == 0:
        gap = single_angle_gap(xTest, yTest, xData, yData, xScale, yScale)

        return gap

    gap = np.zeros(dim)

    if np.size(dim) == 1:
        for i in range(dim[0]):
            gap[i] = single_angle_gap(
                xTest[i], yTest[i], xData, yData, xScale, yScale)

        return gap

    for i in range(dim[0]):
        for j in range(dim[1]):
            gap[i, j] = single_angle_gap(
                xTest[i, j], yTest[i, j], xData, yData, xScale, yScale)

    return gap


def single_fit_give(xTest, yTest, xData, yData, zData,
                    s=None, kx=2, ky=1, deviation=0.02):

    adjXData = np.append(xData, xTest)
    adjYData = np.append(yData, yTest)

    bbox = [
        min(adjXData), max(adjXData),
        min(adjYData), max(adjYData)]

    initialFitReturn = SmoothBivariateSpline(
        xData, yData, zData, bbox=bbox, kx=kx, ky=ky, s=s).ev(xTest, yTest)

    posAdjZData = np.append(zData, initialFitReturn + deviation)
    negAdjZData = np.append(zData, initialFitReturn - deviation)

    posFitReturn = SmoothBivariateSpline(
        adjXData, adjYData, posAdjZData, kx=kx, ky=ky, s=s).ev(xTest, yTest)
    negFitReturn = SmoothBivariateSpline(
        adjXData, adjYData, negAdjZData, kx=kx, ky=ky, s=s).ev(xTest, yTest)

    posGive = (posFitReturn - initialFitReturn) / deviation
    negGive = (initialFitReturn - negFitReturn) / deviation

    give = np.mean([posGive, negGive])

    return give


def fit_give(xTest, yTest, xData, yData, zData,
             s=None, kx=2, ky=1, deviation=0.02):

    dim = np.core.fromnumeric.shape(xTest)

    if np.size(dim) == 0:
        give = single_fit_give(
            xTest, yTest, xData, yData, zData, s=s, kx=kx, ky=ky,
            deviation=deviation)

        return give

    give = np.zeros(dim)

    if np.size(dim) == 1:
        for i in range(dim[0]):
            give[i] = single_fit_give(
                xTest[i], yTest[i], xData, yData, zData, s=s, kx=kx, ky=ky,
                deviation=deviation)

        return give

    for i in range(dim[0]):
        for j in range(dim[1]):
            give[i, j] = single_fit_give(
                xTest[i, j], yTest[i, j],
                xData, yData, zData,
                s=s, kx=kx, ky=ky,
                deviation=deviation)

    return give
