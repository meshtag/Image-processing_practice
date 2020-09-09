from cv2 import cv2
import numpy as np
def rgb_to_bgr(img):
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            dum=img[x][y][0]
            img[x][y][0]=img[x][y][2]
            img[x][y][2]=dum
    return img

def convolution(img,ker_mat):
    xk,yk = ker_mat.shape
    x,y,z = img.shape
    img_pad=np.zeros((x+xk-1,y+yk-1,z))
    img_pad[int(xk/2):int(xk/2)+x,int(yk/2):int(yk/2)+y,:] = img
    op_img=np.zeros_like(img)
    for x1 in range(int(xk/2),int(xk/2)+x):
        for y1 in range(int(yk/2),int(yk/2)+y):
            for z1 in range(z):
                op_img[x1-int(xk/2),y1-int(yk/2),z1] = (ker_mat * img_pad[x1-int(xk/2):x1+xk-int(xk/2),y1-int(yk/2):y1+yk-int(yk/2),z1]).sum()
    cv2.imshow('gauss_filter',op_img)
    cv2.waitKey(0)
    return op_img

def mask(img,l_b,u_b):
    maskb=np.zeros_like(img)
    img1=img
    img=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    cv2.imshow('hsv',img)
    cv2.waitKey(0)
    for x1 in range(img.shape[0]):
        for y1 in range(img.shape[1]):
            if(img[x1,y1,0]>=l_b[0] and img[x1,y1,1]>=l_b[1] and img[x1,y1,2]>=l_b[2] and img[x1,y1,0]<=u_b[0] and img[x1,y1,1]<=u_b[1] and img[x1,y1,2]<=u_b[2]):
                maskb[x1,y1,0]=255#It was giving al,ost black output when conditional value was set to 1 and not 255
                maskb[x1,y1,1]=255
                maskb[x1,y1,2]=255
    cv2.imshow('mask',maskb)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    img1=np.bitwise_and(img1,maskb)
    return img1

img=cv2.imread('mask.jpg')
#img=rgb_to_bgr(img)
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
gaussian_blur=np.array([[1,  4,  6,  4, 1],
                         [4, 16, 24, 16, 4],
                         [6, 24, 36, 24, 6],
                         [4, 16, 24, 16, 4],
                         [1,  4,  6,  4, 1]])/256
l_b=np.array([94,130,38])
u_b=np.array([179,255,255])
img=mask(convolution(img,gaussian_blur),l_b,u_b)
cv2.imshow('masked_image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()          