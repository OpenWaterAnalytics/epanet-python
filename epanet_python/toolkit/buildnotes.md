## Build Notes 

Hints for building EPANET Toolkit SWIG wrapper on Windows. This package
is currently under active development. The build process is likely to change. 


### Dependencies
- Python 3.6.5 64 bit 
- Visual Studio 14 2015
- CMake
- SWIG


### Build Process
The idea here is to build the EPANET library seperately and link it with the SWIG wrapper. This approach uses implicit linking, therefore, an import library must be created. CMake does this automatically using the Generate Export Header function. Once built the EPANET library and headers are manually copied to the epanet-toolkit directory. To run, the resulting epanet-toolkit.pyd needs the epanet.dll.   


Step 1 - Build EPANET Library

Checkout the dev branch of the OWA EPANET project. Build the EPANET Library using CMake generator "Visual Studio 14 2015 Win64". Be sure "generate export header" section of the EPANET Project CMakeLists.txt is not commented out. 


Step 2 - Copy EPANET Library

Checkout the dev branch of the OWA epanet-python project. In the epanet\toolkit directory copy epanet2.h, epanet_export.h, epanet.dll, and epanet.lib all together in the same folder. The setup.py file is configured to find them there. 


Step 3 - Build EPANET Toolkit

Execute the command `python setup.py build`. The package in the build folder should contain epanet.dll, toolkit.py, toolkit.*.pyd, and __init__.py files. With the python setup working you can create a wheel or do a dev install using the pip -e flag.   


Step 4 - Running EPANET Toolkit

Install the .pyd and the .dll in the same directory and add the directory to the python path. 


#### Common Problems
When I used the Developer Command Prompt for Visual Studio 2015 the build fails with linking errors. Use a regular Command Prompt to build. 
