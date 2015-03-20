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

# Move the current import files into a folder called "example inputs"
# Call from these in a nose_test.py


import numpy as np
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

    genericShapeData = pd.read_csv(inputpath)

    width = genericShapeData['width'].values
    length = genericShapeData['length'].values
    shape = genericShapeData['shape'].values

    data = dict()

    for i, index in enumerate(genericShapeData['index'].values):

        data[index] = dict()

        XCoords, YCoords = generic_shape_convert(width[i], length[i], shape[i])

        XCoords = [round(item, 2) for item in XCoords]
        YCoords = [round(item, 2) for item in YCoords]

        data[index]['XCoords'] = list(XCoords)
        data[index]['YCoords'] = list(YCoords)

        data[index]['energy'] = float(genericShapeData['energy'].values[i])
        data[index]['applicator'] = float(
            genericShapeData['applicator'].values[i])
        data[index]['ssd'] = float(genericShapeData['ssd'].values[i])
        data[index]['factor'] = float(genericShapeData['factor'].values[i])

        if isinstance(genericShapeData['poi'][i], str):
            poi = [
                float(
                    genericShapeData['poi'][i].split(',')[j]
                ) for j in range(2)
            ]
            data[index]['poi'] = poi
        else:
            data[index]['poi'] = None

    with open(outputpath, 'w') as outfile:
        outfile.write(yaml.dump(data, default_flow_style=False))
