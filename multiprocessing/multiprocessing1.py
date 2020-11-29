from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import time
import threading
import multiprocessing
import os

def printTest():
    global x
    global y
    global z
    time.sleep(2)
    for i in range(3):
        lock.acquire()
        print("printing\n")
        print(x,y,z)
        ##plt.cla()
        # ax.scatter(x, y, z, c='r', marker='o')
        # plt.show()
        # plt.pause(2)
        
        time.sleep(1)
        lock.release()
        time.sleep(1)
        
        
def inputData():
    time.sleep(0.5)
    lock.acquire()      #checks if the thread is locked
    
    print("inputting\n")
    global x
    global y
    global z
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


lock = multiprocessing.Lock()
    
if __name__ == '__main__':
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.set_xlabel('X')
    # ax.set_ylabel('Y')
    # ax.set_zlabel('Z')
    
    x =[]
    y =[]
    z =[]
    
    
    
        
    pth = multiprocessing.Process(target=printTest)
    pth.start()
    
    for i in range(3):
        ith = multiprocessing.Process(target=inputData)
        ith.start()
        ith.join()

