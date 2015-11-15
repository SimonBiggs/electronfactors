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

from nbconvert.exporters import Exporter
from nbconvert.preprocessors import ExecutePreprocessor

def run_notebook(filename):
    export = Exporter()
    execute = ExecutePreprocessor()
    execute.timeout = 600
    export.register_preprocessor(execute, True)
    export.from_filename(filename)

def test_standalone():
    run_notebook(
        "Spline modelling electron insert factors standalone example.ipynb")

def test_measurement():
    run_notebook(
        "measurements/20150515 -- P13 remeasure.ipynb")
