import sys
import cv2
import time
import numpy as np
from tqdm import tqdm

FPS = 12

VIDEOS = True

GPS = False

#NOW_list = [[49999,50000,'D']]  #单个点,注意这是个嵌套列表

NOW_list = [[49975,49975,'U'],[49975,50025,'U'],[50025,49975,'D'],[50025,50025,'D']]  #四个点



'''

FPS :
    最后视频的帧数
    
    
VIDEOS :
    True : 生成视频,速度慢 
    False : 只会获取最后的结果,速度快


NOW_list :
    开始坐标点 [竖坐标，横坐标,朝向] 
    50000,50000是中心坐标
    U : 向上 
    D : 向下
    L : 向左
    R : 向右
    多个点 , 多个点有先后顺序,如果结果和预期的不一样;可以试试起始点的朝向,上下交换,左右交换,如果上下发生交换，则左右必须交换(我猜的);反之,亦然               
    多个点且演化次数多应该选择只要最后结果，而不是生成每步的视频


GPS :
    画面追踪 , 如果用了追踪 , FPS最好不要超过12

'''

def NEXT_0(a) :
    _NOW = a
    X,Y,compass = _NOW
    if compass == 'U' :
        _NOW = [X+1,Y,'R']
        
    elif compass == 'D' :
        _NOW = [X-1,Y,'L']
        
    elif compass == 'R' :
        _NOW = [X,Y-1,'D']  
        
    elif compass == 'L' :
        _NOW = [X,Y+1,'U']  
    NOW_list.append(_NOW)
        
def NEXT_255(a) :
    _NOW = a
    X,Y,compass = _NOW
    if compass == 'U' :
        _NOW = [X-1,Y,'L']
        
    elif compass == 'D' :
        _NOW = [X+1,Y,'R']
        
    elif compass == 'R' :
        _NOW = [X,Y+1,'U']  
        
    elif compass == 'L' :
        _NOW = [X,Y-1,'D']  
    NOW_list.append(_NOW)
    
    
a = np.zeros((100000,100000),dtype=np.uint8)
#内存不够就减0,坐标和裁切部分也要同步改动
mv = 1
if VIDEOS == True :
    fourcc = cv2.VideoWriter_fourcc(*'avc1')  
    video = cv2.VideoWriter(sys.path[0]+'/蓝盾蚂蚁'+str(time.time())+'.mp4', fourcc,FPS, (2000,2000),isColor=False)
SSS = int(input('\n'*50+'''请输入需要演化的次数(单个点为实际输入的次数，多个点需要乘以点的个数)
>>>请输入纯数字 : '''))   
T=tqdm(total=SSS)
    
while True :
    NOW = NOW_list.pop(0)
    if a[NOW[0],NOW[1]] == 0 :
        a[NOW[0],NOW[1]] = 255
        NEXT_0(NOW)
           
    elif a[NOW[0],NOW[1]] == 255 :
        a[NOW[0],NOW[1]] = 0
        NEXT_255(NOW)
        
    if VIDEOS == True :
        if GPS == False :
            img = a[49950:50050,49950:50050] 
        elif GPS == True  :
            Y,X,_ = NOW
            img = a[Y-50:Y+50,X-50:X+50]
        img = cv2.resize(img, None, fx=20, fy=20, interpolation=cv2.INTER_AREA)
        cv2.rectangle(img,(0,0),(2000,2000),(255),10)
        for i in range(20,2000,20) :
            cv2.line(img, (i,20),(i,1980),0,3)
            cv2.line(img, (20,i),(1980,i),0,3)
        if GPS == True :
            img=cv2.putText(img,'X:{}  Y:{}'.format(X,Y),(10,1980),cv2.FONT_HERSHEY_SIMPLEX,1,(255),2)
        video.write(img)
    T.update(1)
    if mv == SSS :
        break
    mv+=1
    
if VIDEOS == False :
    img = a[49750:50250,49750:50250]
    img = cv2.resize(img, None, fx=20, fy=20, interpolation=cv2.INTER_AREA)
    cv2.rectangle(img,(0,0),(10000,10000),(255),10)
    for i in range(0,10000,20) :
        cv2.line(img, (i,20),(i,9980),0,3)
        cv2.line(img, (20,i),(9980,i),0,3)
    cv2.imwrite(sys.path[0]+'/蓝盾蚂蚁最后结果'+str(time.time())+'.png',img)
elif VIDEOS == True :
    video.release() 