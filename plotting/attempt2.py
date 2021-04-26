from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

#############
##FUNCTIONS##
#############

def newDrone():
    global numDrones, ax, x, y, z
    print("Drone #",numDrones,":")
    #input user data
    xin=input("Enter the x value: ")
    yin=input("Enter the y value: ")
    zin=input("Enter the z value: ")
    #convert to float
    xfl=float(xin)
    yfl=float(yin)
    zfl=float(zin)
    
    newDroneBool=True
    #check to see if drone exists
    for i in range(numDrones-1):
        if (x[i]==xfl and y[i]==yfl and z[i]==zfl):
            newDroneBool=False
            print("This drone already exists! (Drone",i+1,")")
            break
            
    #if it doesnt already exist     
    if(newDroneBool):
        #append to coords                      
        x.append(xfl)
        y.append(yfl)
        z.append(zfl)
        numDrones+=1

def removeDrone():
    global numDrones, x, y, z
    print("Removing a Drone!")
    xin=input("Enter the x value: ")
    yin=input("Enter the y value: ")
    zin=input("Enter the z value: ")
    #convert to float
    xfl=float(xin)
    yfl=float(yin)
    zfl=float(zin)
    removed=False
    for i in range(numDrones-1):
        if (x[i]==xfl and y[i]==yfl and z[i]==zfl):
            print("Removing Drone #",i+1)
            x.pop(i)
            y.pop(i)
            z.pop(i)
            removed=True
            numDrones-=1
            break
    if(not removed):
        print("Failed to remove drone.")
            
def viewGraph():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    global x, y, z
    print(x,y,z)
    print("Close the plot to resume!")
    plt.cla()
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')  
    ax.scatter(x, y, z, c='r', marker='o')
    plt.show() 
    #plt.pause(droneDelay)

def displayGraph():
    global x, y, z
    slp=input("How long would you like to display?: ")
    slp=float(slp)
    ax.scatter(x, y, z, c='r', marker='o')
    plt.show()
    #plt.pause(slp)

def userExit():
    return False

def printText():
    global x, y, z
    print(x,y,z)

def droneDelayFunc():
    global droneDelay
    inp=input("Please enter how long to delay: ")
    inp=float(inp)
    droneDelay=inp
    print("Succesfully changed delay time to",inp,"seconds")
    
def printList():
    global x,y,z
    for i in range(numDrones-1):
        print("Drone #",i+1,": (",x[i],",",y[i],",",z[i],")")  

def addDrones():
    inp=input("How many Drones would you like to add?")
    inp=int(inp)
    for i in range(inp):
        newDrone()
        
def listFuncs():
    print("Command List:")
    print("L - Show command list")
    print("P - Print in Text Format")
    print("N - Add a new Drone")
    print("A - Add a few Drones")
    print("R - Remove a  Drone")
    print("D - Display the graph for X seconds")
    print("S - Display time after adding new Drone")
    print("V - Default view")
    print("Q - Quit")
    
########
##MAIN##
########

#set up figure and plot
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')

#global variable initialization
x=[]
y=[]
z=[]
numDrones=1
runTime=True
droneDelay=2
    
listFuncs()

#running loop
while (runTime):
    
    #user input
    userInp=input("Please enter your command: ")
    userInp=userInp.upper()

    #choose which function to run
    if (userInp == "Q"):
        runTime=userExit()
    elif (userInp == "P"):
        printList()
    elif (userInp == "N"):
        newDrone()
        viewGraph()
    elif (userInp == "D"):
        displayGraph()
    elif (userInp == "S"):
        droneDelayFunc()
    elif (userInp == "V"):
        viewGraph()
    elif (userInp == "L"):
        listFuncs()
    elif (userInp == "R"):
        removeDrone()
        viewGraph()
    elif (userInp == "A"):
        addDrones()
        viewGraph()
    else:
        print("Invalid Response.")