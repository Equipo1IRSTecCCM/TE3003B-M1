import cv2
import time
from threading import Thread
from video_classes2 import IterPerSec
from video_classes2 import putIterationsPerSec
from video_classes2 import VideoGet
from video_classes2 import VideoShow

# Dedicated thread for showing video frames with VideoShow object.
# Main thread grabs video frames.
def threadVideoShow(source=[0,2]):

    
    video_getter = VideoGet(source[0]).start()
    (grabbed, frame) = (video_getter.grabbed, video_getter.frame)
    video_shower = VideoShow(frame).start()
    itps = IterPerSec().start()

    video_getter2 = VideoGet(source[1]).start()
    (grabbed2, frame2) = (video_getter2.grabbed, video_getter2.frame)
    video_shower2 = VideoShow(frame2).start()
    itps2 = IterPerSec().start()

    while True:
        (grabbed, frame) = (video_getter.grabbed, video_getter.frame)
        (grabbed2, frame2) = (video_getter2.grabbed, video_getter2.frame)
        if not grabbed or video_shower.stopped or not grabbed2 or video_shower2.stopped:
            video_shower.stop() 
            video_shower2.stop()
            break

        frame = putIterationsPerSec(frame, itps.itPerSec())
        frame2 = putIterationsPerSec(frame2, itps2.itPerSec())
        video_shower.frame = frame
        video_shower2.frame = frame2
        itps.increment()
        itps2.increment()

    print( itps.itPerSec() )

def main():
    source = [0,2] # 'video_recording.avi'
    Thread(target=threadVideoShow, args=(source,)).start()
    

if __name__ == "__main__":
    main()
