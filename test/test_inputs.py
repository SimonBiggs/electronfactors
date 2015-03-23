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

from electronfactors.inputs.genericshape import convert_generic
from electronfactors.inputs.rawcoords import convert_raw


def test_run_generic():
    convert_generic(
        inputFilepath="examples/user_inputs/GenericShapeImport.csv",
        outputFilepath="examples/imported_data/GenericShape_coords.yml")


def test_run_raw():
    convert_raw(
        XCoordsFilepath="examples/user_inputs/RawCoordsImport_XCoords.csv",
        YCoordsFilepath="examples/user_inputs/RawCoordsImport_YCoords.csv",
        metadataFilepath="examples/user_inputs/RawCoordsImport_metadata.csv",
        outputFilepath="examples/imported_data/RawCoords_coords.yml")
