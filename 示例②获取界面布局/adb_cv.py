import os
import re
import cv2
import time
import numpy
import random
import subprocess 
import xml.etree.ElementTree as el

class Android(object):
    button={}
    def __init__(self,com,ip='127.0.0.1') :
        self.opencv_find_list={}
        self.conn=ip+':'+str(com)
        a=self.shell('adb connect '+self.conn,encoding='utf-8')
        if 'failed to connect to' in a :
            raise Exception('端口号错误')
        
        
        
    def shell(self,a,RT=True,encoding=None) :
        data=subprocess.Popen(a,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding=encoding)
        if RT == False :
            return
        return data.communicate()[0]
    
    
    
    def ADB(self,a,encoding='utf-8') :
        return self.shell(a,encoding=encoding)
    
        
        
    def END(seld) :
        os.system('adb disconnect')
        
        
        
    def get_now_button(self,app_name,F=None,path='/storage/emulated/0/window_dump.xml') :
        D={}
        os.system('adb shell uiautomator dump --compressed')
        if F != None :
            F()
        with open(path,'r') as f :
            data=f.read()
        #print(len(data))
        #input()
        root = el.fromstring(data)
        for book in root.iter("node"):
            if book.attrib['text'] != '' :
                K,V=book.attrib['text'],book.attrib['bounds']
                L=re.split(r'[^\d]',V)
                V=[int(i) for i in L if i != '']
                D[K]=V
        Android.button[app_name]=D
        print(D)
        return D
        
        
    
    def get_button_png(self,a,path) :
        if not os.path.isdir(path) :
            raise Exception('---路径错误---',path)
        img=self.an_ScreenShot()
        #print(img.shape)
        for i in a :
            v=a[i]
            img_button=img[v[1]:v[3],v[0]:v[2]]
            cv2.imwrite(path+'/'+i+'.png',img_button)       
        print('文件保存在以下目录 : ',path)
        
            
    
    def button_tap(self,dic,button_name,RANDOM=0) :
        v=dic.get(button_name)
        if v != None :
            t=[random.randint(v[0]+RANDOM,v[2]-RANDOM),random.randint(v[1]+RANDOM,v[3]-RANDOM)]
            self.tap(t)
        
    
            
    def an_ScreenShot(self) :
        data=self.shell('adb shell screencap -p')
        img=numpy.frombuffer(data,numpy.uint8)
        return cv2.imdecode(img,0)
        
        
        
    def tap(self,a,SH=False) :
        #T=time.time()
        if a :
            if SH == True :
                #print('subprocess')
                self.shell('adb shell input tap {} {}'.format(str(a[0]),str(a[1])),RT=False)
                #print(time.time()-T)
                return
            #print('os')
            os.system('adb shell input tap {} {}'.format(str(a[0]),str(a[1])))
        else :
            print('TAP ERROR',a)
        #print(time.time()-T)
        
        
    
    def swipe(self,a) :
        os.system('adb shell input swipe {} {} {} {} {}'.format(str(a[0]),str(a[1]),str(a[2]),str(a[3]),str(a[4])))
        
    
    
    def text(self,a) :
        os.system('adb shell input text '+a)
    
    
    
    def activity_get(self,a):
        q=self.shell('adb shell monkey -p {} -v -v -v 1'.format(a),encoding='utf-8').split('\n')
        for i in q :
            if 'cmp=' in i :
                print('\n'*50,'Activity : '+i.split('cmp=')[1].split('}')[0])
                break
            
            
            
    def activity_start(self,a) :
        self.shell('adb shell am start -S -W {}'.format(a),RT=False)
        
        

    def PNG_ifin(self,png,BF):
        #print(len(self.opencv_find_list))
        img1=self.an_ScreenShot()
        if BF == False :
            return img1,cv2.imread(png,0)
        if png in self.opencv_find_list :
            return img1,self.opencv_find_list[png]
        else :
            img=cv2.imread(png,0)
            self.opencv_find_list[png]=img
            return img1,img
            
            
        
    def opencv_find(self,png,threshold=0.9,RANDOM=5,BF=True,show=False,tap=False,SH=False):
        img1,img2=self.PNG_ifin(png,BF)
        y,x=img2.shape
        xy=cv2.matchTemplate(img1,img2,3)
        _,a,_,b= cv2.minMaxLoc(xy)
        if show :
            print('相似度:',png,'  >>>>  ',a)
        if a<threshold or a==1 :
            if tap == False :
                return False
            e=False
        else :
            result=[b[0]+(x//2),b[1]+(y//2)]
            e=(random.randint(result[0]-int(RANDOM),result[0]+int(RANDOM)),random.randint(result[1]-int(RANDOM),result[1]+int(RANDOM)))
        if tap == True :
            self.tap(e,SH)
            return
        return e

  
    
if __name__ == '__main__' :
    import sys
    a = Android(40893)
    while True :
        T=time.time()
        xy=a.opencv_find(sys.path[0]+'/测试.jpg',threshold=0.959)
        if xy :
            a.tap(xy,SH=True)
        else :
            break
        print('点击CTRL',time.time()-T)
    a.END()
        
