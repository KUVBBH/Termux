import os,sys
import re
import cv2
import numpy
import time
import random
import socket
import subprocess 
from PIL import Image
import xml.etree.ElementTree as el
from multiprocessing import Process,Queue
os.system('pip install pywebio -i https://pypi.tuna.tsinghua.edu.cn/simple')
from pywebio import start_server
from pywebio.output import *
from pywebio.input import *
web_d = {}
path = sys.path[0]

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
        self.shell('adb shell LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -P {}@{}/0'.format(minicap.size,minicap.size))  
        time.sleep(1)
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
        minicap.minicap_pid = int.from_bytes(header[2:5],byteorder='little')
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
    L = ''
    def __init__(self,com,ip='127.0.0.1') :
        self.conn = ip+':'+str(com)
        a = self.shell('adb connect '+self.conn,RETURN=True,OS=False,encoding='utf-8')
        Android.L = a
        
    def shell(self,a,RETURN=True,OS=False,encoding=None) :
        if OS :
            os.system(a)
            return
        data = subprocess.Popen(a,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding=encoding)
        if not RETURN :
            return
        return data.communicate()[0]
    
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


def web_exit() :
    android.KILL_PID(minicap.minicap_pid)
    time.sleep(1)
    os.system('adb shell am force-stop com.termux')
   
def output_scope() :
    put_column([
        put_row([
        put_scope('img_show'),None,
        put_column([
            put_grid([
                [put_button('退出',onclick=web_exit,color='danger')],
                [put_text('size:'),
                put_scope('img_size')],
                
                [put_text('mode:'),
                put_scope('img_mode')],
                
                [put_text('other:'),
                put_scope('other')],
            
                ])
            ])
        ])
    ])
    
def img_show() :
    minicap.size = (web_d['size'])
    cap = minicap()
    time.sleep(1.5)
    clear()
    output_scope()
    while True :
        img = cap.screenshot_minicap(flags=1)
        img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img=Image.fromarray(img)
        clear('img_show')
        put_image(img,scope='img_show')
        clear('img_size')
        put_text(str(img.size),scope='img_size').style('color: red')
        clear('other')
        put_text('这是一个测试',scope='other')
        clear('img_mode')
        put_text(img.mode,scope='img_mode')
        time.sleep(1.5)



def home() :
    global android
    clear()
    put_text('1.请确保Termux已经安装ADB并且已经配对成功')
    put_text('2.确保有以下python库 : numpy,pillow,opencv')
    put_text('3.确保网络能够正常访问GitHub')
    put_text('4.只在Termux(版本 0.118.0)中用过,且未安装系统,其他版本没有测试过')
    put_text('5.确保Termux有文件管理权限')
    put_link('真雷神托儿的个人空间-哔哩哔哩','https://b23.tv/SWiGZ8b')
    put_text('')
    put_link('编译好的<minicap>文件来自Airtest','https://github.com/AirtestProject/Airtest')
    a = input('请输入端口号(设置>开发者选项>无线调试>ip地址和端口)', type=NUMBER)
    android = Android(a)
    
    if 'bad port number' in Android.L or 'failed to connect to' in Android.L :
        clear()
        put_text('端口号错误,请重新输入！').style('color: red;font-size: 40px')
        time.sleep(3)
        home()
    else :
        clear()
        put_text(Android.L)
        time.sleep(1.5)
        
    a = android.ADB_SHELL('adb shell getprop ro.build.version.sdk',RETURN=True,OS=False,encoding='utf-8')
    web_d['sdk'] = a.strip()
    
    a = android.ADB_SHELL('adb shell getprop ro.product.cpu.abi',RETURN=True,OS=False,encoding='utf-8')
    web_d['abi'] = a.strip()
    
    a = android.ADB_SHELL('adb shell wm size',RETURN=True,OS=False,encoding='utf-8')
    a = re.search('\d{3,4}x\d{3,4}+',a).group()
    web_d['size'] = a
    clear()
    git_svn_minicap = 'svn checkout https://github.com/AirtestProject/Airtest/trunk/airtest/core/android/static/stf_libs {}'.format(path+'/libs')
    
    minicap_bin_push = 'adb push {} /data/local/tmp/'.format(path+'/libs/'+web_d['abi']+'/minicap')
    
    minicap_so_push = 'adb push {} /data/local/tmp/'.format(path+'/libs/minicap-shared/aosp/libs/android-'+web_d['sdk']+'/'+web_d['abi']+'/minicap.so')
    
    put_text('下载如果长时间卡住不动,可能是网络问题…')
    put_text('正在下载git-svn…')
    os.system('pkg install git-svn -y')
    
    put_text('正在下载minicap…')
    os.system(git_svn_minicap)
    
    put_text('下载完成')
    
    put_text('PUSH>>>minicap…')
    os.system(minicap_bin_push)
    
    put_text('PUSH>>>minicap.so…')
    os.system(minicap_so_push)
    
    put_text('授权中…')
    os.system('adb shell chmod 777 /data/local/tmp/minicap')
    
    os.system('adb shell chmod 777 /data/local/tmp/minicap.so')
    
    put_text('授权完成')
    img_show()
    
if __name__ == '__main__' :
    print('\n'*50)
    print('请在浏览器打开以下网页: http://localhost:10086/')
    start_server(home,port=10086)

