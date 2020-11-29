from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import time
import threading

def printTest():
    global x,y,z,ax,plt
    time.sleep(2)
    for i in range(5):
        lock.acquire()
        print("printing\n")
        print(x,y,z)
        #plt.cla()
        ax.scatter(x, y, z, c='r', marker='o')
        plt.show()
        plt.pause(2)
        
        time.sleep(1)
        lock.release()
        time.sleep(1)
        
        
def inputData():
    time.sleep(0.5)
    lock.acquire()      #checks if the thread is locked
    
    print("inputting\n")
    global x,y,z
    xin=input("Enter the x value: ")
    yin=input("Enter the y value: ")
    zin=input("Enter the z value: ")
    #convert to float
    xfl=float(xin)
    yfl=float(yin)
    zfl=float(zin)
    #append to coords                       #this section is not used, trying to just plot new points as they come
    x.append(xfl)
    y.append(yfl)
    z.append(zfl)
    time.sleep(0.5)
    lock.release()      #checks if the thread is locked
    
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

x =[]
y =[]
z =[]


lock = threading.Lock()
    
pth = threading.Thread(target=printTest)
pth.start()
for i in range(5):
    ith = threading.Thread(target=inputData)
    ith.start()
    ith.join()

