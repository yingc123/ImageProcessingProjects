# import the necessary packages
from __future__ import print_function
#from imutils.video.pivideostream import PiVideoStream
from PiVideoStream_stereo import PiVideoStream
from imutils.video import FPS
from stream import Stitcher
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import imutils
import time
import cv2
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=1000,
    help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=-1,
    help="Whether or not frames should be displayed")
args = vars(ap.parse_args())
stitcher = Stitcher()
# created a *threaded *video stream, allow the camera sensor to warmup,
# and start the FPS counter
print("[INFO] sampling THREADED frames from `picamera` module...")
vs = PiVideoStream().start()
time.sleep(2.0)
fps = FPS().start()
# loop over some frames...this time using the threaded stream
while fps._numFrames < args["num_frames"]:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame = vs.read()
    imgLeft = frame[0:480,0:640] #Y+H and X+W
    imgRight = frame[0:480,640:1280]
    result = stitcher.stitch([imgLeft, imgRight])
    if result is None:
        print("[INFO] homography could not be computed")
        break
    #frame = imutils.resize(frame, width=400)
    # check to see if the frame should be displayed to our screen
    #if args["display"] > 0:
    #cv2.imshow("Frame", frame)
    #cv2.imshow("imgLeft", imgLeft)
    #cv2.imshow("imgRight", imgRight)
    cv2.imshow("result", result)
    key = cv2.waitKey(1) & 0xFF
    # update the FPS counter
    fps.update()
# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
