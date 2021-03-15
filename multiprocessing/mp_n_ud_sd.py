import multiprocessing
import time
import random
import os

def sd(sd_pipes, q, sqid):
    sqid.put(os.getpid())                           # save the PID in sqid
    while True:
        for i in range(len(sd_pipes)):                  #loop through each connection in the grid
            #writing to UD                 
            t1 = time.perf_counter()                #log time in t1
            time.sleep(random.random())             #wait 0-1s
            my_data = [t1]
            sd_pipes[i][0].send(my_data)              #send the timestamp into the pipe for each connection in the grid
            #idq.put(os.getpid())                    #stores the PID in the id queue
            time.sleep(.1)                           #wait .5s
            
            #reading
            my_data = sd_pipes[i][1].recv()     # recieve data from UD
            my_data.append(os.getpid())         #store SD PID at the end of data
            
            #write to main
            q.put(my_data)                      #sends back to main
            time.sleep(1)
        
        time.sleep(1)                               #wait 5s
       
def ud(ud_pipes, uqid):
    #stores the PID for the UD
    uqid.put(os.getpid())
    concat_data = []
    while True:
        for i in range (len(ud_pipes)):             #check all SD connections for input
            #reading & internal logic
            t1 = ud_pipes[i][1].recv()              #once something is in the pipe, store it in t1
            t1 = int(t1[0])
            t2 = time.perf_counter()                #record the current timestamp
            tout = t2-t1               #subtract the first timestamp from the second, storing in data
            time.sleep(0.1)
            #concat_data.append(os.getpid())         # store the id in the data          
            concat_data = [tout, os.getpid()]
            #writing back
            ud_pipes[i][0].send(concat_data)       #send the timestamp and UD PID back
            time.sleep(1)
            
            
            
            
######################################
##### THIS IS THE SERVER PROCESS #####
######################################

if __name__ == "__main__":
   
   #build queues for different purposes
    sdq = multiprocessing.Queue()       #transmitting SD IDs
    udq = multiprocessing.Queue()       #transmitting UD IDs
    #idq = multiprocessing.Queue()       #storage for IDs to be used in printer in server
    
    #a list for all the queues for each SD
    queueGrid = []
   
    #list for storing all UD processes
    ud_processes = []
    sd_processes = []
    
    sd_pipes = []
    ud_pipes = []
    #given that you want i * j pipes,
    userInpSD = 2
    userInpUD = 3
    
    pipeGrid = []
    pipeGridRow = []
    #assemble the 3x4 grid that stores all the connections
    for i in range (userInpSD):     
        pipeGridRow = []                                 # empty pipe grid row
        for j in range (userInpUD):                      #
            sd_conn, ud_conn = multiprocessing.Pipe()    # creating a pipe
            connections = [sd_conn, ud_conn]             # renaming for easier use of pipes
            pipeGridRow.append(connections)              # store each connection in pipeGrid so it can be referenced later.
        pipeGrid.append(pipeGridRow)                     # store the pipe grid row in the pipe grid
   
    #initialize SDs
    for i in range(userInpSD):                           # for each SD, assemble the connection grid
        sd_pipes = []                                    # clear sd_pipes 
        for j in range (userInpUD):                      # loop through the row
            sd_pipes.append(pipeGrid[i][j])              # append the connection in pipeGrid[i][j] to sd_pipes
        qTime = multiprocessing.Queue()                  # storing the transmitting times for each SD
        process = multiprocessing.Process(target=sd, args=(sd_pipes, qTime, sdq))
        sd_processes.append(process)                     # add SD to the sd_processes list
        queueGrid.append(qTime)                          # add qTime to the list of queues
        process.start()                                  # start the process
    
    #initialize UDs
    for i in range(userInpUD):                           # for each UD, assemble the connection grid
        ud_pipes = []                                    # clear sd_pipes
        for j in range (userInpSD):                      # loop through the column
            ud_pipes.append(pipeGrid[j][i])              # append the connection in pipeGrid[j][i] to ud_pipes           
        process = multiprocessing.Process(target=ud, args=(ud_pipes, udq))
        ud_processes.append(process)                     # add UD to the ud_processes list    
        process.start()
              
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
        
        #recieve data from each SD
        for i in range(len(queueGrid)):
            while (queueGrid[i].empty() is False):
                # EVERY DATA THAT IS PULLED OUT OF THE QUEUE IS GOING TO BE [TIME, UD_PID, SD_PID]
                myData = queueGrid[i].get() #store time, ud_pid, sd_pid
                #print("A pin from",myData[2],"to",myData[1],"took",myData[0],"seconds") #print the data
                print(myData)
                time.sleep(.3)
           
        time.sleep(.3)
        
        if (ctr%50==0):
            print("\nList\n")
            for i in range(ud_len):
                print("UD#",i,", ID:",ud_ids[i])
            print("\n")
            for i in range(sd_len):
                print("SD#",i,", ID:",sd_ids[i])
            print("\n")    