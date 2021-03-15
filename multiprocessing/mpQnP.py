import multiprocessing
import time
import random

def sd(con,q):
    while True:
        n = "ping"                        #choose 6 as our number
        if (n == "ping"):
            q.put(time.perf_counter())
            n2 = random.random() 
            time.sleep(n2)
        con[0].send(n)                  #send the number into the pipe
        time.sleep(5)                   #wait 5s
       
       
def ud(con,q):
    while True:
        recieved = con[1].recv()        #once something is in the pipe, store it in recieved
        if (recieved == "ping"):
            q.put(time.perf_counter())
        

if __name__ == "__main__":
   
    # creating a pipe
    sd_conn, ud_conn = multiprocessing.Pipe()
   
    #establishing connections in pipes
    connections = [sd_conn, ud_conn] #renaming for easier use of pipes
   
    qTime = multiprocessing.Queue()
   
   
    p1 = multiprocessing.Process(target=sd, args=(connections,qTime))
    p2 = multiprocessing.Process(target=ud, args=(connections,qTime))
   
    p1.start()
    p2.start()
    time.sleep(1)
    while 1:
        while qTime.empty() is False:
           t1 = qTime.get()
           t2 = qTime.get()
           tOut = t2-t1
           print("that ping took", tOut)            
        time.sleep(0.1)
        