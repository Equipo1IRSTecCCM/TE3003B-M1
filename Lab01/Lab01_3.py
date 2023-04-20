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
Pregunta 3. Replicar con multiples camaras usando concatenación de imágenes
            - Usar un hilo para la captura de dos camaras y unirlas en una sola imagen
            - Usar un hilo para el procesamiento de la imagen de las dos imágenes unidas (proponer el método)
            - Usar un hilo para mostrar la captura de ambas camaras en una sola imagen
Se usó como base el código generado por David Christopher Balderas Silva
'''
from threading import Thread
import threading
from video_classes import IterPerSec
from video_classes import putIterationsPerSec
from video_classes import VideoGet
from video_classes import VideoShow
from video_classes import VideoGet_2
from video_classes import check_cameras

# Modifies the frames
class thread_show:
    def __init__(self,source):
        #Call the modifed video getter
        self.video_getter = VideoGet_2(source).start()
        (self.grabbed, self.frame) = (self.video_getter.grabbed, self.video_getter.frame)
        self.video_shower = VideoShow(self.frame).start()
        self.itps = IterPerSec().start()
    def start(self):
        Thread(target=self.run, args=()).start()
        return self
    def run(self):
        while True:
            (self.grabbed, self.frame) = (self.video_getter.grabbed, self.video_getter.frame)
            #Stop when needed
            if not self.grabbed or self.video_shower.stopped:
                self.video_shower.stop() 
                self.video_getter.stop()
                break
            #Modify the frame
            self.frame = putIterationsPerSec(self.frame, self.itps.itPerSec())
            self.video_shower.frame = self.frame
            self.itps.increment()
        #Print final Itereations per second
        print("Iterations per second: {}".format(self.itps.itPerSec()))
    

def main():
    source = check_cameras()
    if len(source) >= 2:
        source = [source[0], source[1]]
        #Modify thread that calls the othe ones
        thread_show(source).start()
        #Display active threads
        print("Current Threads:")
        for t in threading.enumerate():
            print('\tThread {}'.format( t.name)) 
    else:
        raise Exception("You need two cameras to run this program, found = {}".format(len(source)))
if __name__ == "__main__":
    main()