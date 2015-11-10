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


import pandas as pd
import shapely.geometry as geo
import shapely.affinity as aff
import yaml


def ellipse(width, length):
    """Create ellipse when given width and length.
    """
    circle = geo.Point(0, 0).buffer(1)
    stretched = aff.scale(circle, xfact=width/2, yfact=length/2)
    rotated = aff.rotate(stretched, -45)

    return rotated


def rectangle(width, length):
    """Create rectangle when given width and length.
    """
    rectangle = geo.box(-width/2, -length/2, width/2, length/2)

    return rectangle


def generic_shape_convert(width, length, shape):

    shape = shape.lower()

    if (shape == 'oval') | (shape == 'circle') | (shape == 'ellipse'):
        XCoords, YCoords = ellipse(width, length).exterior.xy

    elif (shape == 'square') | (shape == 'rectangle'):
        XCoords, YCoords = rectangle(width, length).exterior.xy

    else:
        raise Exception("Unexpected shape")

    return XCoords, YCoords


# def file_finder()

def convert_generic(**kwargs):
    inputpath = kwargs['inputFilepath']
    outputpath = kwargs['outputFilepath']

    input_data = pd.read_csv(inputpath)

    width = input_data['width'].values
    length = input_data['length'].values
    shape = input_data['shape'].values

    data = dict()

    for i, index in enumerate(input_data['index'].values):

        data[index] = dict()

        XCoords, YCoords = generic_shape_convert(width[i], length[i], shape[i])

        XCoords = [float(round(item, 2)) for item in XCoords]
        YCoords = [float(round(item, 2)) for item in YCoords]

        data[index]['XCoords'] = XCoords
        data[index]['YCoords'] = YCoords

        data[index]['energy'] = float(input_data['energy'].values[i])
        data[index]['applicator'] = float(input_data['applicator'].values[i])
        data[index]['ssd'] = float(input_data['ssd'].values[i])
        data[index]['factor'] = float(round(input_data['factor'].values[i], 4))

    with open(outputpath, 'w') as outfile:
        outfile.write(yaml.dump(data))
