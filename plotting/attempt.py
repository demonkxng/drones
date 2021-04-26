from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import time

#set up figure and plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

x=[]
y=[]
z=[]

inp=input("Please enter how many drones you want to place: ")
totalDrones=int(inp)
for i in range(totalDrones):
    #plt.cla()                              #clear has been temp disabled
    plt.pause(5)
    print("Drone #",i+1,":")
    #input user data
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
    
    #plot
    #ax.scatter(x, y, z, c='r', marker='o')
    ax.scatter(xfl, yfl, zfl, c='r', marker='o')
    plt.show()
    #time.sleep(5) #allows the plot to update
    
    
print(x,y,z)