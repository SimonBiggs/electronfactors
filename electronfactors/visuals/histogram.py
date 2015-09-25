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
import matplotlib.pyplot as plt

from .utilities import create_green_cm

green_cm = create_green_cm()


def colour(x, alpha=1):
    result = list(green_cm(x))
    result[3] = alpha

    return result


def create_histogram(differences,
                     bins=np.arange(-1.0, 4/3, 1/3)):
    plt.figure(figsize=(6 * 1.618, 6))

    dbins = bins[1] - bins[0]
    binsTrans = bins - dbins/2

    binsTrans = binsTrans.reshape(-1, 1)
    binNum = np.argmin(abs(binsTrans - differences), 0)

    representative_height = np.zeros(len(binNum))

    for i in range(len(bins)):
        binRef = (binNum == i)
        representative_height[binRef] = np.arange(sum(binRef)) + 1

    plt.hist(
        differences, bins,
        fc=colour(0.6), lw=1)
    plt.scatter(
        differences,
        representative_height, zorder=2,
        s=200, lw=1, c=colour(0.4))

    return representative_height
