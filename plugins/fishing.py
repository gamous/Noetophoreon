import meteion
from meteion.action import *
from utils.color import *
from plugins.status import player_status
import re,random,time

### {FishingMan
fishing_context={
    "catch_fish":{"total":0},
    "target_fish_count":{"total":0},
    "target_fish":"",
    "auto":False,
    'mooch':False,#以小钓大
    'chum':False,#撒饵
    'patience':True,#耐心
    'mooch_chance':False,
    'cast_on':False,
}

fish_way_presets={
    "碎冰鱼":{
        "auto":False,
        'mooch':False,#以小钓大
        'chum':False,#撒饵
        'patience':False,#耐心
        'mooch_chance':False,
        'cast_on':False,
    },
    "海钓":{
        "auto":False,
        'mooch':False,#以小钓大
        'chum':False,#撒饵
        'patience':True,#耐心
        'mooch_chance':False,
        'cast_on':False,
    },
    "海钓-幻海流":{
        "auto":False,
        'mooch':False,#以小钓大
        'chum':False,#撒饵
        'patience':False,#耐心
        'mooch_chance':False,
        'cast_on':False,
    }

}

def fish_apply_preset(preset:str):
    if preset not in fish_way_presets:return
    preset=fish_way_presets[preset]
    for item in preset:
        if item in fishing_context:
            fishing_context[item]=preset[item]
            do_command(f'/e  - {item}:{fishing_context[item]}')
    do_command('/e AutoFishing Preset Applied')

def foolish(min=300,max=2000):
    time.sleep(random.randint(*(min,max))/1000)

@meteion.chat_handler("Echo")
def fishing_config_handler(_,msg:str):
    if msg.startswith("af"):
        msg=msg.split()
    else:
        return
    msg_count=len(msg)
    if msg_count<=1:
        do_command('/e AutofishHelp: af catch|off|on|on {target_num}')
        return
    match msg[1]:
        case "on":
            if(msg_count>=3) and msg[2].isnumeric():
                fishing_context["target_fish_count"]["total"]=int(msg[2])
                fishing_context["catch_fish"]={}
            fishing_context["auto"]=True
            do_command(f'/e AutoFishing ON {fishing_context["target_fish_count"]["total"]}')
        case "off":
            fishing_context["auto"]=False
            do_command('/e AutoFishing OFF')
        case "go":
            fish_cast()
        case "use":
            if(msg_count<3):return
            fish_apply_preset(msg[2])
        case "conf":
            do_command('/e AutoFishing Config')
            do_command(f'/e  - 自动:{fishing_context["auto"]}')
            do_command(f'/e  - 以小钓大:{fishing_context["mooch"]}')
            do_command(f'/e  - 撒饵:{fishing_context["chum"]}')
            do_command(f'/e  - 耐心:{fishing_context["patience"]}')
        case "catch":
            do_command(f'/e FishCatch ({fishing_context["catch_fish"]["total"]})')
            for fish in fishing_context["catch_fish"]:
                do_command(f'/e  - {fish}:{fishing_context["catch_fish"][fish]}')

@meteion.post_handler("heartbeat")
def fish_auto_checker(_,__):
    if fishing_context["auto"] and not fishing_context["cast_on"]:
        fish_cast()

@meteion.chat_handler("Debug")
def fish_bite_handler(msg_sender,msg_content):
    bite_pattern = re.compile(r"\[FishNotify\] You hook a fish with a (?P<tug_strength>.+) bite.")
    bite=bite_pattern.match(msg_content)
    if not bite:
        return
    tug_strength=bite.groupdict()['tug_strength']
    foolish(500,800)
    fish_hook(tug_strength)


@meteion.chat_handler("0843")#fish action
def fish_catch_handler(_,msg_content):
    catch_pattern = re.compile(r"(?P<player>.+)成功钓上了(?P<item_name>.+)（(?P<size>.+)星寸）。")
    catch = catch_pattern.match(msg_content)
    if not catch:return
    catch=catch.groupdict()
    if "name" not in player_status:player_status["name"]=PlayerName()
    if catch['player']!=player_status["name"]:
        return

    if catch['item_name'] not in  fishing_context["catch_fish"]:
        fishing_context["catch_fish"][catch['item_name']]=0
    fishing_context["catch_fish"]["total"]+=1
    fishing_context["catch_fish"][catch['item_name']]+=1
    if fishing_context["target_fish_count"]["total"]>1 and fishing_context["catch_fish"]["total"]>fishing_context["target_fish_count"]["total"]:
        fishing_context["auto"]=False
        return
    fishing_context["cast_on"]=False
    fish_cast()

@meteion.chat_handler("0843")
def fish_cast_handler(_,msg_content):
    cast_pattern = re.compile(r"(?P<player>.+)在(?P<location>.+)甩出了鱼线开始钓鱼。")
    cast = cast_pattern.match(msg_content)
    if not cast:return
    cast=cast.groupdict()
    if "name" not in player_status:player_status["name"]=PlayerName()
    if cast['player']!=player_status["name"]:
        return
    fishing_context["cast_on"]=True
##

@meteion.chat_handler("0843")
def fish_mooch_handler(_,msg_content):
    mooch_pattern=re.compile(r"以小钓大的机会！")
    mooch=mooch_pattern.match(msg_content)
    if not mooch:return
    fishing_context["mooch_chance"]=True

def fish_cast_fallback():
    do_command('/ac 抛竿')
def fish_hook_fallback(tug_strength):
    do_command("/ac 提钩")

def fish_cast():
    #目标鱼/专一/
    gp=int(do_query('gp').split('/')[0])
    buff=do_query('gp').split('|')
    if fishing_context["mooch_chance"] and fishing_context["mooch"]==True:
        do_command("/ac 以小钓大")
        fishing_context["mooch_chance"]=False
        return
    if fishing_context["patience"]==True \
        and ("提钩成功率降低" not in buff) and gp>=250:
        gp-=250
        foolish(600,600)
        do_command("/ac 耐心")
        foolish(600,600)
    if fishing_context["chum"]==True \
        and "撒饵" not in buff and gp>=150:
        foolish(600,600)
        do_command("/ac 撒饵")
        foolish(600,600)
    foolish()
    do_command('/ac 抛竿')

def fish_hook(tug_strength):
    gp=int(do_query('gp').split('/')[0])
    buff=do_query('gp').split('|')
    if "提钩成功率降低" not in buff:
        match tug_strength:
            case 'light':
                do_command("/ac 精准提钩")
            case 'medium':
                do_command("/ac 强力提钩")
            case 'heavy':
                do_command("/ac 强力提钩")
    do_command("/ac 提钩")

#08c3 有鱼上钩了！

##Echo 定时断杆
#08c3][Sender:]附近的鱼已经有所警惕了。最好换个位置试试。a
@meteion.chat_handler("0843")#fish action
def fish_warn_handler(_,msg_content):
    warn_pattern = re.compile(r"这里的鱼现在警惕性很高，看来还是换个地点比较好。")
    warn = warn_pattern.match(msg_content)
    if not warn:return
    meteion.log(bg_yellow("WARN",front=COLOR.BLACK)+'[Fish]警惕')
    do_command("/ac 中断")

@meteion.chat_handler("08c3")#fish action
def fish_flee_handler(msg_sender,msg_content):
    flee_pattern = re.compile(r"上钩的鱼逃走了……")
    flee_pattern1 = re.compile(r"鱼带着(?P<bite>.+)逃走了……")#
    flee = flee_pattern.match(msg_content)
    flee1 = flee_pattern1.match(msg_content)
    if not flee and not flee1:return
    foolish(600,1000)
    fish_cast()

#08c3 没有钓到任何东西……  选饵
#08c3 不经意间鱼饵被吃掉了…… 超时

##ocean fishing
@meteion.chat_handler("NPCDialogueAnnouncements")#fish action
def fish_spectral_current_handler(msg_sender,msg_content):
    if not msg_sender == "福尔扎吉尔":
        return
    spectral_current_pattern=re.compile(r"难道是(?P<player>.+)钓到的鱼带来的影响吗？！\n幻海流要来了！！")
    spectral_current_pattern1=re.compile(r"多亏了(?P<player>.+)，马上就要发生幻海流了！\n真厉害，这可是爆钓的好机会啊！")
    spectral_current_pattern2=re.compile(r"看来(?P<player>.+)幸运地钓到了啊！\n幻海流马上就要发生了！")
    spectral_current = spectral_current_pattern.match(msg_content)
    spectral_current1 = spectral_current_pattern1.match(msg_content)
    spectral_current2 = spectral_current_pattern2.match(msg_content)
    if not spectral_current and not spectral_current1 and not spectral_current2:return
    do_command('/ac 中断')
    fish_apply_preset("海钓-幻海流")
    foolish(1800,2000)#<player>收回了鱼线。
    fish_cast()
    

#https://ngabbs.com/read.php?tid=25905000&rand=327
#即将前往下一个海域！\n请做好移动的准备，收起鱼竿！#30s
#好了，拔锚起航！\n出发前往下一个海域！#0s
@meteion.chat_handler("NPCDialogueAnnouncements")#fish action
def fish_arrive_handler(msg_sender,msg_content):
    if not msg_sender == "福尔扎吉尔":
        return
    arrive_pattern=re.compile(r"到达(?P<location>.+)了！\n大家努力，争取钓多点啊！")
    arrive = arrive_pattern.match(msg_content)
    if not arrive:return
    do_command('/ac 选饵')
    foolish(1000,3000)
    fish_apply_preset("海钓")
    fish_cast()
    
##[Type:0043][Sender:]从海里感知到了凶暴的气息！
##[Type:0043][Sender:]凶暴的气息消失了……

#出现海鸥群的话，\n就证明大鱼正聚集在一起。
#海豚游到努力号周围了啊，\n那说不定海豚群就快要出现了。
#海豚群过来了！\n这可是好兆头！


#哈哈！\n好壮观的鱼群！

## 切换场景hook

### }FishingMan