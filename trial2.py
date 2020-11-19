from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import time


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x =[1,2,3,4,5,6,7,8,9,10]
y =[5,6,2,3,13,4,1,2,4,8]
z =[-2,-3,-3,-3,-5,-7,-9,-11,-9,-10]



ax.scatter(x, y, z, c='r', marker='o')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()

plt.pause(0.1)
plt.cla()


x2=input("enter x: ")
x3=float(x2)
y2=3
z2=-3
x.append(x3)
y.append(y2)
z.append(z2)

print(x,y,z)

ax.scatter(x, y, z, c='r', marker='o')
plt.show()
