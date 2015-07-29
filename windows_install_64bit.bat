ECHO OFF
::bitsadmin /transfer "MiniConda_download" https://repo.continuum.io/miniconda/Miniconda3-latest-Windows-x86_64.exe %~dp0\install\Miniconda3-latest-Windows-x86_64.exe
%~dp0\install\Miniconda3-latest-Windows-x86_64.exe

CALL %~dp0\install\install_dependencies.bat