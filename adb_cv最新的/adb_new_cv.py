import os
import re
import time
import random
import subprocess 
import xml.etree.ElementTree as el
import cv2
import numpy



class Android(object) :
    button = {}
    Mask_colcr = None
    def __init__(self,com,ip='127.0.0.1') :
        self.opencv_find_list = {}
        self.conn = ip+':'+str(com)
        a = self.shell('adb connect '+self.conn,RETURN=True,OS=False,encoding='utf-8')
        print('连接成功 : ',self.conn)
        if 'failed to connect to' in a :
            raise Exception('端口号错误')
        
        
    def shell(self,a,RETURN=True,OS=False,encoding=None) :
        if OS :
            os.system(a)
            return
        data = subprocess.Popen(a,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding=encoding)
        if not RETURN :
            return
        return data.communicate()[0]
        
        
    #当前连接的设备   
    def conn_now(self) :
        return self.shell('adb devices',RETURN=True,OS=False,encoding='utf-8')
        
    
    #执行ADB命令
    def ADB_SHELL(self,a,**kwargs) :
        return self.shell(a,**kwargs)
        
        
    #断开ADB连接
    def END(self) :
        self.shell('adb disconnect',OS=True)
        
        
    #模拟点击
    def tap(self,a,**kwargs) :
        #T = time.time()
        if a :
            self.shell('adb shell input tap {} {}'.format(str(a[0]),str(a[1])),**kwargs)
        else :
            print('TAP ERROR',a)
        #print(time.time()-T)
    
    
    #模拟滑动
    def swipe(self,a,**kwargs) :
        self.shell('adb shell input swipe {} {} {} {} {}'.format(str(a[0]),str(a[1]),str(a[2]),str(a[3]),str(a[4])),**kwargs)
        
        
    #获取布局  
    def get_now_button(self,app_name,F=None,path='/storage/emulated/0/window_dump.xml') :
        D = {}
        self.shell('adb shell uiautomator dump --compressed',OS=True)
        if F != None :
            F()
        with open(path,'r') as f :
            data = f.read()
        root = el.fromstring(data)
        for book in root.iter('node') :
            if book.attrib['text'] != '' :
                K,V = book.attrib['text'],book.attrib['bounds']
                L = re.split(r'[^\d]',V)
                V = [int(i) for i in L if i != '']
                D[K] = V
        Android.button[app_name] = D
        return D
        
    
    #截图
    def an_ScreenShot(self,flags=0,Mask=None,Resize=None) :
        '''
        flags = 0 灰度
        flags = 1 BGR
        '''
        data = self.shell('adb shell screencap -p',RETURN=True,OS=False)
        img = numpy.frombuffer(data,numpy.uint8)
        img = cv2.imdecode(img,flags)
        if Mask != None :
            img[Mask[0]:Mask[1],Mask[2]:Mask[3]] = Android.Mask_colcr
            return img
        if Resize != None :
            return img[Resize[0]:Resize[1],Resize[2]:Resize[3]]
        return img
    
    
    #获取按钮图片
    def get_button_png(self,a,path) :
        if not os.path.isdir(path) :
            raise Exception('---路径错误---',path)
        img = self.an_ScreenShot()
        for i in a :
            v = a[i]
            img_button = img[v[1]:v[3],v[0]:v[2]]
            cv2.imwrite(path+'/'+i+'.png',img_button)   
        print('文件保存在以下目录 : ',path)

    
    #通过布局点击按钮
    def button_tap(self,dic,button_name,RANDOM=0,**kwargs) :
        v = dic.get(button_name)
        if v != None :
            t = [random.randint(v[0]+RANDOM,v[2]-RANDOM),random.randint(v[1]+RANDOM,v[3]-RANDOM)]
            self.tap(t,**kwargs)



    #获取activity
    def activity_get(self,a):
        q = self.shell('adb shell monkey -p {} -v -v -v 1'.format(a),encoding='utf-8').split('\n')
        for i in q :
            if 'cmp=' in i :
                print('\n'*50,'Activity : '+i.split('cmp=')[1].split('}')[0])
                break
            
            
    #启动应用      
    def activity_start(self,a) :
        self.shell('adb shell am start -S -W {}'.format(a),OS=True)
      
        
        
    def PNG_ifin(self,png,BF):
        #print(len(self.opencv_find_list))
        img1=self.an_ScreenShot()
        if BF == False :
            return img1,cv2.imread(png,0)
        if png in self.opencv_find_list :
            return img1,self.opencv_find_list[png]
        else :
            img = cv2.imread(png,0)
            self.opencv_find_list[png] = img
            return img1,img
            
            
        
    def opencv_find(self,png,threshold=0.9,RANDOM=5,BF=True,show=False,tap=False,OS=True):
        img1,img2 = self.PNG_ifin(png,BF)
        y,x = img2.shape
        xy = cv2.matchTemplate(img1,img2,3)
        _,a,_,b = cv2.minMaxLoc(xy)
        if show :
            print('相似度:',png,'  >>>>  ',a)
        if a < threshold or a == 1 :
            if tap == False :
                return False
            e = False
        else :
            result = [b[0]+(x//2),b[1]+(y//2)]
            e = (random.randint(result[0]-int(RANDOM),result[0]+int(RANDOM)),random.randint(result[1]-int(RANDOM),result[1]+int(RANDOM)))
        if tap :
            self.tap(e,OS)
            return
        return e




if __name__ == '__main__' :
    import sys 
    a=Android(37417)
    path=sys.path[0]
    
    #查看已连接
    print('当前连接',a.conn_now())
    
    #执行ADB命令
    print(a.ADB_SHELL('adb get-state'))
    
    #点击
    #a.tap((0,0),RETURN=False,OS=True)
    
    #滑动
    #a.swipe([500,0,500,1500,100],OS=True)
    
    #获取布局
    b=a.get_now_button('termux')
    print(b)
    
    #获取布局截图
    
    if not os.path.exists(path+'/布局信息PNG') :
        os.mkdir(path+'/布局信息PNG')
        a.get_button_png(b,path+'/布局信息PNG')
    
    
    #点击按钮
    a.button_tap(b,'CTRL')

    #获取activity
    #a.activity_get('tv.danmaku.bili')
    
    #启动应用
    #a.activity_start('tv.danmaku.bili/.MainActivityV2')
    #*********几种不同的截图***********
    
    
    
    
    #匹配模板
    T=time.time()
    xy=a.opencv_find(path+'/布局信息PNG/CTRL.png',threshold=0.99,BF=True,show=True,tap=False,OS=True)
    print('匹配',time.time()-T)
    if xy :
        print(xy)
        a.tap(xy,RETURN=False)
        print('点击',time.time()-T)
        
    
    
    
    #普通截图
    img=a.an_ScreenShot()
    cv2.imwrite(path+'/普通截图.png',img)
    #遮罩
    Android.Mask_colcr = 0,0,255 #设置遮罩的颜色,注意是BGR,而不是RGB
    img=a.an_ScreenShot(flags=1,Mask=[0,1000,0,1080])
    cv2.imwrite(path+'/遮罩.png',img)
    #指定大小截图
    img=a.an_ScreenShot(flags=1,Resize=[0,1000,0,1080])
    cv2.imwrite(path+'/指定大小.png',img)
    
    #断开连接
    a.END()