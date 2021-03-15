import multiprocessing
import time
import random
import os

def sd(con, q, sqid):
    sqid.put(os.getpid())
    while True:
        n = "ping"                        #choose 6 as our number
        if (n == "ping"):
            q.put(time.perf_counter())
            n2 = random.random() 
            time.sleep(n2)
        con[0].send(n)                  #send the number into the pipe
        time.sleep(5)                   #wait 5s
       
       
def ud(con, q, uqid):
    uqid.put(os.getpid())
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
    sdq = multiprocessing.Queue()
    udq = multiprocessing.Queue()
   
   
    p1 = multiprocessing.Process(target=sd, args=(connections,qTime, sdq))
    p2 = multiprocessing.Process(target=ud, args=(connections,qTime, udq))
   
    p1.start()
    p2.start()
    time.sleep(2)
    
    sd_ids = []
    sd_len = 0
    ud_ids = []
    ud_len = 0
    ctr = 0;
    while 1:
        #print("yea")
        ctr+=1
        #store all sd IDs and increment counter
        while sdq.empty() is False:
            sd_ids.append(sdq.get())
            sd_len=+1
            
        
        # store all ud IDs and increment counter
        while udq.empty() is False:
            ud_ids.append(udq.get())   
            ud_len+=1
        
        #check out timestamps
        while qTime.empty() is False:
           t1 = qTime.get()
           t2 = qTime.get()
           tOut = t2-t1
           print("that ping took", tOut)     
           
        time.sleep(.1)
        
        if (ctr%50==0):
            for i in range(ud_len):
                print("UD#",i,", ID:",ud_ids[i])
            for i in range(sd_len):
                print("SD#",i,", ID:",sd_ids[i])
                