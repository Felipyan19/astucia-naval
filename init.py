import multiprocessing 
from servidor1 import server1
from servidor2 import server2

if __name__ == "__main__":
    # Crear dos procesos para ejecutar los servidores
    process1 = multiprocessing.Process(target=server1)
    process2 = multiprocessing.Process(target=server2)

    # Iniciar los procesos
    process1.start()
    process2.start()

    # Esperar a que los procesos terminen (esto no debería ocurrir en este caso)
    process1.join()
    process2.join()