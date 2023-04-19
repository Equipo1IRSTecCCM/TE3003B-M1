import cv2
import time
from video_classes import IterPerSec
from video_classes import putIterationsPerSec
from video_classes import VideoGet
from video_classes import VideoShow

# Dedicated thread for showing video frames with VideoShow object.
# Main thread grabs video frames.
def threadVideoShow(source=0):

    
    video_getter = VideoGet(source).start()
    (grabbed, frame) = (video_getter.grabbed, video_getter.frame)
    video_shower = VideoShow(frame).start()
    itps = IterPerSec().start()

    while True:
        (grabbed, frame) = (video_getter.grabbed, video_getter.frame)
        if not grabbed or video_shower.stopped:
            video_shower.stop() 
            break

        frame = putIterationsPerSec(frame, itps.itPerSec())
        video_shower.frame = frame
        itps.increment()

    print( itps.itPerSec() )

def main():
    source = 0 # 'video_recording.avi'
    threadVideoShow(source)

if __name__ == "__main__":
    main()
