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


from .measurement.utilities import (
    new_reading, calc_and_display, energy_to_reference_depth,
    initialise)

from .ellipse.equivalent import equivalent_ellipse

from .inputs.convert_merge import convert_merge
from .inputs.genericshape import generic_shape_convert

from .model.parameterise import parameterise
from .model.sort import cache_all
from .model.utilities import (
    create_model, pull_data, to_eqPonA, to_length, c4,
    estimate_population_uncertainty, calculate_percent_prediction_differences)
from .model.threshold import fit_give

from .reports.html import create_report
from .reports.utilities import cache_index

from .visuals.utilities import create_green_cm, make_ellipse, make_shapely
from .visuals.shape_display import (
    display_shapely, display_stored_cutout, display_equivalent_ellipse)
from .visuals.print_generic import print_ellipse
from .visuals.print_to_scale import print_to_pdf

from .ellipse.utilities import (
    _CustomBasinhopping, shapely_cutout, shapely_ellipse)
