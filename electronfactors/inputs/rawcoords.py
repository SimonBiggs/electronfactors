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
import numpy as np
import yaml


def convert_raw(**kwargs):
    XCoordsFilepath = kwargs['XCoords']
    YCoordsFilepath = kwargs['YCoords']
    metadataFilepath = kwargs['metadata']
    outputpath = kwargs['output']

    XCoordsData = pd.read_csv(XCoordsFilepath)
    YCoordsData = pd.read_csv(YCoordsFilepath)
    metadata = pd.read_csv(metadataFilepath)

    data = dict()

    for i, index in enumerate(metadata['index'].values):

        data[index] = dict()

        numCoords = sum(~np.isnan(XCoordsData[index].values))

        XCoords = [0] * numCoords
        YCoords = [0] * numCoords

        for j in range(numCoords):
            XCoords[j] = float(round(XCoordsData[index].values[j], 2))
            YCoords[j] = float(round(YCoordsData[index].values[j], 2))

        data[index]['XCoords'] = XCoords
        data[index]['YCoords'] = YCoords

        data[index]['energy'] = float(metadata['energy'].values[i])
        data[index]['applicator'] = float(metadata['applicator'].values[i])
        data[index]['ssd'] = float(metadata['ssd'].values[i])
        data[index]['factor'] = float(metadata['factor'].values[i])

    with open(outputpath, 'w') as outfile:
        outfile.write(yaml.dump(data, default_flow_style=False))
