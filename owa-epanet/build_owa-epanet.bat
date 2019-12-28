cls

SET CMAKE_PATH=cmake.exe 
SET Build_PATH=%CD%
SET COMPILE_PATH=%Build_PATH%\build\

MKDIR "%COMPILE_PATH%"
CD "%COMPILE_PATH%"
%CMAKE_PATH% ../ -A x64
%CMAKE_PATH% --build . --config Release

cd ..
pause