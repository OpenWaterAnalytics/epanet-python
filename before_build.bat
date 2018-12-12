::
::  before_build.bat - Prepares for epanet toolkit and output module builds
::
::  Date Created: 12/12/2018
::
::  Author: Michael E. Tryby
::          US EPA - ORD/NRMRL
::


mkdir buildlib
cd buildlib
git clone --branch=dev-swig-redux https://github.com/michaeltryby/EPANET.git
cd epanet


mkdir buildprod
cd buildprod
cmake -G"Visual Studio 14 2015 Win64" -DBUILD_TESTS=0 ..
cmake --build . --config Release


copy /Y .\bin\Release\epanet2.dll ..\..\..\toolkit\epanet\toolkit\
copy /Y .\lib\Release\epanet2.lib ..\..\..\toolkit\epanet\toolkit\
copy /Y ..\include\*.h ..\..\..\toolkit\epanet\toolkit\

copy /Y .\bin\Release\epanet-output.dll ..\..\..\output\epanet\output\
copy /Y .\lib\Release\epanet-output.lib ..\..\..\output\epanet\output\
copy /Y ..\tools\epanet-output\include\*.h ..\..\..\output\epanet\output\
