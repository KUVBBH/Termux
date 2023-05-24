import sys
import cv2
import time
from adb_cv import Android as an

a=an(42605)
a.activity_start('com.umonistudio.tilepk/com.umonistudio.tile.tile')
path=sys.path[0]+'/'

kkk=0
while True :
        time.sleep(0.5)
        xy=a.opencv_find(path+'经典.jpg',threshold=0.9999,show=True)
        if xy :
            print('点击经典')
            a.tap(xy,SH=False)
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
            a.tap(xy,SH=False)
            kkk=0
            break
        else :
            kkk+=1
            if kkk == 15 :
                sys.exit()

img1=cv2.imread(path+'块.jpg',1)
wh=img1.shape
w,h=wh[1]//2,wh[0]//2
while True :
    T=time.time()
    img2=a.an_ScreenShot(flags=1)
    img2[0:1100,0:1080]=0,0,0
    xy=cv2.matchTemplate(img2,img1,3)
    _,o,_,p= cv2.minMaxLoc(xy)
    x,y=p[0]+w,p[1]+h
    if o > 0.999 and o != 1 :
        print('点击方块')
        a.tap((x,y),SH=False)
        print('TIME:',time.time()-T,'相似度',o)
        kkk=0
    else :
        kkk+=1
        if kkk == 3 :
            break
a.END()
        