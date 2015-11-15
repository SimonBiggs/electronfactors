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

# def test_demo_load_parameterise_cache():
#     with temp_chdir("demo/"):
#         run_notebook(
#             "01 Model -- Load, parameterise, and cache.ipynb")

# def test_demo_create_reports():
#     with temp_chdir("demo/"):
#         run_notebook(
#             "02 Model -- Create reports.ipynb")

# def test_demo_slideshow():
#     with temp_chdir("demo/"):
#         run_notebook(
#             "Slideshow.ipynb")
