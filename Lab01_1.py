import cv2
from video_classes import IterPerSec
from video_classes import putIterationsPerSec

from video_classes import VideoGet

# Dedicated thread for grabbing video frames with VideoGet object.
# Main thread shows video frames.
def threadVideoGet(source=0):
    video_getter = VideoGet(source).start()
    itps = IterPerSec().start()

    while True:
        if (cv2.waitKey(1) == ord("q")) or video_getter.stopped:
            video_getter.stop()
            break

        frame = video_getter.frame
        frame = putIterationsPerSec(frame, itps.itPerSec())
        cv2.imshow("Video", frame)
        itps.increment()

    print( itps.itPerSec() )

def main():
    source = 0 # 'video_recording.avi'
    threadVideoGet(source)

if __name__ == "__main__":
    main()
