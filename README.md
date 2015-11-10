# Spline modelling electron insert factors using routine measurements

[![Build Status](https://travis-ci.org/SimonBiggs/electronfactors.svg?branch=master)](https://travis-ci.org/SimonBiggs/electronfactors)
[![Coverage Status](https://coveralls.io/repos/SimonBiggs/equivalent-ellipse-spline-modelling/badge.svg)](https://coveralls.io/r/SimonBiggs/equivalent-ellipse-spline-modelling)

## Description
The code here provided is for the modelling of the portion of the electron output factor that is dependent on the shape of the shielding insert mounted within the applicator. This allows modelling insert factors using only the measured factors already available at a centre. Should all outliers be removed from the data set the user might expect as low as 0.5% standard uncertainty for factor prediction with as little as 8 data points.

The paper outlining the method, once published will be available using the doi link: [10.1016/j.ejmp.2015.11.002](http://dx.doi.org/10.1016/j.ejmp.2015.11.002). A pre-print of the accepted manuscript is available at my personal website: [simonbiggs.net/paper1](http://simonbiggs.net/paper1). If you have any issues please don't hesitate to contact me (mail@simonbiggs.net), I likely will be more than happy to help. 

Any use of the code accepts the AGPL3+ license which includes no warranty that this code is fit for a particular purpose. Attempts have been made to make the code transparent and it is recommended that an experienced python programmer and physicist who understands the procedure and requirements of your centre identifies whether or not the code is fit for your use.


## Installation for Windows
 * Download and install the relevant Anaconda Python 3.5 install from [continuum.io/downloads](https://www.continuum.io/downloads).
 * Download the source code of this electronfactors program from [releases](https://github.com/SimonBiggs/electronfactors/releases).
 * Installing shapely
  * Download the relevant shapely package from [http://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely](http://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely).
    * If you have 64-bit windows you will be looking for `Shapely-*.*.*-cp35-none-win_amd64.whl` (with * replaced by most recent shapely version).
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
For now the easiest method of use is to directly edit the files found within `demo/user_inputs`. There are currently two methods to import insert shapes, generic shape import, and shape coordinate import. Each shape is indexed by an identifier, this can be whatever is most useful and informative for you however they must be unique throughout the import files. The units used in defining width / length / coords must simply be consistent throughout, in my examples I used all shape dimensions defined in cm at isocentre however as long as the user is consistent this is not necessary.

#### Generic shape import
The first import method is by importing generic shapes (such as ellipses or rectangles). An example input csv is found here:

 * https://github.com/SimonBiggs/electronfactors/blob/master/demo/user_inputs/GenericShapeImport.csv
 
By deleting the contents of that file and replacing it with your desired insert shapes and measurements you can input generic shapes.

#### Coordinate based import
The second import method is by importing arbitrary shape Cartesian coordinates. This requires three csv files. One containing all the labelled x-coordinates, the second containing all the labelled y-coordinates, the third containing the meta data such as energy, applicator, ssd, and measured factor. Of importance is that the index used to label the shape within each of the three files must agree.

Examples of these files are found here:

 * https://github.com/SimonBiggs/electronfactors/blob/master/demo/user_inputs/RawCoordsImport_metadata.csv
 * https://github.com/SimonBiggs/electronfactors/blob/master/demo/user_inputs/RawCoordsImport_XCoords.csv
 * https://github.com/SimonBiggs/electronfactors/blob/master/demo/user_inputs/RawCoordsImport_YCoords.csv

By deleting the contents of those files and replacing them with your own you will be able to import your own generic shapes.

#### Creating a custom import method
There is no reason why a custom import method cannot be created (such as directly pulling from the treatment planning system files). The only requirement is that the created import method appends your shapes into `demo/imported_data/merged.yml`. Its format is yaml and an example of how the data is stored can be found here:

 * https://github.com/SimonBiggs/electronfactors/blob/master/demo/imported_data/merged.yml

I use pyyaml for easy loading and saving of yaml files.
 
Your custom import script needs to be called within the `01 Model -- Load, parameterise, and cache.ipynb` notebook after the `convert_merge()` function and before the `parameterise()` function.

### Opening the jupyter notebook server
The jupyter notebook server can be started by changing directory within a command prompt into the demo folder and then running the following: `jupyter notebook`. Alternatively I have created a windows shortcut within the demo directory which can be clicked and will do this automatically.

Details about what the jupyter notebook is can be found [here](http://jupyter-notebook-beginner-guide.readthedocs.org/en/latest/what_is_jupyter.html).

### Parametrising and caching the modelling
Delete the demo model cache delete all files found within `demo/model_cache`. To create your own cache pulling from the shapes you have inputted simply run the `01 Model -- Load, parameterise, and cache.ipynb` notebook from within the notebook server.

Run this notebook going `Cell > Run All`.

Of high importance at this step as that each shape and the resulting equivalent ellipse is visually checked. It needs to be confirmed by the user at this stage that the expected loss of lateral scatter is sufficiently equivalent between each equivalent ellipse and its corresponding insert. This is of particular issue if the long axis of the shape is becoming small enough to a point that lateral scatter along this axis may not be equivalent between the two shapes.

Of second note is that specifically placed "saw tooth" indents may result in the width being underestimated. Although I have not observed this being an issue in clinical shapes, nevertheless, at this stage the user needs to visually confirm that the equivalent ellipse algorithim is working as intended.

### Creating interactive reports
Delete the demo report(s) found within `demo/interactive_reports`. Then as in the previous step load up and run the notebook labelled `02 Model -- Create reports.ipynb`. This will create a report for each energy/applicator/ssd combination available within the model cache. The resulting reports can be placed on a shared drive for use on any computer (python not required to interactively use these interactive report files).

An example of one such of these interactive reports can be found here:
 * http://simonbiggs.net/electronfactors

Be sure to observe the "prediction differences" column in these reports as this represents the percent prediction difference that results when a shape is removed from the model and then predicted by the model. It is important that a sufficient number of shapes are measured so that the user can observe the resulting prediction differences over the range of the desired use of the model.

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
