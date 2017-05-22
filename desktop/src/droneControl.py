################################################################################
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

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
#while(drone.getBattery()[0]==-1): time.sleep(0.1)
#print "Battery: " + str(drone.getBattery()[0] + str(drone.getBattery()[1])
#if drone.getBattery()[1] == "empty": sys.exit()

drone.useDemoMode(True)
drone.getNDpackage(["demo"])
time.sleep(0.5)

# Recalibrate Sensors
drone.trim()
drone.getSelfRotation(5)

##### Mainprogram begin #####
drone.setConfigAllID()                                       # Go to multiconfiguration-mode
drone.sdVideo()                                              # Choose lower resolution (hdVideo() for...well, guess it)
drone.frontCam()                                             # Choose front view
CDC = drone.ConfigDataCount
while CDC == drone.ConfigDataCount:       time.sleep(0.0001) # Wait until it is done (after resync is done)
drone.startVideo()                                           # Start video-function
drone.showVideo()                                            # Display the video


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

        # Get hands
        for hand in frame.hands:

			# Identify which hand is being detected
            handType = "Left hand" if hand.is_left else "Right hand"                
			

            strength = hand.grab_strength
            if strength > 0.99:
                # Land
                drone.land()
                drone.stop()
                print "Closed Hand"
            else:
                print "Open Hand"
                # Take off and wait for it to properly settle
                drone.takeoff()
                #while drone.NavData["demo"][0][2]: time.sleep(0.1)
                                
    	        # Get the hand's normal vector and direction
    	        normal = hand.palm_normal
    	        direction = hand.direction

    	        # Calculate the hand's pitch, roll, and yaw angles as well as height above sensor
                pitch_raw = direction.pitch * Leap.RAD_TO_DEG
                roll_raw = normal.roll * Leap.RAD_TO_DEG
                yaw_raw = direction.yaw * Leap.RAD_TO_DEG
                thrust_raw = hand.palm_position.y

                # Map values to between -1 and 1
                pitch = (-pitch_raw-(-180)) * (1--1) / (180--180) + (-1)
                roll = (-roll_raw-(-180)) * (1--1) / (180--180) + (-1)
                yaw = (yaw_raw-(-180)) * (1--1) / (180--180) + (-1)
                thrust = (thrust_raw-(50)) * (1--1) / (500-50) + (-1)
                
                # Do the movement
                drone.move(roll, pitch, thrust, yaw)


def main():

    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()


