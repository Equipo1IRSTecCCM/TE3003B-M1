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
Pregunta 2. Crear una programa que capture imágenes de una camara usando hilos 
            - Usar un hilo para la captura de una camara
            - Usar un hilo para el procesamiento de la imagen de una camara (proponer el método)
            - Usar un hilo para mostrar la captura de una camera
Se usó como base el código generado por David Christopher Balderas Silva
'''

import threading
from video_classes import IterPerSec
from video_classes import putIterationsPerSec
from video_classes import VideoGet
from video_classes import VideoShow

# Modifies the frames
def modify(source=0):
    #Summon my threads
    video_getter = VideoGet(source).start()
    (grabbed, frame) = (video_getter.grabbed, video_getter.frame)
    video_shower = VideoShow(frame).start()
    itps = IterPerSec().start()
    #Display active threads
    print("Current Threads:")
    for t in threading.enumerate():
        print('\tThread {}'.format( t.name))

    while True:
        (grabbed, frame) = (video_getter.grabbed, video_getter.frame)
        #Stop when needed
        if not grabbed or video_shower.stopped:
            video_shower.stop() 
            video_getter.stop()
            break
        #Modify frame
        frame = putIterationsPerSec(frame, itps.itPerSec())
        video_shower.frame = frame
        itps.increment()
    #Print final Itereations per second
    print("Iterations per second: {}".format(itps.itPerSec()))

def main():
    source = 0
    #Start the modify thread that'll call the other ones
    threading.Thread(target = modify, args=(source,)).start()

if __name__ == "__main__":
    main()
