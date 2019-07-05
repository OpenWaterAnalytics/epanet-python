cmake_minimum_required(VERSION 3.8)

if(SKBUILD)
  message(STATUS "The project is built using scikit-build")
endif()

find_package(PythonLibs 3 REQUIRED)
find_package(PythonInterp ${PYTHONLIBS_VERSION_STRING} REQUIRED)
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

SET_SOURCE_FILES_PROPERTIES(epanet.i PROPERTIES CPLUSPLUS ON)
SET_SOURCE_FILES_PROPERTIES(epanet.i PROPERTIES SWIG_FLAGS "-includeall")

# build the EPANET library
ADD_SUBDIRECTORY(EPANET)

set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
SWIG_ADD_LIBRARY( toolkit LANGUAGE python SOURCES wrapper/toolkit.i)
set_property(SOURCE toolkit.i PROPERTY USE_LIBRARY_INCLUDE_DIRECTORIES TRUE)
set_property(TARGET epanet2 PROPERTY SWIG_USE_TARGET_INCLUDE_DIRECTORIES TRUE)
SWIG_LINK_LIBRARIES(toolkit epanet2)
SWIG_LINK_LIBRARIES(toolkit ${PYTHON_LIBRARIES})
set_property(TARGET _toolkit PROPERTY INSTALL_RPATH "$ORIGIN")

IF (APPLE)
  set_target_properties(_toolkit PROPERTIES INSTALL_RPATH "@loader_path")
ENDIF (APPLE)

install(TARGETS _toolkit LIBRARY DESTINATION packages/epanet)

add_custom_command(
        TARGET _toolkit POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy
                ${CMAKE_CURRENT_BINARY_DIR}/toolkit.py
                ${CMAKE_CURRENT_BINARY_DIR}/../../../packages/epanet/toolkit.py)

add_custom_command(
        TARGET _toolkit POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy
                ${CMAKE_CURRENT_BINARY_DIR}/lib/libepanet2.*
                ${CMAKE_CURRENT_BINARY_DIR}/../../../packages/epanet/)
