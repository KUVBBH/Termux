'''
以下代码来自:
https://blog.csdn.net/L603409742/article/details/104238820/
'''
import cv2 as cv
import numpy as np
import math
import os
import threading
import random

def run(a) :
    # 先读取游戏画面截图
    img = a
    # 对图片上下部分进行切片操作，缩小目标区域
    up_cut = int(a .shape[0]*0.3)
    down_cut = int(img .shape[0]*0.7)
    img = img [up_cut:down_cut]
    # 将图片色彩空间转换为hsv
    img_hsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)
    # 根据目标小人的身体颜色范围，提取目标小人，注意：这里    面的颜色范围格式是hsv
    color_min = np.int32([105,30,30])
    color_max = np.int32([200,200,120])
    color_mask = cv.inRange(img_hsv,color_min,color_max)
    # 勾画目标小人边缘，返回的第一个参数是轮廓信息
    contours = cv.findContours(color_mask,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)[0]
    # 绘制目标小人坐标信息
    max_contours = max(contours,key=cv.contourArea)
    max_contours = cv.convexHull(max_contours)
    rect = cv.boundingRect(max_contours)
    x,y,w,h = rect
    point_pos = (x+int(w/2),y+h-15)
    point_pos_r = point_pos
    #print(point_pos)
    #cv.rectangle(img, (x,y), (x+w,y+h), (0, 0, 255), 5)
    #cv.circle(img, point_pos, 8, (0, 0, 255), -1)
    # 高斯模糊，为了去除一些噪点
    img_blur = cv.GaussianBlur(img, (5, 5), 0)
    # 边缘检测
    canny_img = cv.Canny(img_blur, 1, 15)
    # 将图片色彩空间转换为hsv
    img_hsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)
    # 根据目标小人的身体颜色范围，提取目标小人，注意：这里     面的颜色范围格式是hsv    
    color_min = np.int32([105,30,30])
    color_max = np.int32([200,200,120])
    color_mask = cv.inRange(img_hsv,color_min,color_max)
    # 勾画目标小人边缘，返回的第一个参数是轮廓信息
    contours = cv.findContours(color_mask,cv.RETR_EXTERNAL    ,cv.CHAIN_APPROX_SIMPLE)[0]
    max_contours = max(contours,key=cv.contourArea)
    max_contours = cv.convexHull(max_contours)
    rect = cv.boundingRect(max_contours)
    # 移除小人头部附近像素
    r_x,r_y,r_w,r_h = rect
    for y in range(r_y-150, r_y+r_h):
        for x in range(r_x-20, r_x+r_w+20):
            canny_img[y][x] = 0
     # 计算目标中心点
    crop_h, crop_w = canny_img.shape
    center_x, center_y = 0, 0
    max_x = 0
    for y in range(crop_h):
        for x in range(crop_w):
            if canny_img[y, x] == 255:
                if center_x == 0:
                    center_x = x
                if x > max_x:
# 如果发现两次y轴的像素点间隔超过了一定值，就认为已经找到中心点了
                    if(center_y!=0 and y-center_y>50):
                        point_pos = (center_x, center_y)
                        return point_pos,point_pos_r
                    else:
                        #cv.circle(img, (center_x, center_y), 1,(255,0,0), -1)
                        center_y = y
                        max_x = x
                        point_pos = (center_x, center_y)
                        return point_pos,point_pos_r



def time(a) :
    b=run(a)
    distance = np.array(b[0])-np.array(b[1])
    distance = int(math.hypot(distance[0],distance[1]))
    click_time = int(distance * 1.25)
    return click_time
    
