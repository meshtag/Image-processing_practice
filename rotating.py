import matplotlib.image as mimg
import matplotlib.pyplot as plt
import numpy as np
import math
im1=mimg.imread('rotate.png')
orig_arr=np.array(im1)#Numpy array of original image. 
x,y,c=im1.shape
i=int(input('Enter the desired angle of rotation '))
ans=np.empty((x,y,c))
for x1 in range(x):
    for y1 in range(y):
            xr=abs(int(x1*math.cos(math.radians(i))-y1*math.sin(math.radians(i))))
            yr=abs(int(x1*math.sin(math.radians(i))+y1*math.cos(math.radians(i))))
            if(xr<x and yr<y):
                ans[xr,yr,:] = orig_arr[x1,y1,:]
                print(str(orig_arr[x1,y1,:] )+"    "+str(ans[xr,yr,:]))
rot_image=plt.imshow(ans)
plt.show()

T=np.array([math.cos(math.radians(i)),-math.sin(math.radians(i)),math.sin(math.radians(i)),math.cos(math.radians(i))])
T.resize(2,2)
#print(T)
INV_T=np.linalg.inv(T)
#print(INV_T)
def neighbour_interpolation(x1,y1,im1,INV_T):
    x_m,y_m,_=im1.shape
    x_max=int(x_m)-1
    y_max=int(y_m)-1
    x,y,_ = INV_T @ np.array([x1,y1,1])
    if(np.floor(x)==x and np.floor(y)==y):
        return im1[x,y,]
    if(abs(np.floor(x)-x)<abs(np.ceil(x)-x)):
        x=int(x)
    else:
        x=int(x)+1
    if(abs(np.floor(y)-y)<abs(np.ceil(y)-y)):
        y=int(y)
    else:
        y=int(y)+1
    if(x>x_max):
        x=x_max
    if(y>y_max):
        y=y_max
    return im1[x,y,]
for x1 in range(x):
    for y1 in range(y):
        ans[x1,y1,:]=neighbour_interpolation(x1,y1,im1,INV_T)

rot1=plt.imshow(ans)
plt.show()




