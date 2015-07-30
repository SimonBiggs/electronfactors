ECHO OFF

:choice
set /P c=Download and install miniconda? ([Y]/N)?
if /I "%c%" EQU "Y" goto :conda_install
if /I "%c%" EQU "N" goto :skip_conda_install
goto :choice

:conda_install
bitsadmin /transfer "MiniConda_download" https://repo.continuum.io/miniconda/Miniconda3-latest-Windows-x86_64.exe %~dp0\windows_install\Miniconda3-latest-Windows-x86_64.exe
%~dp0\windows_install\Miniconda3-latest-Windows-x86_64.exe

:skip_conda_install
CALL %~dp0\windows_install\install_dependencies_64bit.bat