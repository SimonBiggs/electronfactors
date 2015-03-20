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


# Make this function later when I have a better idea how it is needed.

import yaml

from .genericshape import convert_generic
from .rawcoords import convert_raw

from electronfactors.ellipse.fitting import StandardFitEllipse


# For each input method, also make a "finder function"
# This finder function can be used to find the regex the input files
# That way, simply call all finder functions in existance and for those files
# found import the data :)
def convert(input_directory="user_inputs/",
            output_directory="imported_data/"):

    XCoords_filepath = input_directory + "RawCoordsImport_XCoords.csv"
    YCoords_filepath = input_directory + "RawCoordsImport_YCoords.csv"
    metadata_filepath = input_directory + "RawCoordsImport_metadata.csv"

    output_filepath = output_directory + "RawCoords_coords.yml"

    convert_raw(
        XCoordsFilepath=XCoords_filepath,
        YCoordsFilepath=YCoords_filepath,
        metadataFilepath=metadata_filepath,
        outputFilepath=output_filepath)

    input_filepath = input_directory + "GenericShapeImport.csv"
    output_filepath = output_directory + "GenericShape_coords.yml"

    convert_generic(
        inputFilepath=input_filepath,
        outputFilepath=output_filepath)


def merge(working_directory="imported_data/"):
    input_paths = [
        working_directory + "RawCoords_coords.yml",
        working_directory + "GenericShape_coords.yml"
    ]
    output_filepath = working_directory + "merged.yml"

    merged_dict = dict()

    for path in input_paths:
        with open(path, 'r') as inputFile:
            merged_dict.update(yaml.load(inputFile))

    with open(output_filepath, 'w') as outfile:
        outfile.write(yaml.dump(merged_dict, default_flow_style=False))


def guess(working_directory="imported_data/"):
    input_filepath = working_directory + "merged.yml"
    output_filepath = working_directory + "guessed.yml"

    with open(input_filepath, 'r') as inputFile:
        input_dict = yaml.load(inputFile)

    output_dict = input_dict.copy()

    for i, key in enumerate(input_dict):
        XCoords = input_dict[key]['XCoords']
        YCoords = input_dict[key]['YCoords']

        ellipse_fit = StandardFitEllipse(x=XCoords, y=YCoords, n=2)

        output_dict[key]['width'] = ellipse_fit.width
        output_dict[key]['length'] = ellipse_fit.length

    with open(output_filepath, 'w') as outfile:
        outfile.write(yaml.dump(output_dict, default_flow_style=False))


def convert_merge_guess(input_directory="user_inputs/",
                        output_directory="imported_data/"):
    convert(input_directory=input_directory, output_directory=output_directory)
    merge(working_directory=output_directory)
    guess(working_directory=output_directory)
