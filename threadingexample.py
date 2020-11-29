from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import time
import threading


#printing func
def printGraph(lock):
    global x                                    #global vars
    global y                                    #global vars
    global z                                    #global vars
    lock.acquire()                              #locks
    plt.cla()                                   #clears plot
    ax.scatter(x, y, z, c='r', marker='o')      #remakes plot
    plt.show()                                  #shows plot
    lock.release()                              #unlocks
  
#inputting func
def datainput(lock):
    #while(runTime):
    
    for i in range(5):
        print("Drone #",i,":")
        #input user data
        xin=input("Enter the x value: ")
        yin=input("Enter the y value: ")
        zin=input("Enter the z value: ")
        #convert to float
        xfl=float(xin)
        yfl=float(yin)
        zfl=float(zin)
        #append to coords
        global x
        global y
        global z
        x.append(xfl)
        y.append(yfl)
        z.append(zfl)
        
        #create a printer thread
        myThread = threading.Thread(target=printGraph, args=(lock,))
        myThread.start()
    #looping condition
    '''
    cond=input("More Drones? (Y/N): ")
    if (cond.upper() == "N") :
        runTime=False
    else:
        i=i+1
        
    '''
    
    
    #end while    
#end input

####MAIN####

#set up figure and plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

#coords, (x[i], y[i], z[i])
x=[]
y=[]
z=[]

#other intializations
lock = threading.Lock()
global runTime
runTime=True

myExp=threading.Thread(target=datainput, args=(lock,))
myExp.start()