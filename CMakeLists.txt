cmake_minimum_required(VERSION 3.10)

project(TuxTrax)

set(CMAKE_CXX_STANDARD 14)

find_package(PipeWire REQUIRED)
find_package(ALSA REQUIRED)

add_executable(TuxTrax main.cpp)

target_link_libraries(TuxTrax PRIVATE PipeWire::PipeWire ALSA::ALSA)
