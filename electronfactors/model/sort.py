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
import numpy as np


def cache_all():
    input_filepath = "imported_data/parameterised.yml"
    with open(input_filepath, 'r') as file:
        input_dict = yaml.load(file)

    energy = []
    applicator = []
    ssd = []

    for i, key in enumerate(input_dict):
        energy.append(input_dict[key]['energy'])
        applicator.append(input_dict[key]['applicator'])
        ssd.append(input_dict[key]['ssd'])

    energy_array = np.unique(energy).astype(int)
    applicator_array = np.unique(applicator).astype(int)
    ssd_array = np.unique(ssd).astype(int)

    for energy in energy_array:
        for applicator in applicator_array:
            for ssd in ssd_array:
                create_cache(energy=energy, applicator=applicator, ssd=ssd)


def create_cache(input_directory="imported_data/",
                 output_directory="model_cache/",
                 ssd=100, **kwargs):

    input_filepath = input_directory + "parameterised.yml"
    energy = kwargs['energy']
    applicator = kwargs['applicator']

    filepath = (
        output_directory +
        str(energy) + "MeV_" +
        str(applicator) + "app_" +
        str(ssd) + "ssd.yml")

    with open(input_filepath, 'r') as file:
        input_dict = yaml.load(file)

    output_dict = dict()

    for i, key in enumerate(input_dict):
        sameenergy = input_dict[key]['energy'] == energy
        sameapplicator = input_dict[key]['applicator'] == applicator
        samessd = input_dict[key]['ssd'] == ssd

        if sameenergy and sameapplicator and samessd:
            output_dict[key] = input_dict[key]

    number_of_points = len(output_dict.keys())

    with open(filepath, 'w') as file:
        file.write(yaml.dump(output_dict, default_flow_style=False))
    print(
        "Cache created\n"
        "Number of measurements = %d\n"
        "Energy = %d\n"
        "Applicator = %d"
        "\nSSD = %d\n" %
        (number_of_points, energy, applicator, ssd))
