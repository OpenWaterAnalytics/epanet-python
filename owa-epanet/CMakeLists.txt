cmake_minimum_required(VERSION 3.8)

project(OWA-EPANET)

if(SKBUILD)
  message(STATUS "The project is built using scikit-build")
endif()

find_package(PythonLibs 3 REQUIRED)
find_package(PythonInterp ${PYTHONLIBS_VERSION_STRING} REQUIRED)
# If find_package() has difficulty finding the appropriate python 
# directories and libraries (especially in Windows with multiple 
# versions of python) set them manually as in the next three lines 
# below (and comment out the above two find_package() lines):
# set(PYTHON_EXECUTABLE "c:/python/python38/python.exe")
# set(PYTHON_INCLUDE_PATH "c:/python/python38/include")
# set(PYTHON_LIBRARIES "c:/python/python38/libs/python38.lib")

find_package(SWIG REQUIRED)
include(${SWIG_USE_FILE})
set(CMAKE_SWIG_FLAGS -py3)

message("PYTHONLIBS_VERSION_STRING: ${PYTHONLIBS_VERSION_STRING}")
message("CMAKE_SWIG_FLAGS: ${CMAKE_SWIG_FLAGS}")

INCLUDE_DIRECTORIES(${PYTHON_INCLUDE_PATH})
INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR})
INCLUDE_DIRECTORIES(EPANET/include)
INCLUDE_DIRECTORIES(EPANET/src/outfile/include)

SET(CMAKE_SWIG_FLAGS "")

SET_SOURCE_FILES_PROPERTIES(toolkit.i PROPERTIES CPLUSPLUS ON)
SET_SOURCE_FILES_PROPERTIES(toolkit.i PROPERTIES SWIG_FLAGS "-includeall")


# build the EPANET library
ADD_SUBDIRECTORY(EPANET)

set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

SWIG_ADD_LIBRARY( toolkit LANGUAGE python SOURCES wrapper/toolkit.i )
set_property(SOURCE toolkit.i PROPERTY USE_LIBRARY_INCLUDE_DIRECTORIES TRUE)
set_property(TARGET epanet2 PROPERTY SWIG_USE_TARGET_INCLUDE_DIRECTORIES TRUE)
SWIG_LINK_LIBRARIES(toolkit epanet2)

SWIG_LINK_LIBRARIES(toolkit ${PYTHON_LIBRARIES})
set_property(TARGET _toolkit PROPERTY INSTALL_RPATH "$ORIGIN")

#SWIG_ADD_LIBRARY( output LANGUAGE python SOURCES wrapper/output.i )
#SET_PROPERTY( SOURCE output.i PROPERTY USE_LIBRARY_INCLUDE_DIRECTORIES TRUE )
#SET_PROPERTY( TARGET epanet-output PROPERTY SWIG_USE_TARGET_INCLUDE_DIRECTORIES TRUE )
#SWIG_LINK_LIBRARIES( output epanet-output)
#SWIG_LINK_LIBRARIES( output ${PYTHON_LIBRARIES} )
#SET_PROPERTY( TARGET _output PROPERTY INSTALL_RPATH "$ORIGIN" )

IF (APPLE)
  set_target_properties(_toolkit PROPERTIES INSTALL_RPATH "@loader_path")
ENDIF (APPLE)

install(TARGETS _toolkit LIBRARY DESTINATION packages/epanet)

add_custom_command(
        TARGET _toolkit POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy
                ${CMAKE_CURRENT_BINARY_DIR}/toolkit.py
                ${CMAKE_CURRENT_BINARY_DIR}/../../../packages/epanet/toolkit.py)

IF(WIN32)
    add_custom_command(
            TARGET _toolkit POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E copy
                    ${CMAKE_CURRENT_BINARY_DIR}/lib/Release/_toolkit.pyd
                    ${CMAKE_CURRENT_BINARY_DIR}/../../../packages/epanet/_toolkit.pyd)
    add_custom_command(
            TARGET _toolkit POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E copy
                    ${CMAKE_CURRENT_BINARY_DIR}/bin/Release/epanet2.dll
                    ${CMAKE_CURRENT_BINARY_DIR}/../../../packages/epanet/epanet2.dll)
ELSE(True)
    add_custom_command(
            TARGET _toolkit POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E copy
                    ${CMAKE_CURRENT_BINARY_DIR}/lib/libepanet2.*
                    ${CMAKE_CURRENT_BINARY_DIR}/../../../packages/epanet/)
ENDIF(WIN32)



#add_custom_command(
#        TARGET _toolkit POST_BUILD
#        COMMAND ${CMAKE_COMMAND} -E copy
#                ${CMAKE_CURRENT_BINARY_DIR}/output.py
#                ${CMAKE_CURRENT_BINARY_DIR}/../../../packages/epanet/output.py)

#add_custom_command(
#        TARGET _toolkit POST_BUILD
#        COMMAND ${CMAKE_COMMAND} -E copy
#                ${CMAKE_CURRENT_BINARY_DIR}/lib/libepanet-output.*
#                ${CMAKE_CURRENT_BINARY_DIR}/../../../packages/epanet/)
