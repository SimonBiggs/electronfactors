# Spline modelling electron insert factors using routine measurements

[![Build Status](https://travis-ci.org/SimonBiggs/electronfactors.svg?branch=master)](https://travis-ci.org/SimonBiggs/electronfactors)
[![Coverage Status](https://coveralls.io/repos/SimonBiggs/equivalent-ellipse-spline-modelling/badge.svg)](https://coveralls.io/r/SimonBiggs/equivalent-ellipse-spline-modelling)

## Description
The code here provided is for the modelling of the portion of the electron output factor that is dependent on the shape of the shielding insert mounted within the applicator. This allows modelling insert factors using only the measured factors already available at a centre. Should all outliers be removed from the data set the user might expect as low as 0.5% standard uncertainty for factor prediction with as little as 8 data points.

The paper outlining the method, once published will be available using the doi link: [10.1016/j.ejmp.2015.11.002](http://dx.doi.org/10.1016/j.ejmp.2015.11.002). A pre-print of the accepted manuscript is available at my personal website: [simonbiggs.net/paper1](http://simonbiggs.net/paper1). If you have any issues please don't hesitate to contact me (mail@simonbiggs.net), I likely will be more than happy to help. 

Any use of the code accepts the AGPL3+ license which includes no warranty that this code is fit for a particular purpose. Attempts have been made to make the code transparent and it is recommended that an experienced python programmer and physicist who understands the procedure and requirements of your centre identifies whether or not the code is fit for your use.


## Installation for Windows
 * Download the relevant Anaconda Python 3.5 install from [continuum.io/downloads](https://www.continuum.io/downloads).
 * Download the source code for the most recent release from [releases](https://github.com/SimonBiggs/electronfactors/releases).
 * Installing shapely
  * Download the relevant shapely package from [http://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely](http://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely).
   * If you have 64-bit windows you will be looking for Shapely-*.*.*-cp35-none-win_amd64.whl
  * Install shapely by:
   * Opening a command prompt and "cd" into the directory with the downloaded file
   * Then running `pip install Shapely-*.*.*-cp35-none-win_*.whl` (with * replaced with relevant file name).
 * Installing descartes
  * Run the following in a command prompt, `pip install descartes`
 * Installing RISE (optional). This is only required if you want to see the live demo slideshow, not required for actual use.
  * Download the most recent version of RISE at [github.com/damianavila/RISE/releases/](https://github.com/damianavila/RISE/releases/).
  * Extract the zip and change directory within a command prompt into the extracted file
  * Run the following within the RISE directory `python setup.py install`.

  
## Explanation of use
### Importing your insert shapes
For now the easiest method of use is to directly edit the files found within `demo/user_inputs`. There are currently two methods to import insert shapes, generic shape import, and shape coordinate import. All shape labels used throughout these import files must be unique.

#### Generic shape import
The first is by importing generic shapes (such as ellipses or rectangles). An example input csv is found here:

 * https://github.com/SimonBiggs/electronfactors/blob/master/demo/user_inputs/GenericShapeImport.csv
 
By deleting the contents of that file and replacing it with your desired insert shapes and measurements you can input generic shapes.

#### Coordinate based import
The second method is by importing arbitrary shape Cartesian coordinates. This requires three csv files. One containing all the labelled x-coordinates, the second containing all the labelled y-coordinates, the third containing the meta data such as energy, applicator, ssd, and measured factor.

Examples of these files are found here:

 * https://github.com/SimonBiggs/electronfactors/blob/master/demo/user_inputs/RawCoordsImport_metadata.csv
 * https://github.com/SimonBiggs/electronfactors/blob/master/demo/user_inputs/RawCoordsImport_XCoords.csv
 * https://github.com/SimonBiggs/electronfactors/blob/master/demo/user_inputs/RawCoordsImport_YCoords.csv

By deleting the contents of those files and replacing them with your own you will be able to import your own generic shapes. 

### Opening the jupyter notebook server
The jupyter notebook server can be started by changing directory within a command prompt into the demo folder and then running the following: `jupyter notebook`. Alternatively I have created a windows shortcut within the demo directory which can be clicked and will do this automatically.

### Parametrising and caching the modelling
Firstly, to delete the demo model cache delete all files found within `demo/model_cache`. To create your own cache pulling from the shapes you have inputted simply run the `01 Model -- Load, parameterise, and cache.ipynb` notebook from within the notebook server.

Run this notebook going `Cell > Run All`.

Once this notebook has finished go on to the next step.

### Creating interactive reports for everyday clinical use
Firstly, delete the demo report(s) found within `demo/interactive_reports`. Then as in the previous step load up and run the notebook labelled `02 Model -- Create reports.ipynb`. This will create a report for each energy/applicator/ssd combination available within the model cache. The resulting reports can be placed on a clinical shared drive for use on any computer (python not required to interactively use these report files).


## Copyright information
Copyright &#169; 2015  Simon Biggs

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
