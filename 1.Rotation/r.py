import matplotlib.pyplot as plt 
import math
import numpy as np
from PIL import Image
img=plt.imread('rotate.png')
img_arr=np.array(img)
plt.imshow(img)
plt.show()
i=int(input('Enter angle of rotation  '))
i=math.radians(i)
T=np.array([math.cos(i),math.sin(i),0,-math.sin(i),math.cos(i),0,0,0,1])#Rotation matrix for anticlockwise rotation
T.resize(3,3)
x,y,_=img_arr.shape
print("Input image shape is :"+str(img_arr.shape))
#new_img=np.empty((abs(int(x*math.cos(i)+y*math.sin(i)+1)),abs(int(y*math.cos(i)+x*math.sin(i)+1)),_))
new_img=np.empty((x,y,_))

'''fig = plt.gcf()
fig.set_size_inches(18.5, 10.5, forward=True)'''

for x1 in range(x):
    for y1 in range(y):
        co_ord_mat=np.array([x1-img_arr.shape[0]/2,y1-img_arr.shape[1]/2,1])#Making appropriate changes in co-ordinates for rotating the image about its center.
        tra_mat = co_ord_mat @ T
        nx,ny,_=tra_mat
        nx,ny=int(nx+img_arr.shape[0]/2),int(ny+img_arr.shape[1]/2)
        if(nx>=0 and ny>=0 and nx<img_arr.shape[0] and ny<img_arr.shape[1]):
            new_img[nx,ny,:]=img_arr[x1,y1,:]
        

T_INV=np.linalg.inv(T)
def interpolation(x1,y1,img_arr):#Function for implementing nearest neighbour interpolation method
    co_ord_mat1=np.array([x1-img_arr.shape[0]/2,y1-img_arr.shape[1]/2,1])
    tra_mat1 = co_ord_mat1 @ T_INV
    nx1,ny1,_=tra_mat1
    x1_max,y1_max=img_arr.shape[0]-1,img.shape[1]-1
    nx1,ny1=int(nx1+img_arr.shape[0]/2),int(ny1+img_arr.shape[1]/2)
    if(nx1==np.floor(nx1) and ny1==np.floor(ny1)):
        if(nx1>x1_max):
            nx1=x1_max
        if(ny1>y1_max):
            ny1=y1_max
        return img_arr[nx1,ny1,]
    if(abs(nx1-np.floor(nx1))<abs(nx1-np.ceil(nx1))):
        nx1=np.floor(nx1)
    else:
        nx1=np.ceil(nx1)
    if(abs(ny1-np.floor(ny1))<abs(ny1-np.ceil(ny1))):
        ny1=np.floor(ny1)
    else:
        ny1=np.ceil(ny1)
    if(nx1>x1_max):
        nx1=x1_max
    if(ny1>y1_max):
        ny1=y1_max
    if(nx1>=0 and ny1>=0):
        return img_arr[nx1,ny1,]
for x1 in range(x):
    for y1 in range(y):
        new_img[x1,y1,:] = interpolation(x1,y1,img_arr)
img_pil=Image.fromarray(new_img,'RGB')
plt.imshow(new_img)
plt.savefig('res_rotate')
plt.show()