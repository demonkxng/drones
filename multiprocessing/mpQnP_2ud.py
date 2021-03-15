import multiprocessing
import time
import random
import os

def sd(con_grid, q, sqid, idq):
    sqid.put(os.getpid())
    while True:
        for i in range(len(con_grid)):                  #loop through each connection in the grid
            n = "ping"                              #choose ping as input
            if (n == "ping"):                   
                q.put(time.perf_counter())          #log time in qTime
                time.sleep(random.random())         #wait 0-1s
            con_grid[i][0].send(n)                  #send the number into the pipe for each connection in the grid
            idq.put(os.getpid())
            time.sleep(2)                           #wait 2s
        time.sleep(5)                               #wait 5s
       
def ud(con, q, uqid, idq):
    uqid.put(os.getpid())
    while True:
        recieved = con[1].recv()        #once something is in the pipe, store it in recieved
        if (recieved == "ping"):
            q.put(time.perf_counter())
            idq.put(os.getpid())
        

if __name__ == "__main__":
   
    # creating a pipe
    sd_conn, ud_conn = multiprocessing.Pipe()
    sd_conn2, ud_conn2 = multiprocessing.Pipe()
   
    #establishing connections in pipes
    connections = [sd_conn, ud_conn] #renaming for easier use of pipes
    connections2 = [sd_conn2, ud_conn2]
   
    #building an array of connection arrays
    sd_connections_grid = []
    sd_connections_grid.append(connections)
    sd_connections_grid.append(connections2)
    
    #test that 4 different connections are created
    for i in range(len(sd_connections_grid)):
        for j in range(len(sd_connections_grid[i])):
            print ("pipe",i, "connection",j, sd_connections_grid[i][j])
    
    #build queues for different purposes
    qTime = multiprocessing.Queue()     #transmitting times
    sdq = multiprocessing.Queue()       #transmitting SD IDs
    udq = multiprocessing.Queue()       #transmitting UD IDs
    idq = multiprocessing.Queue()       #storage for IDs to be used in printer in server
   
    #declare our processes
    p1 = multiprocessing.Process(target=sd, args=(sd_connections_grid, qTime, sdq, idq))
    p2 = multiprocessing.Process(target=ud, args=(connections, qTime, udq, idq))
    p3 = multiprocessing.Process(target=ud, args=(connections2, qTime, udq, idq))
   
    #start processes
    p1.start()
    p2.start()
    p3.start()
    
    #wait for 2 sec
    time.sleep(2)
    
    #initialize vars for storage/tracking
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
        while (qTime.empty() is False) and (idq.empty() is False):
           t1 = qTime.get()
           id1 = idq.get()
           t2 = qTime.get()
           id2 = idq.get()
           tOut = t2-t1
           print("ping from", id1, "to ", id2, "took ",tOut,"seconds")    
           
        time.sleep(.1)
        
        if (ctr%50==0):
            for i in range(ud_len):
                print("UD#",i,", ID:",ud_ids[i])
            for i in range(sd_len):
                print("SD#",i,", ID:",sd_ids[i])
                