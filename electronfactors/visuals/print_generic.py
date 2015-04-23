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


from .print_to_scale import print_to_pdf
from .utilities import make_ellipse


def print_ellipse(width_array,
                  length_array,
                  directory="scale_prints",
                  scale=0.95):

    for i, width in enumerate(width_array):
        length = length_array[i]

        ellipse = make_ellipse(width=width, length=length)

        filename = (
            directory + "/" +
            "ellipse_" +
            str(width) + "x" + str(length) +
            "_scale=" + str(scale) +
            ".pdf")

        print_to_pdf([ellipse], filename, scale=scale)
