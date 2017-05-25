################################################################################
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

#import cv2
#import getch
import sys
sys.path.insert(0, "../lib/leap")
import Leap, thread, time
sys.path.insert(0, "../lib/psdrone")
import ps_drone


# Configure & Connect to Drone
drone = ps_drone.Drone()
drone.startup()
drone.reset()

# Get Drone Battery Level
while(drone.getBattery()[0]==-1): time.sleep(0.1)
print "Battery: "+str(drone.getBattery()[0])+"% "+str(drone.getBattery()[1])
if drone.getBattery()[1] == "empty": sys.exit()

drone.useDemoMode(True)
drone.getNDpackage(["demo"])
time.sleep(0.5)

# Recalibrate Sensors
drone.trim()
drone.getSelfRotation(5)

##### Mainprogram begin #####
#drone.setConfigAllID()                                       # Go to multiconfiguration-mode
##drone.sdVideo()                                              # Choose lower resolution (hdVideo() for...well, guess it)
#drone.frontCam()                                             # Choose front view
#CDC = drone.ConfigDataCount
#while CDC == drone.ConfigDataCount:       time.sleep(0.0001) # Wait until it is done (after resync is done)
#drone.startVideo()                                           # Start video-function
#drone.showVideo()                                            # Display the video

# Global Variables from Leap Input
handClosed = True
handRoll = 0
handPitch = 0
handYaw = 0
handLevel = 0
handCount = 0
landed = True

# Leap Motion Listener
class SampleListener(Leap.Listener):

    # Debug information for leap connectivity
    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    # When a new frame is detected
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

    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    print "Press Enter to quit..."

    while 1:
        #if msvcrt.kbhit():
	    #if ord(msvcrt.getch()) == 27:
                #sys.exit()

        dronecontrolling()


def dronecontrolling():
    global landed
    global drone
    print "incontrol"
    if (handClosed and not landed) or (handCount < 1 and not landed):
        drone.land()
        drone.stop()
        print "Land"
        landed = True
    elif not handClosed and landed and handCount > 0:
        drone.takeoff()
        print "Take Off"
        landed = False

    rollVal = mapVals(-handRoll * Leap.RAD_TO_DEG, -100, 100, -1, 1 )
    pitchVal = mapVals(-handPitch * Leap.RAD_TO_DEG, -100, 100, -1, 1)
    yawVal = mapVals(handYaw * Leap.RAD_TO_DEG, -100, 100, -1, 1)
    thrustVal = mapVals(handLevel, 100, 400, -1, 1)

    # Cap Values at 1 and -1


    rollVal = capVals(rollVal)
    pitchVal = capVals(pitchVal)
    yawVal = capVals(yawVal)
    thrustVal = capVals(thrustVal)
    print pitchVal
    drone.move(rollVal, pitchVal, thrustVal, yawVal)
    return


def mapVals(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def capVals(val):
    if val is None:
	val = 0

    if val > 1:
        return 1
    elif val < -1:
        return -1
    else:
        return val


if __name__ == "__main__":
    main()


