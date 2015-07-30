ECHO OFF

conda install statsmodels numpy scipy nose pandas matplotlib bokeh ipython ipython-notebook ipython-qtconsole
pip install --upgrade coveralls descartes pyyaml nbopen

bitsadmin /transfer "Shapely_download" http://www.lfd.uci.edu/~gohlke/pythonlibs/3i673h27/Shapely-1.5.9-cp34-none-win_amd64.whl %~dp0\Shapely-1.5.9-cp34-none-win_amd64.whl
pip install --upgrade --use-wheel --no-index --find-links=%~dp0 shapely 

cd %~dp0\nbopen
python win-install.py