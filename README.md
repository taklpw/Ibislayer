# Ibislayer

## What is in this Readme?
- WHAT IS OUR PROJECT
- WHAT DOES OUR PROJECT REQUIRE - HARDWARE/SOFTWARE/LIBRARIES
- VERSION OF PYTHON
- HOW IT ALL WORKS

## What is This Project

The Ibislayer Project, although has nothing to do with Ibis slaying, uses a Leap Motion device to fly a Parrot AR Drone 2.0. Using IR sensors and a basic UI system, it is possible to fly the drone with or without visual line of sight. The drone also has a seperate mode called automatic avoidance system, where the drone be set to take off and then avoid objects that come within 30 cm of its range.

## Project Hardware Requirements

- Leap Motion
- Parrot Ar Drone 2.0 (Any edition)
- 5x IR senors
- Raspberry Pi Zero W (Weight is the main consideration so the Zero W is the preference, though any Pi with WiFi communcations can work)
- Arduino (We use Arduino Uno, however it is also possible to use an any other Arduino with 5 Analog Inputs)
- Computer

## Project Software Requirements

- Python 2.7.13
- Leap Software
- Linux 

## Project Libraries Used

- OpenCV (http://opencv.org/)
- PS Drone (http://www.playsheep.de/drone/)
- NetCat (http://sectools.org/tool/netcat/)
- Leap Motion Libraries (https://developer.leapmotion.com/documentation/csharp/devguide/Leap_SDK_Overview.html)


