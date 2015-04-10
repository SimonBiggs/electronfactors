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
from matplotlib import pylab
import descartes as des

import subprocess
import os


def print_to_pdf(shapley_list, filename):

    pylab.rcParams['savefig.dpi'] = 254 * 0.95

    x_min = []
    x_max = []
    y_min = []
    y_max = []

    for shape in shapley_list:
        bound = shape.bounds
        x_min.append(bound[0])
        y_min.append(bound[1])
        x_max.append(bound[2])
        y_max.append(bound[3])

    x_limits = [np.min(x_min), np.max(x_max)]
    y_limits = [np.min(y_min), np.max(y_max)]

    fig_width = np.ptp(x_limits)
    fig_height = np.ptp(y_limits)

    fig = plt.figure(figsize=(fig_width/2.54, fig_height/2.54))
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax = fig.add_subplot(111)

    for shape in shapley_list:
        patch = des.PolygonPatch(
            shape, fc=np.random.uniform(size=3), alpha=0.5
        )
        ax.add_patch(patch)

    ax.set_xlim(x_limits)
    ax.set_ylim(y_limits)

    plt.grid(True)

    plt.savefig("temp.png")
    subprocess.call([
        "convert", "-units", "PixelsPerInch",
        "temp.png", "-density", "254", "temp.pdf"
    ])
    os.rename("temp.pdf", filename)
    os.remove("temp.png")
