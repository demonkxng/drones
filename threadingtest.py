from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import time
import threading


#printing func
def printGraph():
    plt.pause(5)
    ax.scatter(x, y, z, c='r', marker='o')
    plt.show()
  
    
  
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
global runTime
runTime=True
    
#while(runTime):
i=1
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
x.append(xfl)
y.append(yfl)
z.append(zfl)

#looping condition
'''
cond=input("More Drones? (Y/N): ")
if (cond.upper() == "N") :
    runTime=False
else:
    i=i+1
    
'''

myThread = threading.Thread(target=printGraph)
myThread.start()





'''
myExp=threading.Thread(target=datainput)
myExp.start()
'''