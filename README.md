# Spline modelling electron insert factors using routine measurements

[![Build Status](https://travis-ci.org/SimonBiggs/electronfactors.svg?branch=master)](https://travis-ci.org/SimonBiggs/electronfactors)
[![Coverage Status](https://coveralls.io/repos/SimonBiggs/electronfactors/badge.svg?branch=master&service=github)](https://coveralls.io/github/SimonBiggs/electronfactors?branch=master)


## Description
The code here provided is for the modelling of the portion of the electron output factor that is dependent on the shape of the shielding insert mounted within the applicator. This allows modelling insert factors using only the measured factors already available at a centre. Should all outliers be removed from the data set the user might expect as low as 0.5% standard uncertainty for factor prediction with as little as 8 data points.

The paper outlining this method is currently in press:

 > S. Biggs, M. Sobolewski, R. Murry, J. Kenny, Spline modelling electron insert factors using routine measurements. Physica Medica (2015), [doi:10.1016/j.ejmp.2015.11.002](http://dx.doi.org/10.1016/j.ejmp.2015.11.002).

A pre-print of the accepted manuscript is available at my personal website: [simonbiggs.net/paper1](http://simonbiggs.net/paper1). If you have any issues please don't hesitate to contact me (mail@simonbiggs.net), I likely will be more than happy to help.

Any use of the code accepts the AGPL3+ license which includes no warranty that this code is fit for a particular purpose. Attempts have been made to make the code transparent and it is recommended that an experienced python programmer and physicist who understands the procedure outlined in the paper and the requirements of your centre identifies whether or not this method and code is fit for your use.


## Installation for Windows
Download Anaconda Python 3.5 from [continuum.io/downloads](https://www.continuum.io/downloads).

Install Anaconda
 * Make sure "Add Anaconda to my PATH environment variable" and "Register Anaconda as my default Python 3.5" are ticked.

Download the Shapely module from [here](http://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely).
 * If you have 64-bit windows with python 3.5 you will be looking for `Shapely-*.*.*-cp35-none-win_amd64.whl` (with * replaced by most recent shapely version).

Open jupyter qtconsole:
 * Press [Windows Key] + R
 * Type: `jupyter qtconsole`
 * Press Enter

To install electronfactors and descartes, within the jupyter console, type:

    !pip install descartes electronfactors

To install the downloaded shapely file I assume the shapely file was downloaded into your Downloads library and the version downloaded was 1.5.13. If this is not the case change what is written here to match the downloaded file. Within the jupyter console type:

    !pip install Downloads/Shapely-1.5.13-cp35-none-win_amd64.whl

To be able to make use of the examples referred to for the remaining of this guide make sure you download the most recent electronfactors source code found [here](https://github.com/SimonBiggs/electronfactors/releases).


## Installation for Ubuntu
From a fresh install of Ubuntu, using pip to install all dependencies the following method can be used. However, of course if you prefer, system packages may be used from apt-get, or conda from anaconda.

    sudo apt-get build-dep python-numpy matplotlib python-scipy pandas ipython pyzmq python-shapely pyyaml
    sudo apt-get install python3-pip
    sudo pip3 install --upgrade pip numpy matplotlib scipy pandas shapely descartes bokeh pyyaml jupyter electronfactors



## Explanation of use
At this point of time there are two options available for using this code. The first method is outlined in detail below and requires using the example files that comes with downloading the code from [releases](https://github.com/SimonBiggs/electronfactors/releases). This involves using csv files which can be edited with microsoft excel or libre office calc (and resaved as .csv, not .xls) and then the ready made notebooks can be used to pull from these csv files.

The second option requires only the jupyter notebook (or just python if you choose) and python dictionaries are used to input the cutout shapes. This second option  is explained in detail in the standalone notebook found here:

 > [Spline modelling electron insert factors using routine measurements.ipynb](http://nbviewer.ipython.org/github/SimonBiggs/electronfactors/blob/master/Spline%20modelling%20electron%20insert%20factors%20standalone%20example.ipynb)

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

Your custom import script needs to be called within the [`01 Model -- Load, parameterise, and cache.ipynb`](http://nbviewer.ipython.org/github/SimonBiggs/electronfactors/blob/master/demo/01%20Model%20--%20Load%2C%20parameterise%2C%20and%20cache.ipynb) notebook after the `convert_merge()` function and before the `parameterise()` function.

An example of a utlitiy I made for pulling the insert shapes directly from the XiO server within our centre can be found here (please note this example is intended as an example only, it is minimally tested and will likely need adaptation and bug fixing):

 * http://nbviewer.ipython.org/github/SimonBiggs/electronfactors/blob/master/historical_exploration_and_measurement/scripts/xio.ipynb

### Opening the jupyter notebook server
The jupyter notebook server can be started by changing directory within a command prompt into the demo folder and then running the following: `jupyter notebook`. Alternatively I have created a windows shortcut within the demo directory which can be clicked and will do this automatically.

Details about what the jupyter notebook is can be found [here](http://jupyter-notebook-beginner-guide.readthedocs.org/en/latest/what_is_jupyter.html).

### Parametrising and caching the modelling
Before creating your own model the cache of the demo model needs to be deleted. This is achieved by deleting all files found within `demo/model_cache`. To create your own cache pulling from the shapes you have inputted simply run the [`01 Model -- Load, parameterise, and cache.ipynb`](http://nbviewer.ipython.org/github/SimonBiggs/electronfactors/blob/master/demo/01%20Model%20--%20Load%2C%20parameterise%2C%20and%20cache.ipynb) notebook from within the notebook server. This notebook will look something like this:

 * http://nbviewer.ipython.org/github/SimonBiggs/electronfactors/blob/master/demo/01%20Model%20--%20Load%2C%20parameterise%2C%20and%20cache.ipynb

Run this notebook going `Cell > Run All`.

Of high importance at this step as that each shape and the resulting equivalent ellipse is visually checked. It needs to be confirmed by the user at this stage that the expected loss of lateral scatter is sufficiently equivalent between each equivalent ellipse and its corresponding insert. This is of particular issue if the long axis of the shape is becoming small enough to a point that lateral scatter along this axis may not be equivalent between the two shapes.

Of second note is that specifically placed "saw tooth" indents may result in the width being underestimated. Although I have not observed this being an issue in clinical shapes, nevertheless, at this stage the user needs to visually confirm that the equivalent ellipse algorithim is working intelligently.

### Creating interactive reports
Delete the demo report(s) found within `demo/interactive_reports`. Then as in the previous step load up and run the notebook labelled [`02 Model -- Create reports.ipynb`](http://nbviewer.ipython.org/github/SimonBiggs/electronfactors/blob/master/demo/02%20Model%20--%20Create%20reports.ipynb). This will create a report for each energy/applicator/ssd combination available within the model cache. The resulting reports can be placed on a shared drive for use on any computer (python not required to interactively use these report files).

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
