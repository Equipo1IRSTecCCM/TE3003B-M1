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
Pregunta 1. Crear una programa que capture imágenes de una camara usando hilos
        - Capturar la imagen de una camara
        - Procesamiento de la imagen una camara (proponer el método)
        - Mostrar la captura de una camera
Se usó como base el código generado por David Christopher Balderas Silva
'''

import cv2
import threading
from video_classes import IterPerSec
from video_classes import putIterationsPerSec
from video_classes import VideoGet

# Modifies the frames
def threadVideoGet(source=0):
    video_getter = VideoGet(source).start()
    itps = IterPerSec().start()
    #Print current Threads
    print("Current Threads:")
    for t in threading.enumerate():
        print('\tThread {}'.format( t.name)) 

    while True:
        #Stop when asked to
        if (cv2.waitKey(1) == ord("q")) or video_getter.stopped:
            video_getter.stop()
            break
        #Update frame
        frame = video_getter.frame
        frame = putIterationsPerSec(frame, itps.itPerSec())
        cv2.imshow("Video", frame)
        itps.increment()
    #Print final Itereations per second
    print("Iterations per second: {}".format(itps.itPerSec()))

def main():
    source = 0
    threadVideoGet(source)

if __name__ == "__main__":
    main()
