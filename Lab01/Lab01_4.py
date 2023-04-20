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
Pregunta 4. Replicar con multiples camaras usando un hilo por cada una de las imágenes
            - Usar un primer hilo para la captura de una camara
            - Usar un segundo hilo para la captura de una camara
            - Usar un tercer hilo para el procesamiento de la imagen de la primera camara
            - Usar un cuarto hilo para el procesamiento de la imagen de la segunda camara
            - Usar un quinto hilo para mostrar la captura de la primera camara
            - Usar un sexto hilo para mostrar la captura de la segunda camara
Se usó como base el código generado por David Christopher Balderas Silva
'''
from threading import Thread
import threading
from video_classes import IterPerSec
from video_classes import putIterationsPerSec
from video_classes import VideoGet
from video_classes import VideoShow
from video_classes import check_cameras

#Modify the frame
class thread_show:
    def __init__(self,source):
        #Call a set of threads per camera
        #A more iterative solution was proposed, but ultimately, failed
        self.video_getter0 = VideoGet(source[0]).start()
        self.video_getter1 = VideoGet(source[1]).start()
        (self.grabbed, self.frame1, self.frame2) = (self.video_getter0.grabbed and self.video_getter1.grabbed, self.video_getter0.frame, self.video_getter1.frame)
        self.video_shower0 = VideoShow(self.frame1, name="Video {}".format(source[0])).start()
        self.video_shower1 = VideoShow(self.frame2, name="Video {}".format(source[1])).start()
        self.itps0 = IterPerSec().start()
        self.itps1 = IterPerSec().start()
        
    def start(self):
        #Call the two modify threads
        Thread(target=self.run, args=(True,)).start()
        Thread(target=self.run, args=(False,)).start()
        return self
    def run(self,camera_toggle):
        #Select which camera to use
        if camera_toggle:
            video_get = self.video_getter0
            video_show = self.video_shower0
            fps_counter = self.itps0
        else:
            video_get = self.video_getter1
            video_show = self.video_shower1
            fps_counter = self.itps1
        while True:
            (grabbed_local, frame_local) = (video_get.grabbed, video_get.frame)
            #Stop when needed
            if not grabbed_local or video_show.stopped:
                self.video_shower0.stop() 
                self.video_shower1.stop() 
                self.video_getter0.stop()
                self.video_getter1.stop()
                break
            #Modify frame
            frame_local = putIterationsPerSec(frame_local, fps_counter.itPerSec())
            video_show.frame = frame_local
            fps_counter.increment()
        #Print final Itereations per second
        print("Iterations per second of {}: {}".format(self.video_shower0.name,self.itps0.itPerSec()))
        print("Iterations per second of {}: {}".format(self.video_shower1.name,self.itps1.itPerSec()))
        
    

def main():
    source = check_cameras()
    if len(source) >= 2:
        source = [source[0], source[1]]
        #Call the class that manages the threads
        thread_show(source).start()
        #Display current threads
        print("Current Threads:")
        for t in threading.enumerate():
            print('\tThread {}'.format( t.name)) 
    else:
        raise Exception("You need two cameras to run this program, found = {}".format(len(source)))

if __name__ == "__main__":
    main()