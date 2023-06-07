import re,time,os#,hashlib
try :
    from pywebio import start_server
except :
    os.system('pip install pywebio -i https://pypi.tuna.tsinghua.edu.cn/simple')
    import sys
    sys.exit()
from multiprocessing import Process,Manager,Queue
from pywebio.input import input,NUMBER,input_group,actions
from pywebio.output import put_text,put_buttons,clear,toast,put_button,put_link,put_code

#存档的路径
data_path = '/storage/emulated/0/Download/Brotato/user/save.json'
#网页端口
web_port = 4397

td_path = '/data/data/com.termux/files/usr/etc/profile.d/tdxd.sh'
RUN = Queue(1)
manager = Manager()
manager_l = manager.list([False])
    
def str_in(a,b) :#要查找，被查找
    s = '\\W'+a+'\\W{2,3}\\d+'
    f = re.search(s,b)
    try :
        r = f.span(),f.group()
        return r
    except :
        return None

def str_modify(a,b,data) : #内容,位置,原字符串
    c = data[b[0]:b[1]]
    d = re.search('-?\d+',c).group()
    #print(d)
    return data[:b[1]-len(d)]+a+data[b[1]:]
    
    
def td_help() :
    clear()
    put_link('真雷神托儿的个人空间-哔哩哔哩','https://b23.tv/SWiGZ8b')
    put_button('返回', onclick=web_1,color='success', outline=True)
    put_text('游戏版本 :  0.8.0.3HF2')
    put_text('刷新 : 手动刷新页面(此脚本在一个循环里面监控存档的变化，每次读取存档间隔5s,所以刷新的时间间隔应在5s以上)')
    put_text('复活 : 死亡后复活')
    put_text('*存档数值修改的属性并不全,可以在web_1函数中，按照格式自行添加')
    put_code('''input(<表格显示的名字>, name=<文件save.json中的值>,value=re.search('\d+',str_in(<文件save.json中的值>,manager_l[-1])[1]).group(),type=NUMBER)''')
    put_text('!注意 : 修改前先关掉游戏,修改后再打开游戏').style('color: red')
    
def but(set_value) :
    if set_value == '刷新' :
        web_1()
    elif set_value == '复活' :
        data = manager_l[-1]
        with open(data_path,'w') as f :
            f.write(data)
        toast('复活成功，当前界面5秒后刷新',duration=5)
        time.sleep(5.5)
        web_1()
    elif set_value == '退出' :
        import os,signal
        os.kill(RUN.get(),signal.SIGTERM)
        os.kill(os.getpid(),signal.SIGTERM)
    elif set_value == '帮助' : 
        td_help()
    elif set_value == '打开Termux自动启动' :
        with open(td_path,'r') as f :
            QWER = f.read()
        #print(QWER,len(QWER))
        if len(QWER) > 1 :
            with open(td_path,'w') as f :
                f.write('')
            toast('已关闭>>>下次打开Termux[无事发生]',duration=0)
        else :
            with open(td_path,'w') as f :
                f.write('sleep 1\npython '+__file__)
            toast('已开启>>>下次打开Termux[自启动]',duration=0)
        web_1()
    

def web_1() :
    clear()
    put_buttons(['刷新', '复活', '退出','帮助','打开Termux自动启动'], onclick=but,outline=True)
    if manager_l[0] :
        info = input_group('当前存档数值修改',[
        input('货币', name='gold',value=re.search('\d+',str_in('gold',manager_l[-1])[1]).group(),type=NUMBER),
    
        input('HP', name='stat_max_hp',value=re.search('\d+',str_in('stat_max_hp',manager_l[-1])[1]).group(),type=NUMBER),
    
        input('近战伤害', name='stat_melee_damage',value=re.search('\d+',str_in('stat_melee_damage',manager_l[-1])[1]).group(),type=NUMBER),
    
        input('远程伤害', name='stat_ranged_damage',value=re.search('\d+',str_in('stat_ranged_damage',manager_l[-1])[1]).group(),type=NUMBER),
    
        input('闪避', name='stat_dodge',value=re.search('\d+',str_in('stat_dodge',manager_l[-1])[1]).group(),type=NUMBER),
    
        input('范围', name='stat_range',value=re.search('\d+',str_in('stat_range',manager_l[-1])[1]).group(),type=NUMBER),
    
        input('攻击速度', name='stat_attack_speed',value=re.search('\d+',str_in('stat_attack_speed',manager_l[-1])[1]).group(),type=NUMBER),
    
        input('元素伤害', name='stat_elemental_damage',value=re.search('\d+',str_in('stat_elemental_damage',manager_l[-1])[1]).group(),type=NUMBER),
    
        input('速度', name='stat_speed',value=re.search('\d+',str_in('stat_speed',manager_l[-1])[1]).group(),type=NUMBER),
    
        input('暴击', name='stat_crit_chance',value=re.search('\d+',str_in('stat_crit_chance',manager_l[-1])[1]).group(),type=NUMBER),
    
        input('幸运', name='stat_luck',value=re.search('\d+',str_in('stat_luck',manager_l[-1])[1]).group(),type=NUMBER),
    
        input('护甲', name='stat_armor',value=re.search('\d+',str_in('stat_armor',manager_l[-1])[1]).group(),type=NUMBER),
    
        input('收获', name='stat_harvesting',value=re.search('\d+',str_in('stat_harvesting',manager_l[-1])[1]).group(),type=NUMBER),
    
        input('经验', name='xp_gain',value=re.search('\d+',str_in('xp_gain',manager_l[-1])[1]).group(),type=NUMBER),
    
    
        input('生命再生', name='stat_hp_regeneration',value=re.search('\d+',str_in('stat_hp_regeneration',manager_l[-1])[1]).group(),type=NUMBER),
    
    
        input('等级', name='current_level',value=re.search('\d+',str_in('current_level',manager_l[-1])[1]).group(),type=NUMBER),
        
        input('当前已过关数', name='current_wave',value=re.search('\d+',str_in('current_wave',manager_l[-1])[1]).group(),type=NUMBER),
        
    ])
        data = manager_l[-1]
        for i in info :
            v = info[i]
            w = str_in(i,data)
            data = str_modify(str(v),w[0],data)
        with open(data_path,'w') as f :
            f.write(data)
        toast('修改成功，当前界面5秒后刷新',duration=5)
        time.sleep(5.5)
        web_1()


def read_date(a,q) :
    #md5_data = ''
    while True :
        if q.empty() :
            q.put(os.getpid())
        #print(len(a),a[0])
        with open(data_path,'r') as f :
            data = f.read()
        try :
            hp = re.search('\d+',str_in('stat_max_hp',data)[1]).group()
        except :
            hp = 0
            a[0] = False
        if int(hp) >= 1 :
            a[0] = True
            #md5hash = hashlib.md5(data.encode())
            #md5 = md5hash.hexdigest()
            #print(md5_data,md5,len(a))
            #if md5 != md5_data :
                #md5_data = md5
            a.append(data)
        if len(a) > 3 : #10
            a.pop(1)   
            
        time.sleep(5)
        

if not os.path.exists(td_path) :
    print('TD_PATH')
    with open(td_path,'w') as f :
        f.write('')
P = Process(target=read_date,args=(manager_l,RUN))
P.daemon = True
P.start()
#P.join()
time.sleep(1)
print('请在浏览器打开以下网页:127.0.0.1:'+str(web_port))
start_server(web_1, port=web_port,debug=True)


