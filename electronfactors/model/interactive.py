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

import bokeh.plotting as bkh
from bokeh.models import HoverTool

from matplotlib import colors

from .threshold import fit_give
from .utilities import create_model, to_eqPonA, to_length
from ..visuals.utilities import create_green_cm


green_cm = create_green_cm()


def create_native_plot_mesh(width, eqPonA, factor):
    model = create_model(width, eqPonA, factor)

    x = np.arange(np.floor(np.min(width)) - 1, np.ceil(np.max(width)), 0.1)
    y = np.arange(
        np.floor(np.min(eqPonA)*10)/10 - 0.2,
        np.ceil(np.max(eqPonA)*10)/10 + 0.1, 0.01)

    xx, yy = np.meshgrid(x, y)

    zz = model(xx, yy)
    give_contour = fit_give(xx, yy, width, eqPonA, factor, kx=2, ky=1)

    maximum_eqPonA = to_eqPonA(xx, xx)

    mesh_max_area = ((10 * np.sqrt(2) - xx) * xx + (xx/np.sqrt(2))**2)
    mesh_max_length = 4 * mesh_max_area / (np.pi * xx)

    minimum_rqPonA = to_eqPonA(xx, mesh_max_length)

    outOfTolerance = (
        (give_contour > 0.5) | (yy > maximum_eqPonA) | (yy < minimum_rqPonA))

    zz[outOfTolerance] = np.nan

    return xx, yy, zz


def interactive_native_contourf(width, eqPonA, factor):
    xx, yy, zz = create_native_plot_mesh(width, eqPonA, factor)

    xx_flat = np.ravel(xx)
    yy_flat = np.ravel(yy)
    zz_flat = np.ravel(zz)

    reference = ~np.isnan(zz_flat)
    xx_flat = xx_flat[reference]
    yy_flat = yy_flat[reference]
    zz_flat = zz_flat[reference]

    length_calc = to_length(xx_flat, yy_flat)

    hover_width = [" %0.1f cm" % (num) for num in xx_flat]
    hover_length = [" %0.1f cm" % (num) for num in length_calc]
    hover_eqPonA = [" %0.2f cm^-1" % (num) for num in yy_flat]
    hover_factor = [" %0.3f" % (num) for num in zz_flat]

    hover_labels = ["Width", "Length", "PonA", "Factor"]
    hover_values = [hover_width, hover_length, hover_eqPonA, hover_factor]

    bokeh_contourf(xx, yy, zz, hover_labels, hover_values, "Native domain")


def create_transformed_plot_mesh(width, length, factor):
    eqPonA = to_eqPonA(width, length)
    model = create_model(width, eqPonA, factor)

    x = np.arange(np.floor(np.min(width)) - 1, np.ceil(np.max(width)), 0.1)
    y = np.arange(np.floor(np.min(length)) - 1, np.ceil(np.max(length)), 0.1)

    mesh_width, mesh_length = np.meshgrid(x, y)
    mesh_eqPonA = to_eqPonA(mesh_width, mesh_length)

    width_length_zz = model(mesh_width, mesh_eqPonA)
    give = fit_give(mesh_width, mesh_eqPonA, width, eqPonA, factor, kx=2, ky=1)

    mesh_max_area = (
        (10 * np.sqrt(2) - mesh_width) *
        mesh_width + (mesh_width/np.sqrt(2))**2)

    mesh_max_length = 4 * mesh_max_area / (np.pi * mesh_width)

    outOfTolerance = (
        (give > 0.5) |
        (mesh_width > mesh_length) |
        (mesh_length > mesh_max_length))

    width_length_zz[outOfTolerance] = np.nan

    return mesh_width, mesh_length, width_length_zz


def interactive_transformed_contourf(width, length, factor):
    xx, yy, zz = create_transformed_plot_mesh(width, length, factor)

    xx_flat = np.ravel(xx)
    yy_flat = np.ravel(yy)
    zz_flat = np.ravel(zz)

    reference = ~np.isnan(zz_flat)
    xx_flat = xx_flat[reference]
    yy_flat = yy_flat[reference]
    zz_flat = zz_flat[reference]

    eqPonA_calc = to_eqPonA(xx_flat, yy_flat)

    hover_width = [" %0.1f cm" % (num) for num in xx_flat]
    hover_length = [" %0.1f cm" % (num) for num in yy_flat]
    hover_eqPonA = [" %0.2f cm^-1" % (num) for num in eqPonA_calc]
    hover_factor = [" %0.3f" % (num) for num in zz_flat]

    hover_labels = ["Width", "Length", "PonA", "Factor"]
    hover_values = [hover_width, hover_length, hover_eqPonA, hover_factor]

    bokeh_contourf(
        xx, yy, zz, hover_labels, hover_values, "Transformed domain")


def convert_to_source(hover_labels, hover_values):
    data = dict()
    for i in range(len(hover_labels)):
        data[hover_labels[i]] = hover_values[i]

    source = bkh.ColumnDataSource(
        data=data)

    return source


def convert_to_tooltips(hover_labels, hover_values):
    tooltips = [(label, " @" + label) for label in hover_labels]
    return tooltips


def bokeh_contourf(xx, yy, zz, hover_labels, hover_values, title):
    dx = xx[0, 1] - xx[0, 0]
    dy = yy[1, 0] - yy[0, 0]

    xx_flat = np.ravel(xx)
    yy_flat = np.ravel(yy)
    zz_flat = np.ravel(zz)

    reference = ~np.isnan(zz_flat)
    xx_flat = xx_flat[reference]
    yy_flat = yy_flat[reference]
    zz_flat = zz_flat[reference]

    colour_reference = (zz_flat - zz_flat.min()) / zz_flat.ptp()
    rgb = green_cm(colour_reference)
    rgb = rgb[:, 0:3]
    color = [colors.rgb2hex(tuple(item)) for item in rgb]

    fig = bkh.figure(
        title=title,
        tools="resize, hover",
        plot_height=400, plot_width=600)

    source = convert_to_source(hover_labels, hover_values)
    tooltips = convert_to_tooltips(hover_labels, hover_values)

    fig.rect(xx_flat, yy_flat, dx, dy, color=color, source=source)
    hover = fig.select(dict(type=HoverTool))
    hover.tooltips = tooltips

    bkh.show(fig)
