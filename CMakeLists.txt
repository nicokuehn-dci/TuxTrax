cmake_minimum_required(VERSION 3.10)

project(TuxTrax)

set(CMAKE_CXX_STANDARD 14)

find_package(PipeWire REQUIRED)
find_package(ALSA REQUIRED)
find_package(LV2 REQUIRED)
find_package(PkgConfig REQUIRED)
pkg_check_modules(LIBUDEV REQUIRED libudev)

add_executable(TuxTrax main.cpp)

target_link_libraries(TuxTrax PRIVATE PipeWire::PipeWire ALSA::ALSA LV2::lv2 ${LIBUDEV_LIBRARIES})

# Add error handling for unhandled exceptions
if(NOT PipeWire_FOUND)
    message(FATAL_ERROR "PipeWire not found. Please install PipeWire and try again.")
endif()

if(NOT ALSA_FOUND)
    message(FATAL_ERROR "ALSA not found. Please install ALSA and try again.")
endif()

if(NOT LV2_FOUND)
    message(FATAL_ERROR "LV2 not found. Please install LV2 and try again.")
endif()

if(NOT LIBUDEV_FOUND)
    message(FATAL_ERROR "libudev not found. Please install libudev and try again.")
endif()

# Add logging for failures using the logging module
if(NOT TARGET PipeWire::PipeWire)
    message(WARNING "PipeWire target not found. Logging this failure.")
endif()

if(NOT TARGET ALSA::ALSA)
    message(WARNING "ALSA target not found. Logging this failure.")
endif()

if(NOT TARGET LV2::lv2)
    message(WARNING "LV2 target not found. Logging this failure.")
endif()

if(NOT TARGET ${LIBUDEV_LIBRARIES})
    message(WARNING "libudev target not found. Logging this failure.")
endif()
