'''
TE3003B Integración de robótica y sistemas inteligentes
M1. Tecnologías Emergentes
Lab 01

Equipo 3.
    Diego Reyna Reyes               A01657387
    Jorge Antonio Hoyo García       A01658142
    Samantha Barrón Martínez        A01652135
    Jorge Gerardo Iglesias Ortiz    A01653261
20/04/2023, CDMX, México 

Descripción:
Este archivo contiene las clases necesarias para 
hacer funcionar la solución para los 4 incisos de 
esta actividad

Se usó como base el código generado por David Christopher 
Balderas Silva, todas las modificaciones realizadas están marcadas por el comentario # (Mod)
'''
from threading import Thread
import cv2
from datetime import datetime

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
        self.name = name # (Mod) Include a name to have an unique name in the cv2 window

    def start(self):
        Thread(target=self.show, args=()).start()
        return self

    def show(self):
        while not self.stopped:
            cv2.imshow(self.name, self.frame) # (Mod) Show the saved name
            if cv2.waitKey(1) == ord("q"):
                self.stopped = True

    def stop(self):
        self.stopped = True

######################################################################
# (Mod) Captures video from two cameras and concatenates them
class VideoGet_2(VideoGet):
    def __init__(self, src=[0,2]):
        # (Mod) Create a two of each of the elemnts on the base VideoGet
        self.stream = cv2.VideoCapture(src[0])
        self.stream2 = cv2.VideoCapture(src[1])
        (self.grabbed1, self.frame1) = self.stream.read()
        (self.grabbed2, self.frame2) = self.stream2.read()
        self.grabbed = True
        self.stopped = False
        self.frame = self.frame1

    def start(self):
        Thread(target = self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            self.grabbed = self.grabbed1 and self.grabbed2 # (Mod) If one camera fails to grab, both will stop
            if not self.grabbed:
                self.stop()
                self.stream.release()
            else:
                # (Mod) Get both images
                (self.grabbed1, self.frame1) = self.stream.read()
                (self.grabbed2, self.frame2) = self.stream2.read()
                self.concat()
    def concat(self):
        # (Mod) Resize the bigger image so it's the same size as the smaller one
        if self.frame1.shape[0] > self.frame2.shape[0]:
            self.frame1 = cv2.resize(self.frame1, (int(self.frame1.shape[1] * self.frame2.shape[0] / self.frame1.shape[0]), self.frame2.shape[0]), interpolation=cv2.INTER_CUBIC)
        else:
            self.frame2 = cv2.resize(self.frame2, (int(self.frame2.shape[1] * self.frame1.shape[0] / self.frame2.shape[0]), self.frame1.shape[0]), interpolation=cv2.INTER_CUBIC)
        # (Mod) Concatenate
        self.frame = cv2.hconcat([self.frame1,self.frame2])
    def stop(self):
        self.stopped = True