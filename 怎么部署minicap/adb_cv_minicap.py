import os
import re
import cv2
import numpy
import time
import random
import socket
import subprocess 
import xml.etree.ElementTree as el
from multiprocessing import Process,Queue



class minicap(object): 
    minicap_pid = None
    screenshot_a = Queue(1)
    screenshot_b = Queue(1)
    socket_ip = '127.0.0.1'
    socket_port = 4396
    size = None
    def __init__(self) :
        if minicap.size == None :
            raise Exception('未设置屏幕分辨率')
        self.shell('adb forward tcp:{} localabstract:minicap'.format(str(minicap.socket_port)))
        self.shell('adb shell LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -P {}x{}@{}x{}/0'.format(minicap.size[0],minicap.size[1],minicap.size[0],minicap.size[1]))  
        self.header_sum = 0
        while True:
            try:
                self.sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sk.connect((minicap.socket_ip,minicap.socket_port))
                header = self.sk.recv(24)
            except :
                self.header_sum += 1
                if self.header_sum == 10 :
                    raise Exception('SOCKET 连接失败')
                time.sleep(0.2)
                continue
            break
        print('连接成功 :',len(header),self.header_sum)
        print('Version :',header[0])
        print('Size of the header :',header[1])
        minicap.minicap_pid = int.from_bytes(header[2:5],byteorder='little')
        print('Pid of the process :',int.from_bytes(header[2:5],byteorder='little'))
        print('Real display width in pixels :',int.from_bytes(header[6:9],byteorder='little'))
        print('Real display height in pixels :',int.from_bytes(header[10:13],byteorder='little'))
        print('Virtual display width in pixels :',int.from_bytes(header[14:17],byteorder='little'))
        print('Virtual display height in pixels :',int.from_bytes(header[18:21],byteorder='little'))
        print('Display orientation :',header[22])
        print('Quirk bitflags :',header[23])
        
        self.screenshot_run()
        
    def shell(self,a) :
        subprocess.Popen(a,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        
    def mini_screenshot(self,a,b) :
        while True :
            size = self.sk.recv(4)
            size = int.from_bytes(size,byteorder='little')
            img = self.sk.recv(size)
            if not minicap.screenshot_a.empty() :
                a.get()
                if  minicap.screenshot_b.empty() :
                    b.put(img)
            
    def screenshot_run(self) :
        P = Process(target=self.mini_screenshot,args=(minicap.screenshot_a,minicap.screenshot_b))
        P.daemon = True
        P.start()
        
    def screenshot_minicap(self,flags=0) :
        s = False
        while True :
            if minicap.screenshot_a.empty() and s == False :
                minicap.screenshot_a.put(1)
                s = True
            if not minicap.screenshot_b.empty() :
                a = minicap.screenshot_b.get()
                img = numpy.frombuffer(a,numpy.uint8)
                try :
                    img = cv2.imdecode(img,flags=flags)
                except cv2.error :
                    s = False
                    print('cv2.error')
                    continue
                if img is None :
                    s = False
                    print('未知错误')
                    continue
                return img
                    

class Android(object) :
    button = {}
    Mask_colcr = None
    def __init__(self,com,ip='127.0.0.1',MCAP=False,size = None) :
        self.opencv_find_list = {}
        self.MCAP = MCAP
        self.conn = ip+':'+str(com)
        a = self.shell('adb connect '+self.conn,RETURN=True,OS=False,encoding='utf-8')
        print('连接成功 : ',self.conn)
        if 'failed to connect to' in a :
            raise Exception('端口号错误')
        if self.MCAP :
            minicap.size = (size)
            self.scr_cap = minicap()
            T = 3
            while T > -1 :
                print('minicap启动 :',T)
                time.sleep(1)
                T-=1
            
        
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
        
        
    #关闭进程   
    def KILL_PID(self,a) :
        if a :
            print('kill pid :',a)
            self.shell('adb shell kill '+str(a),OS=True)
        
        
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
        if self.MCAP :
            #print('minicap ScreenShot')
            img = self.scr_cap.screenshot_minicap(flags)
        else :
            #print('adb ScreenShot')
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
    '''
    Android()
    37337 :端口号 设置>开发者选项>无线调试>IP和端口号
    MCAP :  True : 使用minicap截图  False : 使用adb截图
    size : 屏幕的大小,需要区分横屏或者竖屏,如果MCAP为False,不用传size
    '''
    
    a=Android(37337,MCAP=True,size=(1080,2520))
    for _ in range(100) :
        T=time.time() 
        img = a.an_ScreenShot()
        print(time.time() - T)
    a.KILL_PID(minicap.minicap_pid)
    a.END()
    