::
::  before_build.bat - Prepares for epanet toolkit and output module builds
::
::  Date Created: 12/12/2018
::
::  Author: Michael E. Tryby
::          US EPA - ORD/NRMRL
::
:: Requires:
::     git
::     CMake
::     Visual Studio Build Tools
::     SWIG
::
:: Note:
::     This script must be located at the root of the project folder
::     in order to work correctly.
::


:: Determine project path and strip trailing \ from path
set "PROJECT_PATH=%~dp0"
IF %PROJECT_PATH:~-1%==\ set "PROJECT_PATH=%PROJECT_PATH:~0,-1%"

set TOOLKIT_PATH=\epanet_python\toolkit\epanet\toolkit
set OUTPUT_PATH=\epanet_python\output\epanet\output


mkdir buildlib
cd buildlib
git clone --branch=dev https://github.com/OpenWaterAnalytics/EPANET.git
cd epanet


mkdir buildprod
cd buildprod
cmake -G"Visual Studio 14 2015 Win64" -DBUILD_PY_LIB=ON -DBUILD_TESTS=OFF ..
cmake --build . --config Release


copy /Y .\bin\Release\epanet_py.dll  %PROJECT_PATH%\%TOOLKIT_PATH%
copy /Y .\lib\Release\epanet_py.lib  %PROJECT_PATH%\%TOOLKIT_PATH%
copy /Y ..\include\*.h  %PROJECT_PATH%\%TOOLKIT_PATH%

copy /Y .\bin\Release\epanet-output.dll  %PROJECT_PATH%\%OUTPUT_PATH%
copy /Y .\lib\Release\epanet-output.lib  %PROJECT_PATH%\%OUTPUT_PATH%
copy /Y ..\src\outfile\include\*.h  %PROJECT_PATH%\%OUTPUT_PATH%


:: Generate swig wrappers
cd %PROJECT_PATH%\%TOOLKIT_PATH%
swig -python -py3 toolkit.i
cd %PROJECT_PATH%\%OUTPUT_PATH%
swig -python -py3 output.i


:: Return to project root
cd %PROJECT_PATH%
