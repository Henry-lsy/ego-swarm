#include "yaml_utils.hpp"
#include <iostream>


void readWaypointsFromFile(const std::string & path, double waypoints[50][3])
{
    YAML::Node node = YAML::LoadFile(path);
    for(int i = 0; i < node.size(); i++)
    {
      waypoints[i][0] = node[i]["x"].as<double>();
      waypoints[i][1] = node[i]["y"].as<double>();
      waypoints[i][2] = node[i]["z"].as<double>();
      std::cout << "get waypoints " << waypoints[i][0] << " "<< waypoints[i][1] <<" "<< waypoints[i][2] << std::endl;
    }
}