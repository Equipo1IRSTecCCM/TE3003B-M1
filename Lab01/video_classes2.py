from threading import Thread
import cv2
from datetime import datetime
import time

######################################################################
# Add iterations per second text to lower-left corner of a frame.
def putIterationsPerSec(frame, iterations_per_sec):
    cv2.putText(frame, "{:.0f} iterations/sec".format(iterations_per_sec),
        (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
    return frame

######################################################################
# Tracks the number of Frames per Second.
class IterPerSec:
    def __init__(self):
        self._start_time = None
        self._numFrames  = 0

    def start(self):
        self._start_time = datetime.now()
        return self

    def increment(self):
        self._numFrames += 1

    def itPerSec(self):
        elapsed_time = (datetime.now() - self._start_time).total_seconds()
        if elapsed_time != 0:
            return self._numFrames / elapsed_time
        return 0
######################################################################
# Continuously gets frames from a VideoCapture object with a thread.
class VideoGet:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        Thread(target = self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
                self.stream.release()
            else:
                (self.grabbed, self.frame) = self.stream.read()
    
    def stop(self):
        self.stopped = True

######################################################################
# Continuously shows a frame using a thread.
class VideoShow:
    def __init__(self, frame=None, name = "Video"):
        self.frame = frame
        self.stopped = False
        self.name = name

    def start(self):
        Thread(target=self.show, args=()).start()
        return self

    def show(self):
        while not self.stopped:
            cv2.imshow(self.name, self.frame)
            if cv2.waitKey(1) == ord("q"):
                self.stopped = True
            time.sleep(0.1)

    def stop(self):
        self.stopped = True
