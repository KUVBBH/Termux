import sys
import cv2
import time
from adb_cv_minicap import Android as an

a=an(37337)
a.activity_start('com.umonistudio.tilepk/com.umonistudio.tile.tile')
path=sys.path[0]+'/'

kkk=0
while True :
        time.sleep(0.5)
        xy=a.opencv_find(path+'经典.jpg',threshold=0.9999,show=True)
        if xy :
            print('点击经典')
            a.tap(xy)
            kkk=0
            break
        else :
            kkk+=1
            if kkk == 50 :
                sys.exit()
time.sleep(1)
while True :
        xy=a.opencv_find(path+'开始.jpg',threshold=0.98,show=True)
        if xy :
            print('点击开始')
            a.tap(xy)
            kkk=0
            break
        else :
            kkk+=1
            if kkk == 15 :
                sys.exit()
C =  [0,35,160]
S = 0
while True :
    print(S)
    #time.sleep(0.09)
    img=a.an_ScreenShot(flags=1)
    #print(img[1370,135])
    #print(img[1370,405])
    #print(img[1370,675])
    #print(img[1370,945])
    if list(img[1370,135]) == C :
        a.tap((135,1370))
        S = 0
        print('点击')
        continue
    if list(img[1370,405]) == C :
        a.tap((405,1370))
        S = 0
        print('点击')
        continue
    if list(img[1370,675]) == C :
        a.tap((675,1370))
        S = 0
        print('点击')
        continue
    if list(img[1370,945]) == C :
        a.tap((945,1370))
        S = 0
        print('点击')
        continue
    S+=1
    if S == 10 :
        print('结束')
        break

a.END()
        