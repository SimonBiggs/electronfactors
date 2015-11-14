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

from bokeh.resources import CDN
from bokeh.embed import components

from bokeh.plotting import show
from bokeh.io import output_file

from .interactive import (
    fallback_scatter, interactive_native_contourf,
    interactive_transformed_contourf, interactive_v2)
from ..model.utilities import pull_data, prediction_uncertainty


# def create_report(energy=None, applicator=None, ssd=None, filepath=None,
#                   inverted_factor=False):
#     width, length, eqPonA, factor, label = pull_data(
#         energy=energy, applicator=applicator, ssd=ssd, return_label=True)
#
#     if inverted_factor:
#         factor = 1/factor
#         tag = "!!INVERTED_FACTOR!!"
#     else:
#         tag = ""
#
#     fig_fallback = fallback_scatter(width, length, factor, label)
#     script_fallback, div_fallback = components(fig_fallback)
#
#     number_of_measurements = len(width)
#     if number_of_measurements < 8:
#         sufficient = False
#     else:
#         sufficient = True
#
#     if filepath is None:
#         filepath = (
#             "interactive_reports/" +
#             str(energy) + "MeV_" +
#             str(applicator) + "app_" +
#             str(ssd) + "ssd_" +
#             str(number_of_measurements) + "datapoints" +
#             tag + ".html")
#
#     if sufficient:
#         fig_native = interactive_native_contourf(width, eqPonA, factor)
#         script_native, div_native = components(fig_native)
#
#         fig_transformed = interactive_transformed_contourf(
#             width, length, factor)
#         script_transformed, div_transformed = components(fig_transformed)
#
#         uncertainty = prediction_uncertainty(width, eqPonA, factor)
#
#     title = (
#         "Electron factors | " + str(energy) + " MeV | " +
#         str(applicator) + " app | " +
#         str(ssd) + " ssd")
#
#     if sufficient:
#         figure_scripts = script_native + script_transformed + script_fallback
#     else:
#         figure_scripts = script_fallback
#
#     script = '''<script type="text/javascript" src="''' + CDN.js_files[0] + '''"></script>
#             ''' + figure_scripts
#
#     stylesheet = (
#         '<link rel="stylesheet" href="' + CDN.css_files[0] +
#         '" type="text/css" />' +
#         '<link rel="stylesheet" ' +
#         'href="https://maxcdn.bootstrapcdn.com/' +
#         'bootstrap/3.3.5/css/bootstrap.min.css">' +
#         '''
#         <style>
#             body {
#                 width: 80%;
#                 margin: 60px auto;
#             }
#         </style>''')
#
#     body = '''<section>
#         <h1>Electron cutout factor spline modelling</h1>
#         </section>
#
#         <section>
#         <h2>Energy: ''' + str(energy) + ''' MeV &emsp;&emsp;
#         Applicator: ''' + str(applicator) + ''' cm &emsp;&emsp;
#         SSD: ''' + str(ssd) + '''</h2>
#         </section>'''
#
#     if sufficient:
#         uncertainty_str = "+/- {0:0.1f}% (1SD)".format(uncertainty)
#         body += '''<section>
#                 Sufficient data is avalaible in this data set therefore
#                 all models are included.
#             </section>
#             <section>
#                 The prediction uncertainty for this model is approximately
#                 ''' + uncertainty_str + '''
#             </section>
#             <section>
#             ''' + div_native + div_transformed + div_fallback + '''
#             </section>'''
#     else:
#         body += '''<section>
#             Insufficient data was available so only the fallback plot was
#             included
#             ''' + div_fallback + '''
#             </section>'''
#
#     html_string = '''<!DOCTYPE html>
#         <html lang="en">
#             <head>
#                 <meta charset="utf-8">
#                 <title>''' + title + '''</title>
#
#                 ''' + script + '''
#                 ''' + stylesheet + '''
#             </head>
#             <body>
#                 ''' + body + '''
#             </body>
#         </html>'''
#
#     f = open(filepath, 'w')
#     f.write(html_string)
#     f.close()


def create_report_v2(input_dict=None, standard_output=True,
                     energy=None, applicator=None, ssd=None, filepath=None,
                     inverted_factor=False):
    if input_dict is None:
        width, length, eqPonA, factor, label = pull_data(
            energy=energy, applicator=applicator, ssd=ssd, return_label=True)
    else:
        width, length, eqPonA, factor, label = pull_data(
            input_dict=input_dict, return_label=True)

    if inverted_factor:
        factor = 1/factor
        tag = "!!INVERTED_FACTOR!!"
    else:
        tag = ""

    number_of_measurements = len(width)
    if number_of_measurements < 8:
        sufficient = False
    else:
        sufficient = True

    if filepath is None:
        filepath = (
            "interactive_reports/" +
            str(energy) + "MeV_" +
            str(applicator) + "app_" +
            str(ssd) + "ssd_" +
            str(number_of_measurements) + "datapoints" +
            tag + ".html")

    if standard_output:
        output_file(filepath)

    if sufficient:
        result = interactive_v2(width, length, eqPonA, factor, label)
        show(result)


create_report = create_report_v2
