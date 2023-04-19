import cv2
import time
from threading import Thread
from video_classes import IterPerSec
from video_classes import putIterationsPerSec
from video_classes import VideoGet
from video_classes2 import VideoShow

# Dedicated thread for showing video frames with VideoShow object.
# Main thread grabs video frames.
class thread_show:
    def __init__(self,source):
        self.video_getter = VideoGet(source).start()
        (self.grabbed, self.frame) = (self.video_getter.grabbed, self.video_getter.frame)
        self.video_shower = VideoShow(self.frame,str(source)).start()
        self.itps = IterPerSec().start()
    def start(self):
        Thread(target=self.run, args=()).start()
        return self
    def run(self):
        while True:
            (self.grabbed, self.frame) = (self.video_getter.grabbed, self.video_getter.frame)
            if not self.grabbed or self.video_shower.stopped:
                self.video_shower.stop() 
                break

            self.frame = putIterationsPerSec(self.frame, self.itps.itPerSec())
            self.video_shower.frame = self.frame
            self.itps.increment()

        print( self.itps.itPerSec() )
    

def main():
    source = 2 # 'video_recording.avi'
    thread_show(source).start()
    source = 0
    thread_show(source).start()
if __name__ == "__main__":
    main()
