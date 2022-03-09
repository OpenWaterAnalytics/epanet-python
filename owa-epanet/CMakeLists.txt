cmake_minimum_required(VERSION 3.8)

project(owa-epanet)

if(SKBUILD)
  message(STATUS "The project is built using scikit-build")
endif()

# Setup python
if(NOT MSVC)
    find_package (Python3 ${PYTHON_VERSION_STRING} COMPONENTS Interpreter Development.Module EXACT REQUIRED)
else()
    find_package (Python3 ${PYTHON_VERSION_STRING} COMPONENTS Interpreter Development EXACT REQUIRED)
endif()

# Setup swig
find_package(SWIG REQUIRED)
cmake_policy(SET CMP0078 NEW)
cmake_policy(SET CMP0086 NEW)
include(${SWIG_USE_FILE})
set(CMAKE_SWIG_FLAGS -py3)

message("PYTHONLIBS_VERSION_STRING: ${PYTHONLIBS_VERSION_STRING}")
message("CMAKE_SWIG_FLAGS: ${CMAKE_SWIG_FLAGS}")

# Build the EPANET library
ADD_SUBDIRECTORY(EPANET)

# Set up rpath on MacOS and Linux
if(APPLE)
    set(PACKAGE_RPATH "@loader_path")
else()
    set(PACKAGE_RPATH "$ORIGIN")
endif()


# Include files for swig
INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR})
INCLUDE_DIRECTORIES(EPANET/include)
INCLUDE_DIRECTORIES(EPANET/src/outfile/include)


# Allow target_include_directories to be used later
set_property(SOURCE wrapper/toolkit.i
    PROPERTY
        USE_TARGET_INCLUDE_DIRECTORIES TRUE
)
set_property(TARGET epanet2
    PROPERTY
        USE_TARGET_INCLUDE_DIRECTORIES TRUE
)

# Create cmake target
swig_add_library(toolkit
    TYPE
        MODULE
    LANGUAGE
        python
    SOURCES
        wrapper/toolkit.i
)

target_include_directories(toolkit
    PUBLIC
        ${Python3_INCLUDE_DIRS}
)

target_link_options(toolkit
    PUBLIC
        $<$<BOOL:${APPLE}>:-undefined dynamic_lookup>
)



swig_link_libraries(toolkit
    PUBLIC
        $<$<BOOL:$<C_COMPILER_ID:MSVC>>:Python3::Module>
        epanet2
)

set_target_properties(toolkit
    PROPERTIES
        SWIG_COMPILE_DEFINITIONS EXPORT_OUT_API
        MACOSX_RPATH TRUE
        SKIP_BUILD_RPATH FALSE
        BUILD_WITH_INSTALL_RPATH FALSE
        INSTALL_RPATH "${PACKAGE_RPATH}"
        INSTALL_RPATH_USE_LINK_PATH TRUE
)

install(TARGETS toolkit LIBRARY DESTINATION packages/epanet)

add_custom_command(
    TARGET toolkit
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy
        "${CMAKE_CURRENT_BINARY_DIR}/toolkit.py"
        $<$<BOOL:${WIN32}>:${CMAKE_CURRENT_BINARY_DIR}/_toolkit.pyd>
        $<$<BOOL:${WIN32}>:${CMAKE_CURRENT_BINARY_DIR}/bin/epanet2.dll>
        $<$<NOT:$<BOOL:${WIN32}>>:${CMAKE_CURRENT_BINARY_DIR}/lib/libepanet2.*>
        ${CMAKE_SOURCE_DIR}/packages/epanet
)

