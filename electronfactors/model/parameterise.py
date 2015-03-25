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

import yaml

from ..ellipse.equivalent import equivalent_ellipse


def parameterise(display=False, working_directory="imported_data/", **kwargs):

    input_filepath = working_directory + "merged.yml"
    output_filepath = working_directory + "parameterised.yml"

    with open(input_filepath, 'r') as file:
        input_dict = yaml.load(file)

    output_dict = input_dict.copy()
    for i, key in enumerate(input_dict):
        XCoords = input_dict[key]['XCoords']
        YCoords = input_dict[key]['YCoords']

        if display:
            print(str(key) + ":")

        ellipse = equivalent_ellipse(
            XCoords=XCoords, YCoords=YCoords, display=display)

        width = float(round(ellipse['width'], 2))
        length = float(round(ellipse['length'], 2))
        poi = [float(round(item, 2)) for item in ellipse['poi']]

        output_dict[key]['width'] = width
        output_dict[key]['length'] = length
        output_dict[key]['poi'] = poi

    with open(output_filepath, 'w') as file:
        file.write(yaml.dump(output_dict, default_flow_style=False))
