import cv2 #importamos opencv
from timeit import timeit
from multiprocessing import Process, Pipe, Lock
import time

def caputarar_video(conn1_child,conn2_parent,l):

    """
        Metodo que crea un proceso que captura el trafico de manera sincrona (Lock).
        input:
            conn1_child: conexion de la pipe entre hijos
            conn2_parent: conexion de la pipe con el padre
            l: objeto de tipo bloque, para bloquear el proceso y que sea sincrono
    """
    l.acquire()
    try:
        cap = cv2.VideoCapture(0) #instnca un objeto de video (0 seleciona cam principal, se pude ponere IP, ruta,... )
        while(True): 
            ret, frame = cap.read() 
            #envio el video frame a frame y ret 
            conn1_child.send([ret, frame])
            res_padre=conn2_parent.recv()
            if(res_padre=='q'):
                break
        cap.release() #deja de ocupar los recurso de la webcam
    except Exception as error:
        print(error)
    finally:
        l.release()

def pintar_imagen(conn1_child,conn2_parent,l):

    """
        Metodo que crea un proceso que pinta los frames con figuara de manera sincrona (Lock).
        input:
            conn1_child: conexion de la pipe entre hijos
            conn2_parent: conexion de la pipe con el padre
            l: objeto de tipo bloque, para bloquear el proceso y que sea sincrono
    """

    l.acquire()
    try:
        while(True): 
            frame= conn1_child.recv()[1] #recibo de hijo los frames
            imagen = cv2.rectangle(frame, (100, 100), (200, 200), (255, 0, 0), 2)
            #envio al padre el frame ya pintado
            conn2_parent.send(imagen)
            res_padre=conn2_parent.recv()
            if(res_padre=='q'):
                break   

    except Exception as error:
        print(error)
    finally:
        l.release()

if __name__ == '__main__':
    """
        Main que crea al proceso padre, muestra las imagenes. Gesiona el inicio 
        y el final del los procesos. Se crean 3 tuberias: 1º tuberia es la comunicacion
        entre porocesos hijos (pasa los frames a otro hijo) y las 2 restantes son la 
        comunicacion de cada hijo con el padre.   
    """
    #Pipes para la comunicación 
    child1_conn1, child2_conn1 = Pipe() 
    parent_conn2, child1_conn2 = Pipe()
    parent_conn3, child2_conn3 = Pipe()

    #semaforos para cada uno de los procesos 
    child1_lock = Lock() 
    child2_lock = Lock() 
    parent_lock= Lock()

    #creo los procesos hijos y los incio
    p1 = Process(target=caputarar_video, args=(child1_conn1, child1_conn2, child1_lock)) #instancio el proceso hijo
    p1.start() 

    p2 = Process(target=pintar_imagen, args=(child2_conn1, child2_conn3, child2_lock)) #instancio el proceso hijo
    p2.start() 
    
  
    parent_lock.acquire() #bloque el proceso con semaforo del padre
    try:
        while(True):
            parent_conn2.send('r1')
            parent_conn3.send('r2') 
            imagen= parent_conn3.recv()
            # pinto el frame resultante en pantalla 
            cv2.imshow('webcam', imagen)
            if cv2.waitKey(1) & 0xFF == ord('q'): #cv2.waitKey(1) una espera 1ms para pasar al sigueinte frame. Si pulso q exit
                    parent_conn2.send('q') #envia por la tuberia una q para terminar los procesos hijos
                    break
        #termino los preocesos hijos            
        p1.terminate() 
        p2.terminate() 
        #espero a que finalicen los hijos      
        p1.join() 
        p2.join() 
        cv2.destroyAllWindows() #cierro el programa actual y libero memoria

    except Exception as error:
        print(error)
    finally:
        parent_lock.release() #desbloque el proceso con semaforo del padre
