cmake_minimum_required(VERSION 2.8.3)
project(yaml_utils)

## Add some compile flags
set(ADDITIONAL_CXX_FLAG "-Wall -O3 -g")
ADD_COMPILE_OPTIONS(-std=c++14 )
## Find catkin macros and libraries
# find_package(catkin REQUIRED COMPONENTS
#   roscpp
# )

find_package(Eigen3 REQUIRED)
find_package(yaml-cpp REQUIRED)

catkin_package(
  INCLUDE_DIRS include
  LIBRARIES yaml_utils
)

include_directories(
  include
  ${EIGEN3_INCLUDE_DIRS}
  # ${catkin_INCLUDE_DIRS}
  ${YAML_CPP_INCLUDE_DIR}
)

add_library(yaml_utils src/yaml_utils.cpp)

target_link_libraries(yaml_utils
  # ${YAML_CPP_LIBRARY_DIR} 
  /usr/local/lib/libyaml-cpp.a

  # /usr/lib/aarch64-linux-gnu/libyaml-cpp.so
  ${catkin_LIBRARIES}
)
