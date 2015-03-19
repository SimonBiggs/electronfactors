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


def create_cache(ssd=100, **kwargs):

    input_filepath = "imported_data/guessed.yml"
    energy = kwargs['energy']
    applicator = kwargs['applicator']

    output_filepath = (
        "model_cache/" +
        str(energy) + "MeV_" +
        str(applicator) + "app_" +
        str(ssd) + "ssd.yml"
    )

    with open(input_filepath, 'r') as inputFile:
        input_dict = yaml.load(inputFile)

    output_dict = dict()

    for i, key in enumerate(input_dict):
        sameenergy = input_dict[key]['energy'] == energy
        sameapplicator = input_dict[key]['applicator'] == applicator
        samessd = input_dict[key]['ssd'] == ssd

        if sameenergy and sameapplicator and samessd:
            output_dict[key] = input_dict[key]

    with open(output_filepath, 'w') as outfile:
        outfile.write(yaml.dump(output_dict, default_flow_style=False))
