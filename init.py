import multiprocessing 
from servidor1 import server1
from servidor2 import server2
from servidor3 import server3

if __name__ == "__main__":

    process1 = multiprocessing.Process(target=server1)
    process2 = multiprocessing.Process(target=server2)
    process3 = multiprocessing.Process(target=server3)

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()