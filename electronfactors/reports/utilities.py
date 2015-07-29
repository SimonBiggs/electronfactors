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

from glob import glob
import yaml

from .html import create_report


def cache_all():
    index = cache_index()
    energy = index['energy']
    applicator = index['applicator']
    ssd = index['ssd']

    for i in range(len(energy)):
        create_report(
            energy=energy[i],
            applicator=applicator[i],
            ssd=ssd[i])


def cache_index():
    cache_list = glob("model_cache/*")

    energy = []
    applicator = []
    ssd = []
    cachepath = []

    for filepath in cache_list:
        with open(filepath, 'r') as file:
            data = yaml.load(file)

        label = [key for key in data]

        if len(label) > 0:
            energy_array = np.unique([data[key]['energy'] for key in label])
            assert len(energy_array) == 1
            energy.append(int(energy_array[0]))

            applicator_array = np.unique(
                [data[key]['applicator'] for key in label])
            assert len(applicator_array) == 1
            applicator.append(int(applicator_array[0]))

            ssd_array = np.unique([data[key]['ssd'] for key in label])
            assert len(ssd_array) == 1
            ssd.append(int(ssd_array[0]))

            cachepath.append(filepath)

    result = dict(
        energy=energy, applicator=applicator,
        ssd=ssd, cachepath=cachepath)

    return result
