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

from runipy.notebook_runner import NotebookRunner
from nbformat import read

import os, contextlib

@contextlib.contextmanager
def temp_chdir(path):
    """
    Usage:
    >>> with temp_chdir(gitrepo_path):
    ...   subprocess.call('git status')
    """
    starting_directory = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(starting_directory)


def run_notebook(filename):
    notebook = read(open(filename), as_version=3)
    r = NotebookRunner(notebook)
    r.run_notebook()

def test_where_to_measure():
    with temp_chdir("paper/"):
        run_notebook(
            "Discussion -- Example of where to first measure.ipynb")

def test_equivalent_ellipse_example():
    with temp_chdir("paper/"):
        run_notebook(
            "Method -- Equivalent ellipse example.ipynb")

def test_deformability_example():
    with temp_chdir("paper/"):
        run_notebook(
            "Method -- Fit deformability example.ipynb")

def test_change_uncertainty_with_num_meas():
    with temp_chdir("paper/"):
        run_notebook(
            "Results -- "
            "Change in uncertainty with number of measurements.ipynb")

def test_collated_prediction_uncertainties():
    with temp_chdir("paper/"):
        run_notebook(
            "Results -- Collated prediction uncertainties.ipynb")

def test_contour_plots():
    with temp_chdir("paper/"):
        run_notebook(
            "Results -- Contour plots of model.ipynb")

def test_prediction_diff_histograms():
    with temp_chdir("paper/"):
        run_notebook(
            "Results -- Percent prediction difference histograms.ipynb")

def test_automatically_discerning_outliers():
    with temp_chdir("paper/"):
        run_notebook(
            "Results -- "
            "Point at which an outlier is automatically discernable.ipynb")

def test_prediction_diffs_of_eight():
    with temp_chdir("paper/"):
        run_notebook(
            "Results -- Prediction with eight point data subsets.ipynb")

def test_printing_utility():
    with temp_chdir("paper/"):
        run_notebook(
            "Utility -- "
            "Printing shapes to scale for subsequent measurement.ipynb")
