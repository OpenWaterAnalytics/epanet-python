::
::  before_build.bat - Prepares for epanet toolkit and output module builds
::
::  Date Created: 12/12/2018
::
::  Author: Michael E. Tryby
::          US EPA - ORD/NRMRL
::

set PROJECT_PATH=%~1

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
copy /Y ..\tools\epanet-output\include\*.h  %PROJECT_PATH%\%OUTPUT_PATH%
