ECHO OFF

conda install statsmodels numpy scipy nose pandas matplotlib bokeh ipython ipython-notebook ipython-qtconsole
pip install --upgrade coveralls descartes pyyaml nbopen

:choice1
set /P c=Download and install shapely? ([Y]/N)?
if /I "%c%" EQU "Y" goto :shapely_install
if /I "%c%" EQU "N" goto :skip_shapely_install
goto :choice1

:shapely_install
bitsadmin /transfer "Shapely_download" http://www.lfd.uci.edu/~gohlke/pythonlibs/3i673h27/Shapely-1.5.9-cp34-none-win_amd64.whl %~dp0\Shapely-1.5.9-cp34-none-win_amd64.whl
pip install --upgrade --use-wheel --no-index --find-links=%~dp0 shapely 

:skip_shapely_install


:choice2
set /P c=Install nbopen? ([Y]/N)?
if /I "%c%" EQU "Y" goto :nbopen_install
if /I "%c%" EQU "N" goto :skip_npopen_install
goto :choice2

:nbopen_install
cd %~dp0\nbopen
python win-install.py

:skip_npopen_install