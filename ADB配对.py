import re
import os
import time
import pytesseract
from PIL import Image

path=input('''
原理 :
监控截图文件夹，当该文件夹新增文件后,
识别上面的内容,然后配对.

打开以下界面:

设置>开发者选项>无线调试>使用配对码配对设备

然后截图，等待完成,配对完成.

如果长时间没有反应，那就是不出意外的出了意外,'CTRL+4'退出死循环

请输入需要监控的文件夹(必须是保存截图的文件夹)>>>''')

dir_list=None
while True :
    time.sleep(0.1)
    if dir_list == None:
        dir_list = os.listdir(path)
    now_list=os.listdir(path)
    if len(now_list) > len(dir_list) :
        time.sleep(1)
        now_list=os.listdir(path)
        for  i in now_list :
            if i not in dir_list :
                new_path=path+'/'+i
                img= Image.open(new_path)
                s = pytesseract.image_to_string(img)
                ip_list = re.search('[:]\d{4,6}',s).group()
                pin = re.search('\d{6,6}',s).group()
                global cmd
                cmd = 'adb pair 127.0.0.1'+ip_list+' '+pin
                print(cmd)
                break
        break
os.system(cmd)

