################################################################################
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import sys
sys.path.insert(0, "../lib/leap")
import Leap, sys, thread, time

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
                print "Closed Hand"
            else:
    	        # Get the hand's normal vector and direction
    	        normal = hand.palm_normal
    	        direction = hand.direction

    	        # Calculate the hand's pitch, roll, and yaw angles as well as height above sensor
    	        print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees, height: %f mm" % (
    	            ((direction.pitch * Leap.RAD_TO_DEG)-(-180))*(1--1)/(180--180)+(-1),
    	            normal.roll * Leap.RAD_TO_DEG,
    	            direction.yaw * Leap.RAD_TO_DEG,
    	            hand.palm_position.y)


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
