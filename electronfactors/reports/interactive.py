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
from bokeh.models import (
    HoverTool, ColumnDataSource, Rect, Range1d, CrosshairTool)
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.plotting import figure, gridplot
from bokeh.io import vplot

from matplotlib import colors

from ..model.threshold import fit_give
from ..model.utilities import (
    create_model, to_eqPonA, to_length,
    calculate_percent_prediction_differences)
from ..visuals.utilities import create_green_cm


green_cm = create_green_cm()
default_tools = "hover, box_zoom, reset"


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
        (give_contour > 0.5) |
        (np.around(yy, decimals=2) > np.around(maximum_eqPonA, decimals=2)) |
        (np.around(yy, decimals=2) < np.around(minimum_rqPonA, decimals=2)))

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

    fig = bokeh_contourf(xx, yy, zz, hover_labels, hover_values)

    fig.title = "Native domain"
    fig.xaxis.axis_label = "Width (cm)"
    fig.yaxis.axis_label = "Perimeter / Area (cm^-1)"

    return fig


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
        (
            np.around(mesh_width, decimals=1) >
            np.around(mesh_length, decimals=1)) |
        (
            np.around(mesh_length, decimals=1) >
            np.around(mesh_max_length, decimals=1)))

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

    fig = bokeh_contourf(
        xx, yy, zz, hover_labels, hover_values)

    fig.title = "Transformed domain"
    fig.xaxis.axis_label = "Width (cm)"
    fig.yaxis.axis_label = "Length (cm)"

    return fig


def fallback_scatter(width, length, factor, label):
    hover_width = [" %0.1f cm" % (num) for num in width]
    hover_length = [" %0.1f cm" % (num) for num in length]
    hover_factor = [" %0.3f" % (num) for num in factor]

    hover_labels = ["Label", "Width", "Length", "Factor"]
    hover_values = [label, hover_width, hover_length, hover_factor]

    fig = bokeh_scatter(width, factor, hover_labels, hover_values)

    fig.title = "Fallback scatter plot"
    fig.xaxis.axis_label = "Width (cm)"
    fig.yaxis.axis_label = "Factor"

    return fig


def bokeh_scatter(x, y, hover_labels, hover_values):
    fig = bkh.figure(
        tools=default_tools,
        plot_height=400, plot_width=600)

    source = convert_to_source(hover_labels, hover_values)
    tooltips = convert_to_tooltips(hover_labels, hover_values)

    fig.scatter(x, y, source=source, size=10)
    hover = fig.select(dict(type=HoverTool))
    hover.tooltips = tooltips

    return fig


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


def bokeh_contourf(xx, yy, zz, hover_labels, hover_values):
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
        tools=default_tools,
        plot_height=400, plot_width=600)

    source = convert_to_source(hover_labels, hover_values)
    tooltips = convert_to_tooltips(hover_labels, hover_values)

    fig.rect(xx_flat, yy_flat, dx, dy, color=color, source=source)
    hover = fig.select(dict(type=HoverTool))
    hover.tooltips = tooltips

    return fig


def find_colour(factor, vmin, vmax):
    colour_reference = (factor - vmin) / (vmax - vmin)
    rgb = green_cm(colour_reference)
    rgb = rgb[:, 0:3]
    colour = [colors.rgb2hex(tuple(item)) for item in rgb]

    return colour


def interactive_v2(width, length, eqPonA, factor, label):
    model = create_model(width, eqPonA, factor)
    model_value = model(width, eqPonA)
    pred_diff = calculate_percent_prediction_differences(
        width, eqPonA, factor, keep_nans=True)
    pc_residual = 100 * (factor - model_value) / factor

    transformed_mesh = dict()
    result = create_transformed_plot_mesh(width, length, factor)
    reference = ~np.isnan(np.ravel(result[2]))
    transformed_mesh['width'] = np.ravel(result[0])[reference]
    transformed_mesh['length'] = np.ravel(result[1])[reference]
    transformed_mesh['factor'] = np.ravel(result[2])[reference]
    transformed_mesh['eqPonA'] = to_eqPonA(
        transformed_mesh['width'], transformed_mesh['length'])

    native_mesh = dict()
    result = create_native_plot_mesh(width, eqPonA, factor)
    reference = ~np.isnan(np.ravel(result[2]))
    native_mesh['width'] = np.ravel(result[0])[reference]
    native_mesh['eqPonA'] = np.ravel(result[1])[reference]
    native_mesh['factor'] = np.ravel(result[2])[reference]
    native_mesh['length'] = to_length(
        native_mesh['width'], native_mesh['eqPonA'])

    all_factor = np.hstack([
        transformed_mesh['factor'], native_mesh['factor'], factor])
    vmin = np.nanmin(all_factor)
    vmax = np.nanmax(all_factor)

    colour = find_colour(factor, vmin, vmax)

    measurement_data = dict(
        width=width,
        length=length,
        eqPonA=np.around(eqPonA, decimals=3),
        factor=np.around(factor, decimals=3),
        model_value=np.around(model_value, decimals=3),
        pc_residual=np.around(pc_residual, decimals=1),
        pred_diff=np.around(pred_diff, decimals=1),
        colour=colour,
        label=label,
        zeros=np.zeros(len(factor))
    )

    measurements_source = ColumnDataSource(measurement_data)

    transformed_hover_width = [
        " %0.1f cm" % (num) for num in transformed_mesh['width']]
    transformed_hover_length = [
        " %0.1f cm" % (num) for num in transformed_mesh['length']]
    transformed_hover_eqPonA = [
        " %0.2f cm^-1" % (num) for num in transformed_mesh['eqPonA']]
    transformed_hover_factor = [
        " %0.3f" % (num) for num in transformed_mesh['factor']]

    transformed_data = dict(
        width=transformed_mesh['width'],
        length=transformed_mesh['length'],
        eqPonA=transformed_mesh['eqPonA'],
        factor=transformed_mesh['factor'],
        zeros=np.zeros(len(transformed_mesh['factor'])),
        colour=find_colour(transformed_mesh['factor'], vmin, vmax),
        hover_width=transformed_hover_width,
        hover_length=transformed_hover_length,
        hover_eqPonA=transformed_hover_eqPonA,
        hover_factor=transformed_hover_factor
    )

    transformed_source = ColumnDataSource(transformed_data)

    native_hover_width = [
        " %0.1f cm" % (num) for num in native_mesh['width']]
    native_hover_length = [
        " %0.1f cm" % (num) for num in native_mesh['length']]
    native_hover_eqPonA = [
        " %0.2f cm^-1" % (num) for num in native_mesh['eqPonA']]
    native_hover_factor = [
        " %0.3f" % (num) for num in native_mesh['factor']]

    native_data = dict(
        width=native_mesh['width'],
        length=native_mesh['length'],
        eqPonA=native_mesh['eqPonA'],
        factor=native_mesh['factor'],
        zeros=np.zeros(len(native_mesh['factor'])),
        colour=find_colour(native_mesh['factor'], vmin, vmax),
        hover_width=native_hover_width,
        hover_length=native_hover_length,
        hover_eqPonA=native_hover_eqPonA,
        hover_factor=native_hover_factor
    )

    native_source = ColumnDataSource(native_data)

    columns = [
        TableColumn(field="label", title="Label"),
        TableColumn(field="width", title="Width (cm)"),
        TableColumn(field="length", title="Length (cm)"),
        TableColumn(field="eqPonA", title="P/A (cm^-1)"),
        TableColumn(field="factor", title="Cutout factor"),
        TableColumn(field="model_value", title="Model factor"),
        TableColumn(field="pc_residual", title="Residual (%)"),
        TableColumn(field="pred_diff", title="Prediction Diff. (%)"),
    ]

    data_table = DataTable(
        source=measurements_source, columns=columns, width=1000, height=500)

    tools = "box_select, tap, crosshair"
    unselect_rectangle = Rect(line_alpha=0, fill_alpha=0)

    native_y_range = Range1d(
        native_data['eqPonA'].min() - 0.005 - native_data['eqPonA'].ptp()*0.03,
        native_data['eqPonA'].max() + 0.005 + native_data['eqPonA'].ptp()*0.03)
    native_x_range = Range1d(
        native_data['width'].min() - 0.05 - native_data['width'].ptp()*0.03,
        native_data['width'].max() + 0.05 + native_data['width'].ptp()*0.03)

    native = figure(
        tools=tools, width=450, height=350,
        title="Native domain",
        x_axis_label="Width (cm)", y_axis_label="Perimeter / Area cm^-1)",
        x_range=native_x_range, y_range=native_y_range)
    native.rect(
        'width', 'eqPonA', 0.1, 0.01, alpha=0, source=transformed_source,
        name='native_invis')
    native.rect(
        'width', 'eqPonA', 0.1, 0.01, color='colour', source=native_source,
        name='native_visible')
    native.circle(
        'width', 'eqPonA', source=measurements_source,
        size=10, fill_color='colour', line_color='black')
    render_invis = native.select(name='native_invis')
    render_invis.nonselection_glyph = unselect_rectangle
    render_vis = native.select(name='native_visible')
    render_vis.nonselection_glyph = unselect_rectangle

    tooltips = [
        ("Width", "@hover_width"),
        ("Length", "@hover_length"),
        ("P/A", "@hover_eqPonA"),
        ("Factor", "@hover_factor"),
    ]
    native.add_tools(HoverTool(
            tooltips=tooltips,
            renderers=render_vis))

    trans_y_range = Range1d(
        transformed_data['length'].min() - 0.05 -
        transformed_data['length'].ptp()*0.03,
        transformed_data['length'].max() + 0.05)
    trans_x_range = Range1d(
        transformed_data['width'].min() - 0.05 -
        transformed_data['width'].ptp()*0.03,
        transformed_data['width'].max() + 0.05 +
        transformed_data['width'].ptp()*0.03)

    transformed = figure(
        tools=tools, width=450, height=350,
        title="Transformed domain",
        x_axis_label="Width (cm)", y_axis_label="Length (cm)",
        x_range=trans_x_range, y_range=trans_y_range)
    transformed.rect(
        'width', 'length', 0.1, 0.1, alpha=0, source=native_source,
        name='trans_invis')
    transformed.rect(
        'width', 'length', 0.1, 0.1, color='colour', source=transformed_source,
        name='trans_visible')
    transformed.circle(
        'width', 'length', source=measurements_source,
        size=10, fill_color='colour', line_color='black')
    render_invis = transformed.select(name='trans_invis')
    render_invis.nonselection_glyph = unselect_rectangle
    render_vis = transformed.select(name='trans_visible')
    render_vis.nonselection_glyph = unselect_rectangle

    tooltips = [
        ("Width", "@hover_width"),
        ("Length", "@hover_length"),
        ("P/A", "@hover_eqPonA"),
        ("Factor", "@hover_factor"),
    ]
    transformed.add_tools(HoverTool(
            tooltips=tooltips,
            renderers=render_vis))

    mesh_factors = np.hstack(
        [transformed_mesh['factor'], native_mesh['factor']])
    colour_bar_range = Range1d(
        np.floor(100*mesh_factors.min())/100,
        np.ceil(100*mesh_factors.max())/100)

    colour_bar = figure(
        tools=tools, width=135, height=350, title=None,
        y_range=colour_bar_range,
        y_axis_label="Factor")
    colour_bar.rect(
        'zeros', 'factor', 0.5, 0.0005, name='colour_bar_trans',
        source=transformed_source, color='colour')
    render = colour_bar.select(name='colour_bar_trans')
    render.nonselection_glyph = unselect_rectangle
    colour_bar.rect(
        'zeros', 'factor', 0.5, 0.0005, name='colour_bar_native',
        source=native_source, color='colour')
    render = colour_bar.select(name='colour_bar_native')
    render.nonselection_glyph = unselect_rectangle
    colour_bar.rect(
        'zeros', 'factor', 0.5, 0.0005, name='colour_bar_meas',
        source=measurements_source, alpha=0)
    render = colour_bar.select(name='colour_bar_meas')
    render.nonselection_glyph = unselect_rectangle

    crosshair = colour_bar.select(type=CrosshairTool)
    crosshair.dimensions = ['width']

    colour_bar.xgrid.grid_line_color = None
    colour_bar.ygrid.grid_line_color = None
    colour_bar.xaxis.major_label_text_font_size = '0pt'
    colour_bar.xaxis.major_tick_line_color = None
    colour_bar.xaxis.minor_tick_line_color = None

    p = gridplot([[colour_bar, native, transformed]], toolbar_location=None)
    output = vplot(p, data_table)
    return output
