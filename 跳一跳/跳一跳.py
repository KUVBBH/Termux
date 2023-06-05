import tyt
import sys
import time
import random
from adb_and_minicap import Android as an
from pywebio import start_server
from pywebio.output import put_text,put_button,clear,put_link


def open_wx() :
    a.activity_start('com.tencent.mm/.ui.LauncherUI')
 
def xl() :
    a.swipe((500,500,500,2000,300))
    
def tb() :
    time.sleep(2)
    xy=a.opencv_find(path+'跳一跳.jpg',threshold=0.959,show=True,tap=True)
    
def game_start() :
    time.sleep(2)
    xy=a.opencv_find(path+'开始.jpg',threshold=0.959,show=True,tap=True)
    
def game_whell() :
    time.sleep(1)
    while True :
        #break
        try :
            time.sleep(random.uniform(0.7,1.2))
            img = a.an_ScreenShot(flags=1)
            T=tyt.time(img)
            x = random.randint(500,1000)
            y = random.randint(1500,2000)
            x1 = random.randint(x-10,x+10)
            y1 = random.randint(y-10,y+10)
           # print(T,TTT,x,y,x1,y1)
            a.swipe((x,y,x1,y1,T),OS=True)
        except :
            a.END()
            break
def run() :
    open_wx()
    time.sleep(5)
    xl()
    tb()
    game_start()
    game_whell()
     
def but2():
    a.ADB_SHELL('adb shell am force-stop com.tencent.mm',OS=True)
    a.ADB_SHELL('adb shell am force-stop com.termux',OS=True)
    
def but() :
    put_text('程序结束请点击关闭;并确保在Termux里面关闭本进程,防止脚本误触!').style('color: red')
    put_text('\n')
    put_text('其中< tyt.py >的源码来自 :')
    put_link('Python微信跳一跳自动化脚本','https://blog.csdn.net/L603409742/article/details/104238820/')
    put_text('\n')
    put_link('真雷神托儿的个人空间-哔哩哔哩','https://b23.tv/SWiGZ8b')
    put_text('\n'*3)
    put_button('开始', onclick=run,color='success', outline=True)
    put_text('\n')
    put_button('关闭', onclick=but2,color='danger', outline=True)
    
 
path=sys.path[0]+'/'

#端口号,设置>开发者选项>无线调试>ip地址和端口
a=an(38397)
time.sleep(0.5)

a.ADB_SHELL('adb shell am start -a android.intent.action.VIEW -d http://127.0.0.1:15280',OS=True)
start_server(but, port=15280,debug=True)


 