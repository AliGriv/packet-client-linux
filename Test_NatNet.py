from NatNetClient       import NatNetClient
from threading          import Thread
from threading          import Event

import struct
import time
import numpy as np


# This is a callback function that gets connected to the NatNet client and called once per mocap frame.
def receiveNewFrame(frameNumber, markerSetCount, unlabeledMarkersCount, rigidBodyCount, skeletonCount,
                    labeledMarkerCount, latency, timecode, timecodeSub, timestamp, isRecording, trackedModelsChanged):
    pass


# This is a callback function that gets connected to the NatNet client. It is called once per rigid body per frame
def receiveRigidBodyFrame(frameID, pos, orient,
                          trackingValid):  # NOTE: assign 4 markers to the leader(#1), 5 to copter number 2, 6 to copter number 3, and so on!
    global positions, orientations, trackingFlags, numCopters
    global payloadPose
    if (frameID == 3):
        print("frameID == 3")
        payloadPose = [pos[0], -pos[2], pos[1], orient[0], orient[1], orient[2], orient[3]]
    else:
        index = frameID - 4
        tempPos = [pos[0], -pos[2], pos[1]]  # To transform the camera frame to the inertial frame
        positions[index] = tempPos
        orientations[index] = orient
        trackingFlags[index] = trackingValid
        optitrackThread.callCounter += 1
        if (optitrackThread.callCounter % numCopters == 0):
            event.set()
    print(payloadPose)


if __name__ == "__main__":
    event = Event()  # Event object to sync the main thread and the optitrack thread
    # To run in the optitrackThread
    optitrackThread = NatNetClient(ver=(2, 9, 0, 0), quiet=False)  # This will create a new NatNet client to connect to motive
    optitrackThread.newFrameListener = receiveNewFrame  # Configure the streaming client to call our rigid body handler on the emulator to send data out.
    optitrackThread.rigidBodyListener = receiveRigidBodyFrame
    optitrackThread.run()
