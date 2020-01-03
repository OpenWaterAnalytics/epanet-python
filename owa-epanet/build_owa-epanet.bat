cls

git submodule update --init

SET CMAKE_PATH=cmake.exe 
SET Build_PATH=%CD%
SET COMPILE_PATH=%Build_PATH%\build\

MKDIR "%COMPILE_PATH%"
CD "%COMPILE_PATH%"
rem Building 64-bit toolkit for 64-bit python.
rem If 32-bit toolkit is required ensure 32-bit python is located 
rem by cmake (check CmakeList.txt) and replace '%CMAKE_PATH% ../ -A x64'
rem with '%CMAKE_PATH% ../ -A Win32'."
%CMAKE_PATH% ../ -A x64
%CMAKE_PATH% --build . --config Release

rem 'After successful compilation "toolkit.py", "_toolkit.pyd", "epanet2.dll" will be created. You can start using the toolkit by importing the module "toolkit.py".

cd ..
pause