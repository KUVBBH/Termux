import numpy as np
import random
import json
import sys
import cv2
 
def R() :
    q=int(input('需要生成的随机数个数 : '))
    r=[]
    while len(r) < q :
        b=[random.randint(1,98),random.randint(1,98)]
        r.append(b)
    p=[i for i in r if r.count(i) == 1]
    print(len(r),len(p))
    return p
    

def yx_next(i) :
    xy=[]
    y=i[0]-1
    x=i[1]-1
    if x >= 0 and x < max_x and y >=0 and y < max_y :
        xy.append([y,x])
        
    y=i[0]-1
    x=i[1]
    if x >= 0 and x < max_x and y >=0 and y < max_y :
        xy.append([y,x])
    
    y=i[0]-1
    x=i[1]+1
    if x >= 0 and x < max_x and y >=0 and y < max_y :
        xy.append([y,x])
        
    y=i[0]
    x=i[1]-1
    if x >= 0 and x < max_x and y >=0 and y < max_y :
        xy.append([y,x])
        
    y=i[0]
    x=i[1]+1
    if x >= 0 and x < max_x and y >=0 and y < max_y :
        xy.append([y,x])
        
    y=i[0]+1
    x=i[1]-1
    if x >= 0 and x < max_x and y >=0 and y < max_y :
        xy.append([y,x])
        
    y=i[0]+1
    x=i[1]
    if x >= 0 and x < max_x and y >=0 and y < max_y :
        xy.append([y,x])
    
    y=i[0]+1
    x=i[1]+1
    if x >= 0 and x < max_x and y >=0 and y < max_y :
        xy.append([y,x])
        
    return np.array(xy)

####################################
cap_fps = 12  #这里修改帧数

name={
    '随机' : R ,
    '滑翔机':[[50,50],[50,51],[50,52],[49,52],[48,51]],
    '闪光灯':[[50,50],[50,51],[50,52]],
    '五连':[[50,50],[50,49],[50,51],[49,50],[51,51]],
    '蟾蜍':[[50,50],[50,51],[50,52],[51,51],[51,52],[51,53]],
    '高斯帕滑翔机枪':[[50,50],[51,50],[50,51],[51,51],[60,50],[60,49],[60,51],[61,48],[61,52],[62,53],[62,47],[63,53],[63,47],[64,50],[65,48],[65,52],[66,49],[66,50],[66,51],[67,50],[70,51],[70,52],[70,53],[71,51],[71,52],[71,53],[72,50],[72,54],[74,50],[74,49],[74,54],[74,55],[84,52],[84,53],[85,52],[85,53]],
    
}

#https://baijiahao.baidu.com/s?id=1653854876062433235&wfr=spider&for=pc&searchword=生命游戏结构
####################################
a=np.zeros((100,100),dtype=np.uint8)
key=list(name.keys())
print('\n'*50)
for i in range(len(key)) :
    print(i,'------',key[i])
d_key=int(input('请输入序号 : '))
if key[d_key] == '随机' :
    xxyy=name[key[d_key]]()
else :
    xxyy=name[key[d_key]]
for i in xxyy :
    a[i[0],i[1]] = 255
max_y,max_x=a.shape
while True :
    try :
        SSS=int(input('演化次数 : '))
        break
    except :
        print('输入错误')
fourcc = cv2.VideoWriter_fourcc(*'avc1')  
video = cv2.VideoWriter(sys.path[0]+'/out.mp4', fourcc, cap_fps, (2000,2000),isColor=False)
mv=1




while True :
    yx_255=np.argwhere(a==255)
    yx_0=[]
    W=[]
    B=[]
    for i in yx_255 :
        o=yx_next(i)
        S=0
        for p in o :
            if not yx_0  :
                yx_0.append(p)
            if not (np.any(np.all(p == yx_0, axis=1))) :
                yx_0.append(p)
            if (np.any(np.all(p == yx_255, axis=1))) :
                S+=1
        if S > 3 or S < 2 :
            W.append(i)
    yx_0=np.array(yx_0)  
    for i in yx_0 :
        o=yx_next(i)
        S=0
        for p in o :
            if (np.any(np.all(p == yx_255, axis=1))) :
                S+=1
        if S == 3 :
            B.append(i)
    img = cv2.resize(a, None, fx=20, fy=20, interpolation=cv2.INTER_AREA)
    cv2.rectangle(img,(0,0),(2000,2000),(255),10)
    video.write(img)
    for i in W :
        a[i[0],i[1]] = 0
    for i in B :
        a[i[0],i[1]] = 255
    print('\r','%.6f'%(mv/SSS*100),'%',end='')
    if mv == SSS :
        break
    mv+=1

video.release() 
