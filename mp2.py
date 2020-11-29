import time
import multiprocessing as mp
import sys
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def inp(x,y,z):
    for i in range(5):
        
        x.append(i)
        y.append(i)
        z.append(i)
        
        # x2=mp.Array('f', 0)
        
        # for j in range(x.len()):
        #     x2[j]=x[j]
        # x2[x.len()]=6
        # x=x2;
        # x.append(6)
        # y.append(6)
        # z.append(6)
        time.sleep(1)

def printer(x,y,z):
    for i in range(5):
        time.sleep(1)
        ax.scatter(x, y, z, c='r', marker='o')
        plt.show()
        plt.pause(2)
        
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

if __name__ == '__main__':
    manx=mp.Manager()
    x=manx.list()
    many=mp.Manager()
    y=manx.list()
    manz=mp.Manager()
    z=manx.list()
    
   
    
    mp1 = mp.Process(target=inp, args=(x,y,z))
    mp2 = mp.Process(target=printer, args=(x,y,z))
    
    mp1.start()
    mp2.start()
    
    mp1.join()
    mp2.join()
    print(x)
    print("done")