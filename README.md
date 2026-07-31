# COSMOS Cluster 11 Final Project
## The Objective
Make an autonomous robot city based on a provided map. The robots should be able to interact with each other and maintain tasks after their interactions. All robots are Maqueen Plus V2 kits with BBC micro:bits as the microcontrollers. The milestones for completion are:
* Milestone 1: Navigate the outer track without human intervention for one full lap.
* Milestone 2: Detect and keep a gap between vehicles of a set distance apart around the entire outer lap of the track.
* Milestone 3: Stop at any stop signs on the map.
* Milestone 4: Obey posted speed limit signs on the map.
* Milestone 5: Navigate an intersection according to traffic laws.

## The Code
We were successfully able to implement Milestones 1, 2, and 3.
### Milestone 1
Outer track navigation operates on a PID controller algorithm. It reads the ADC values from the robot's built-in line sensors and then calculates the correction according to PID.

### Milestone 2
The robot's attached LiDAR sensor reads the distance from the robot to an object in front of it, which, in this milestone, is another robot. If the distance between the two robots is below a set number for slowing down, then the robot will calculate what speed it should go at to maintain the distance and set the global speed variable to that value. If it is below a set number for stopping, then the global speed variable will be set to zero.

### Milestone 3
We affixed black tape at the intersections, under the stop signs, to allow the line sensors to detect where an intersection is. The robots will stop at an intersection and wait for instructions from the traffic controller on the next move to take. The movements through an intersection are hardcoded movement values.

## Our results
We were able to complete Milestones 1-3, which were done via a modified version of the code in vehicle-base.py. 

## Info
This code is meant to be pasted into the Makecode editor for micro:bits and uses the DFRobot Maqueen Plus V2 library.
