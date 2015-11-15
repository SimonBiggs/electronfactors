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

def test_where_to_measure():
    run_notebook(
        "paper/Discussion -- Example of where to first measure.ipynb")

def test_equivalent_ellipse_example():
    run_notebook(
        "paper/Method -- Equivalent ellipse example.ipynb")

def test_deformability_example():
    run_notebook(
        "paper/Method -- Fit deformability example.ipynb")

def test_change_uncertainty_with_num_meas():
    run_notebook(
        "paper/"
        "Results -- Change in uncertainty with number of measurements.ipynb")

def test_collated_prediction_uncertainties():
    run_notebook(
        "paper/"
        "Results -- Collated prediction uncertainties.ipynb")

def test_contour_plots():
    run_notebook(
        "paper/"
        "Results -- Contour plots of model.ipynb")

def test_prediction_diff_histograms():
    run_notebook(
        "paper/"
        "Results -- Percent prediction difference histograms.ipynb")

def test_automatically_discerning_outliers():
    run_notebook(
        "paper/"
        "Results -- "
        "Point at which an outlier is automatically discernable.ipynb")

def test_prediction_diffs_of_eight():
    run_notebook(
        "paper/"
        "Results -- Prediction with eight point data subsets.ipynb")

def test_printing_utility():
    run_notebook(
        "paper/"
        "Utility -- Printing shapes to scale for subsequent measurement.ipynb")
