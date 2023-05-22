import os
import sys 
import time
from adb_cv import Android as an

a=an(43293)
#启动APP
a.activity_start('tv.danmaku.bili/.MainActivityV2')

#sleep 3s 确保后面的代码执行时,当前页是我们需要的页面
time.sleep(3)

#这里'BL'没有什么实际意义,只是作为an.button的key
#an.button是一个字典,里面存放着本次脚本所有获取过的页面布局信息
#get_now_button()得到结果是一个字典

button=a.get_now_button('BL')

def 获取按钮的截图() :
    path=sys.path[0]+'/界面布局截图'
    if not os.path.exists(path) :
        os.mkdir(path)
    a.get_button_png(button,path)



#点击<我的>按钮
a.tap(button['我的'])

获取按钮的截图()    #  <<<<<<  这是个函数,不是注释



#END()断开ADB链接
time.sleep(3)
a.END()