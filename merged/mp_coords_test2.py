import multiprocessing
import time
import random
import os
import math

def sd(sd_pipes, sd_pipes2, q, sqid):
    x=random.randrange(100)+1
    y=random.randrange(100)+1
    z=0
    pos = [x,y,z,os.getpid()]
    sqid.put(pos)                       #sends SD coords and PID to main
    print ("SD#",os.getpid(), "located at (x,y,z):",x,y,z)
    while True:
        for i in range(len(sd_pipes)):                  #loop through each connection in the grid
            #writing to UD                 
            #t1 = time.perf_counter()                #log time in t1
            #time.sleep(random.random())             #wait 0-1s
            my_data = [os.getpid()]
            sd_pipes[i][0].send(my_data)              #send the timestamp into the pipe for each connection in the grid
            #idq.put(os.getpid())                    #stores the PID in the id queue
            time.sleep(.1)                           #wait .5s
            
            # while (sd_pipes[i][0] != None):   #wait until the pipe is empty
            #     pass
            # print("SD#",os.getpid(), "entered top")
            #reading back 
            my_data = sd_pipes2[i][1].recv()     # recieve data from UD
            #ud_pid = my_data[1]
            x2=pow((x-my_data[2]),2)
            y2=pow((y-my_data[3]),2)
            #z2=pow((z-my_data[4]),2)
            distance = math.sqrt(x2+y2)   
            my_data.pop(3)      
            my_data.pop(2)
            my_data.append(distance)            #distance to surface xy
            # print("SD#",os.getpid(), "entered bot",my_data)
            
            #write to main
            q.put(my_data)                      #sends back to main
            time.sleep(1)
        
        time.sleep(1)                               #wait 5s
       
def ud(ud_pipes, ud_pipes2, uqid):
    #stores the PID for the UD
    concat_data = []
    x=random.randrange(100)+1
    y=random.randrange(100)+1
    z=-(random.randrange(90)+10)
    
    udData = [os.getpid(), z]
    uqid.put(udData)
    
    print ("UD#",os.getpid(), "located at (x,y,z):",x,y,z)
    while True:
        for i in range (len(ud_pipes)):             #check all SD connections for input
            #reading & internal logic
            concat_data = ud_pipes[i][1].recv()          #once something is in the pipe, store it in t1
            concat_data.append(os.getpid())         # store the id in the data
            concat_data.append(x)
            concat_data.append(y)
            #print("IN UD",concat_data)
            #writing back
            ud_pipes2[i][0].send(concat_data)       #send the timestamp and UD PID back
            # print("UD#",os.getpid(), "entered loop")
            time.sleep(1)

######################################            
####### THIS IS JUST A FUNCTION ######
######################################

def calcSDdistance(xGrid,yGrid, i1, i2): #i1, i2 are indices // xGrid,yGrid,zGrid are positions of SDs where each index is 1 SD
    xdif=pow(xGrid[i1]-xGrid[i2], 2)
    ydif=pow(yGrid[i1]-yGrid[i2], 2)
    distance = math.sqrt(xdif+ydif)
    return distance

def assembleSDdGrid(sdx,sdy,sdz,i1,i2,i3):
    s1 = calcSDdistance(sdx,sdy,sdz, i1, i2)
    s2 = calcSDdistance(sdx,sdy,sdz, i1, i3)
    s3 = calcSDdistance(sdx,sdy,sdz, i2, i3)
    SDdGrid= [s1,s2,s3]
    return SDdGrid

def GPSfunc(dGrid, sd_coords, ud_pid, sd_pids):
    global sd_ids, ud_zpos, ud_ids
    
    myDistances = []
    [sd_xpos, sd_ypos, sd_zpos] = sd_coords
    A = []
    B = []
    i=0
    #finds the origin point
    for i in range(len(sd_ids)):
        if (sd_ids[i]==sd_pids[0]):         #REFER TO THIS SD AS "A"
            A.append(sd_xpos[i])       #x offset
            A.append(sd_ypos[i])       #y offset
            myDistances.append(dGrid[0])    #AC
            break
    #find the j value of 
    j=0
    for j in range(len(sd_ids)):            
        if (sd_ids[j]==sd_pids[1]):         #REFER TO THIS SD AS "B"
            B.append(sd_xpos[j])       #x offset
            B.append(sd_ypos[j])       #y offset
            myDistances.append(dGrid[1])    #BC
            break
        
    myDistances.append(calcSDdistance(sd_xpos, sd_ypos, i, j)) #this is AB
    #decompile myDistances into AC BC AB
    print("AC BC AB",myDistances)
    [AC, BC, AB] = myDistances
    Cy = pow(AB,2)+pow(AC,2)-pow(BC,2)
    Cy /= (2*AB)
    Cx = math.sqrt(pow(AC,2)-pow(Cy,2))
    print("pre adjusted: (Cx,Cy)",Cx,Cy)
    for i in range(len(ud_ids)):
        if (ud_pid == ud_ids[i]):
            z=ud_zpos[i]
    
    #rotate back to normal
    theta = math.asin((B[0]-A[0])/AB)
    x = Cx*math.cos(theta)-Cy*math.sin(theta)
    y = Cx*math.sin(theta)+Cy*math.cos(theta)
    
    #translate back to origin
    
    x+=A[0]
    y+=A[1]
    if ((x > 100) or (y>100) or (x<0) or (y<0)):
        print ("failed with (x,y):",x,y)
        Cx= -Cx
        x = Cx*math.cos(theta)-Cy*math.sin(theta)
        y = Cx*math.sin(theta)+Cy*math.cos(theta)
        x+=A[0]
        y+=A[0]
    
    print ("UD#",ud_pid, "located at (x,y,z):",x,y,z)
    print("")
    
    
            
#checks the list to see if ud_pid has 3 matches with unique SDs
def checkList(data, ud_pid, sd_coords):
    listLength = len(data)
    foundBool=False
    for i in range(listLength):
        ctr=0
        sd_pids=[]
        distances=[]
        for j in range(listLength):
            
            #if the counter hits 2, 
            if (ctr==2):
                foundBool=True
                break
            
            #if list is empty
            elif (ud_pid == data[j][1]) and (not sd_pids):
                sd_pids.append(data[j][0])
                distances.append(data[j][2])
                ctr+=1
                
            #otherwise
            elif (ud_pid == data[j][1]):
                #check the sd_pids and make sure it is not a duplicate
                myBool = True
                for k in range(ctr): #sweeps the sd_pids list
                    #if the sd_pid is found, it won't append
                    if (sd_pids[k] == data[j][0]):
                        myBool = False
                #otherwise, it'll append to the distances and sd_pids
                if myBool:
                    sd_pids.append(data[j][0])
                    distances.append(data[j][2])
                    ctr+=1
        if foundBool:
            break
    #after the loop is done, sd_pids should have 2
    if foundBool:
        # print("UD:",ud_pid)
        # for i in range(ctr):
        #     print ("sd#",i,"pid",sd_pids[i],"distance",distances[i])
        # print("")
        
        GPSfunc(distances, sd_coords, ud_pid, sd_pids)
        
          
######################################
##### THIS IS THE SERVER PROCESS #####
######################################

if __name__ == "__main__":
   
    ######################
    ######## INIT ########
    ######################
   
    #build queues for different purposes
    sdq = multiprocessing.Queue()           #transmitting SD IDs
    udq = multiprocessing.Queue()           #transmitting UD IDs
    #sdCoordsQ = multiprocessing.Queue()     #transmitting SD coordinates
    
    #a list for all the queues for each SD
    sd2mainQ = multiprocessing.Queue()
   
    #list for storing all UD processes
    ud_processes = []
    sd_processes = []
    
    sd_pipes = []
    ud_pipes = []
    #given that you want i * j pipes,
    userInpSD = 2
    userInpUD = 2
    
    pipeGrid = []
    pipeGrid2 = []
    pipeGridRow = []
    pipeGridRow2 = []
    #assemble the I x J grid that stores all the connections
    for i in range (userInpSD):     
        pipeGridRow = []                                 # empty pipe grid row
        pipeGridRow2 = []
        for j in range (userInpUD):                      #
            sd_conn, ud_conn = multiprocessing.Pipe()    # creating a pipe
            connections = [sd_conn, ud_conn]             # renaming for easier use of pipes
            pipeGridRow.append(connections)              # store each connection in pipeGrid so it can be referenced later.
            
            sd_conn, ud_conn = multiprocessing.Pipe()    # creating a pipe
            connections = [sd_conn, ud_conn]             # renaming for easier use of pipes
            pipeGridRow2.append(connections)
            
        pipeGrid.append(pipeGridRow)                     # store the pipe grid row in the pipe grid
        pipeGrid2.append(pipeGridRow2)
   
    #initialize SDs
    for i in range(userInpSD):                           # for each SD, assemble the connection grid
        sd_pipes = []                                    # clear sd_pipes 
        sd_pipes2 = []
        for j in range (userInpUD):                      # loop through the row
            sd_pipes.append(pipeGrid[i][j])              # append the connection in pipeGrid[i][j] to sd_pipe
            sd_pipes2.append(pipeGrid2[i][j])
        process = multiprocessing.Process(target=sd, args=(sd_pipes, sd_pipes2, sd2mainQ, sdq))
        sd_processes.append(process)                     # add SD to the sd_processes list
        process.start()                                 # start the process
    
    #initialize UDs
    for i in range(userInpUD):                           # for each UD, assemble the connection grid
        ud_pipes = []                                    # clear sd_pipes
        ud_pipes2 = []
        for j in range (userInpSD):                      # loop through the column
            ud_pipes.append(pipeGrid[j][i])              # append the connection in pipeGrid[j][i] to ud_pipes   
            ud_pipes2.append(pipeGrid2[j][i])
        process = multiprocessing.Process(target=ud, args=(ud_pipes, ud_pipes2, udq))
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
    
    sd_xpos = []
    sd_ypos = []
    sd_zpos = []
    
    ud_zpos = []
    
    data_storage = []
    print("[SD_PID, UD_PID, DISTANCE]")
    
    
    #####################
    ##### MAIN LOOP #####
    #####################
   
    while 1:
        #print("yea")
        ctr+=1
        
       
        # store all SD IDs, coords, and increments counter
        while sdq.empty() is False:
            sdInfo = sdq.get()
            sd_xpos.append(sdInfo[0])
            sd_ypos.append(sdInfo[1])
            sd_zpos.append(sdInfo[2])
            sd_ids.append(sdInfo[3])
            sd_len+=1
            
        
        # store all UD IDs and increment counter
        while udq.empty() is False:
            udInfo = udq.get()
            ud_ids.append(udInfo[0])   
            ud_zpos.append(udInfo[1])
            ud_len+=1
        
        #recieve data from each SD
        while sd2mainQ.empty() is False:
            # EVERY DATA THAT IS PULLED OUT OF THE QUEUE IS GOING TO BE [SD_PID, UD_PID, xy distance, UD_ZPOS
            myData = sd2mainQ.get() #store time, ud_pid, sd_pid
            #print("A pin from",myData[2],"to",myData[1],"took",myData[0],"seconds") #print the data
            print(myData)
            
            #locates where in array to store the data
            data_storage.append(myData)
                
                
       
        time.sleep(.3)
        
        if (ctr%25==0):
            print("\nList\n")
            for i in range(ud_len):
                print("UD#",i,", ID:",ud_ids[i])
            print("")
            for i in range(sd_len):
                print("SD#",i,", ID:",sd_ids[i])
            print("")
            # for i in range(len(sd_xpos)):
            #     print ("SD_XPOS:", sd_xpos[i])
            # for i in range(len(sd_ypos)):
            #     print ("SD_YPOS:", sd_ypos[i])
            # for i in range(len(sd_zpos)):
            #     print ("SD_ZPOS:", sd_zpos[i])
            
            
            #origin = [ sd_xpos[0], sd_ypos[0], sd_zpos[0] ]
            sd_coords = [sd_xpos, sd_ypos, sd_zpos]
            for i in range(ud_len):
                checkList(data_storage, ud_ids[i], sd_coords)
            