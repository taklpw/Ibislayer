###################################################################
# Ibis Slayer Drone                                               #
# Authors: Akash Bhatia, Bill Wang, Kelly Lynch, Taylor Barker    #
# Description: Parrot A.R Drone 2.0 controlled by your hand with  #
# a Leap Motion.                                                  #
# TODO:                                                           #
# - Make this drone a total coward by backing away from           #
# everything.                                                     #
# - Add UI                                                        #
###################################################################

# Imports
import os
import signal
import csv
import sys
import curses
sys.path.insert(0, "../lib/leap")
import Leap, thread, time
sys.path.insert(0, "../lib/psdrone")
import ps_drone

# Configure & Connect to Drone
drone = ps_drone.Drone()
drone.startup()
drone.reset()

# Get Drone Battery Level, Quit if battery is too low
while(drone.getBattery()[0]==-1): time.sleep(0.1)
print "Battery: "+str(drone.getBattery()[0])+"% "+str(drone.getBattery()[1])
if drone.getBattery()[1] == "empty": sys.exit()

# Use the demo NavData package (15Hz Sensors)
drone.useDemoMode(True)
drone.getNDpackage(["demo"])
time.sleep(0.5)

# Recalibrate Sensors
drone.trim()
drone.getSelfRotation(5)

# Camera Setup
drone.setConfigAllID()                                       # Go to multiconfiguration-mode
drone.sdVideo()                                              # SD Video
drone.frontCam()                                             # Choose front view (There is no other view)
CDC = drone.ConfigDataCount
while CDC == drone.ConfigDataCount:       time.sleep(0.0001) # Wait until Configuration is done
drone.startVideo()                                           # Start video
drone.showVideo()                                            # Display the video using OpenCV

# Start UI
#screen = curses.initscr()
#screen.border(0)

# Global Variables from Leap Input
handClosed = True
handRoll = 0
handPitch = 0
handYaw = 0
handLevel = 0
handCount = 0

# Other Global Variables
autoMode = False
leapStatusDisplay = "Not Connected"
piStatusDisplay = "Not Connected"
droneStatusDisplay = "Unknown      "
flightmodeDisplay = "Manual       "
landed = True
navData = []
NDC = drone.NavDataCount



# Leap Motion Listener
class SampleListener(Leap.Listener):

    # Debug information for leap connectivity
    def on_init(self, controller):
        #print "Initialized"
        global leapStatusDisplay
        leapStatusDisplay = "Initialising"

    def on_connect(self, controller):
        #print "Connected"
        global leapStatusDisplay
        leapStatusDisplay = "OK          "

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        #print "Disconnected"
        drone.stop()
        global leapStatusDisplay
        leapStatusDisplay = "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    # When a new frame is detectedrol
    def on_frame(self, controller):
        # Get the most recent frame from the Leap
        frame = controller.frame()

        # Set Global Variables
        global handClosed
        global handPitch
        global handRoll
        global handYaw
        global handLevel
        global handCount

        handCount = len(frame.hands)

        # Get hands
        for hand in frame.hands:

            # Identify which hand is being detected
            handType = "Left hand" if hand.is_left else "Right hand"
            strength = hand.grab_strength
            if strength > 0.4:
                handClosed = True
            else:
                handClosed = False

            # Send hand information to global variables
            normal = hand.palm_normal
            direction = hand.direction
            handPitch = direction.pitch
            handRoll = normal.roll
            handYaw = direction.yaw
            handLevel = hand.palm_position.y


def main():
    # Create a Leap listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Add Leap Motion Listener (runs like an interrupt)
    controller.add_listener(listener)

    print "Press Space Bar to quit..."

    while 1:
	# Exit program if spacebar is hit
	if drone.getKey() == ' ':
	    drone.land()

	    # Store Navigation data in CSV
	    with open("../data/output.csv", "wb") as f:
	        writer = csv.writer(f)
                writer.writerows(navData)

            # Remove Leap listener
            controller.remove_listener(listener)
            
            # End screen
            curses.endwin()

            # Exit the program
            sys.exit(0)

	    # Control Drone
        dronecontrolling()

        # Log Data
        logData()

        #Collect Flight info and display it
        uiDisp()


def dronecontrolling():
    # Use global variablkes
    global landed
    global drone

    # Initialise local variables (lower numbers = higher sensitivity)
    rollSens = 100	 # Roll Sensitivity, nominally between 100 and 180
    pitchSens = 70	 # Pitch Sensitivity, nominally between 100 and 180
    yawSens = 100	 # Yaw Sensitivity, nominally between 100 and 180
    thrustSensLow = 100  # Low Value of thrust sensitivity, nominally around 50 to 100
    thrustSensHigh = 400 # High Value of thrust sensitivity, nominally around 400-500

    # Land and takeoff depending on whether your hand is open or closed
    if (handClosed and not landed) or (handCount < 1 and not landed):
        drone.land()
        drone.stop()
        print "Land"
        landed = True
    elif not handClosed and landed and handCount > 0:
        #drone.takeoff()
        print "Calibrating, Please Wait"
        time.sleep(7.5)
        print "Take Off"
        landed = False

    # Scale values based on sensitivity
    rollVal = mapVals(-handRoll * Leap.RAD_TO_DEG, -rollSens, rollSens, -1, 1 )
    pitchVal = mapVals(-handPitch * Leap.RAD_TO_DEG, -pitchSens, pitchSens, -1, 1)
    yawVal = mapVals(handYaw * Leap.RAD_TO_DEG, -yawSens, yawSens, -1, 1)
    thrustVal = mapVals(handLevel, thrustSensLow, thrustSensHigh, -1, 1)

    # Cap Values at 1 and -1 and create a deadzone
    rollVal = deadZone(capVals(rollVal), 0.1)
    pitchVal = deadZone(capVals(pitchVal), 0.1)
    yawVal = deadZone(capVals(yawVal), 0.1)
    thrustVal = deadZone(capVals(thrustVal), 0.1)

    # Send movement command
    if not landed:
        # Delay to allow time between sending commands
        time.sleep(0.01) # 100Hz
        #drone.move(rollVal, pitchVal, thrustVal, yawVal)
    return


# Map input values between two values
def mapVals(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


# Cap the input value between -1 and 1
def capVals(val):
    if val is None:
	val = 0

    if val > 1:
        return 1
    elif val < -1:
        return -1
    else:
        return val


# Deadzone the controls so neutral hand position feels better
def deadZone(inputNum, thresh):
    if inputNum > 0:
        if inputNum-thresh < 0:
	    return 0
    elif inputNum < 0:
	if -inputNum-thresh < 0:
	    return 0
    elif inputNum == 0:
	return 0

    # Smooths deadzone so it doesn't jump when exited
    if inputNum > 0:
        return inputNum - thresh
    if inputNum < 0:
	return inputNum + thresh


# Log data from the drone when in flight at a rate of 15Hz
def logData():
    # Navigation Data Count
    global NDC
    # Stores data in the form of [time, alititude, roll, pitch, yaw, x speed, y speed, z speed]
    global navData

    # If new data is here
    if drone.NavDataCount > NDC:

        # Collect Data
        recieveTime = drone.NavDataTimeStamp
        decodeTime = drone.NavDataDecodingTime
        navTime = recieveTime - decodeTime
        navAltitude = drone.NavData["demo"][3]
        navRoll = drone.NavData["demo"][2][1]
        navPitch = drone.NavData["demo"][2][0]
        navYaw = drone.NavData["demo"][2][2]
        xSpeed = drone.NavData["demo"][4][0]
        ySpeed = drone.NavData["demo"][4][1]
        zSpeed = drone.NavData["demo"][4][2]

     	# Store Data
    	navData.append([navTime, navAltitude, navRoll, navPitch, navYaw, xSpeed, ySpeed, zSpeed])
    	NDC = drone.NavDataCount
    return


# Inputs: Battery Level, Yaw, Pitch, Roll, Altitude, Emergency Status
# Outputs: Displays information to the user via the terminal
# TODO: Add IR stuff
def uiDisp():
    # Initialise Global Variables
    global leapStatusDisplay
    global piStatusDisplay
    global droneStatusDisplay
    global navData
    global flightmodeDisplay

    #Collect Variables
    battDisplay = str(drone.getBattery()[0])
    yawDisplay = str(drone.NavData["demo"][2][2])
    pitchDisplay = str(drone.NavData["demo"][2][0])
    rollDisplay = str(drone.NavData["demo"][2][1])
    altDisplay = str(drone.NavData["demo"][3])

    # Collect information on the status of the drone
    if drone.State[0] == 0:
        droneStatusDisplay = "Landed "
    elif drone.State[0] == 1:
        droneStatusDisplay = "Flying "
    elif drone.State[31] == 1:
        droneStatusDisplay = "Crashed"

    # Start UI
    screen = curses.initscr()
    curses.cbreak()
    screen.border(0)

	# Top Line Satuses
    screen.addstr(1,1,"Battery: " + battDisplay + "%")
    screen.addstr(1,25,"Leap: " + leapStatusDisplay)
    screen.addstr(1,45,"Pi: " + piStatusDisplay)
    screen.addstr(1,65,"Drone: " + droneStatusDisplay)

	# 4th Line Measurements
    screen.addstr(4,1,"Altitude: " + altDisplay)
    screen.addstr(4,17,"cm")
    screen.addstr(4,60,"Closest Detection: " + "32")
    screen.addstr(4,83,"cm")

	# Roll, Pitch, & Yaw
    screen.addstr(6,1,"Roll: ")
    screen.addstr(6,9,rollDisplay)
    screen.addstr(6,15,"degrees")
    screen.addstr(7,1,"Pitch: ")
    screen.addstr(7,9,pitchDisplay)
    screen.addstr(7,15,"degrees")
    screen.addstr(8,1,"Yaw: ")
    screen.addstr(8,9,yawDisplay)
    screen.addstr(8,15,"degrees")

	# Detection Grid
    screen.addstr(6,60,"###"+"FF"+"###")
    screen.addstr(7,60,"L"+"##"+"UU"+"##"+"R")
    screen.addstr(8,60,"L"+"##"+"DD"+"##"+"R")
    screen.addstr(9,60,"###"+"BB"+"###")

	# Mode Display
    screen.addstr(10,1,"Flight Mode: ")
    screen.addstr(10,15, flightmodeDisplay)

    # Update Screen
    screen.refresh()
    return


# Run the Main Function
if __name__ == "__main__":
    main()
