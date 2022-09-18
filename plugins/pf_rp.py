import meteion
from model.roleplay import RolePlayFinder
from app import db

from utils.color import *
from utils import text

from datetime import datetime
import re
from operator import indexOf

### {RolePlayer Filiter
@meteion.pf_handler()
def rp_filter(pf_item):
    # 该正则仅适配鸟区 Only For Chinese LuXingNiao
    # Todo Replace Char https://thewakingsands.github.io/ffxiv-axis-font-icons/

    server_strs = [ '宇宙','宇宙和音',
                    '幻影','幻影群岛',
                    '晨曦','晨曦王座',
                    '沃仙','沃仙曦染',
                    '萌芽','萌芽池',
                    '神意','神意之地',
                    '拉诺','拉诺西亚',
                    '瓜海','红玉海']
    estate_strs = [ '海','海都','海雾村',
                    '沙','沙都','高脚孤丘',
                    '森','森都','薰衣草苗圃',
                    '白','白银','白银乡',
                    '雪','穹顶','穹顶皓天',
                    '雪','山都'
                    ]
    server_str="|".join(server_strs)
    estate_str="|".join(estate_strs)

    loc_pattern=re.compile( r"(?P<server>%s).*?(?P<estate>%s)"
                            r"\D{0,4}(公寓)?"
                            r"(?P<num1>\d{1,2})"
                            r"(非?(扩建)?(公寓)|(区|区?-+)非?(扩建)?(公寓)?)"
                            r"(?P<num2>\d{1,2})(.{0,3}?(号|(个人)?房间)?"
                            r"(?P<room>\d{1,3})?号?(房间)?)?"%(server_str,estate_str))
                            
    loc = loc_pattern.search(pf_item["content"])
    if not loc:return
    locs = loc.group()
    loc = loc.groupdict()
    _server=loc["server"]
    _estate=loc["estate"]
    _num1  =int(loc["num1"])
    _num2  =int(loc["num2"])
    _room  =int(loc["room"]) if loc["room"] else 0

    if "扩建" in locs and "非扩建" not in locs:
        _room=_num2
        _num2=99
    elif "公寓" in locs or "非扩建" in locs:
        _room=_num2
        _num2=00

    if len(_server)>=3:_server= server_strs[indexOf(server_strs,_server) -1]
    if len(_estate)>=2:_estate= estate_strs[(indexOf(estate_strs,_estate))//3 *3]
    
    pf_item["content"] = pf_item["content"].replace(locs,'')
    pf_item["content"] = text.clean_close(pf_item["content"])

    recruit_pattern = re.compile(r"招募?.{0,8}店员|店招|(新店|RP|店员|电源)?招募|(店员)?招新")
    recruit = recruit_pattern.search(pf_item["content"])
    if recruit:
        pf_item["content"] = pf_item["content"].replace(recruit.group(),'')
        pf_item["content"] = text.clean_close(pf_item["content"])

    pf_item["content"]=pf_item["content"].replace('营业中','')

    name_pattern=re.compile(r"(《(?P<name>.{1,18}?)》)|(<(?P<name1>.{1,15}?)>)|(「(?P<name2>.+?)」)|(【(?P<name3>.{1,13}?)】)|(\[(?P<name4>.{1,13}?)\])")
    name = name_pattern.search(pf_item["content"])
    name_str=''
    if name:
        pf_item["content"]=pf_item["content"].replace(name.group(),'')
        pf_item["content"] = text.clean_close(pf_item["content"])
        name = name.groupdict()
        name = name['name'] if name['name'] else name['name1'] if name['name1'] else name['name2'] if name['name2'] else name['name3'] if name['name3'] else name['name4']
        name_str = name.strip()

    #  Tag:轻R 重R 中R
    _tag=[]
    tag_pattern=re.compile(r'摄影棚|咖啡[厅店馆]|酒[吧馆]|搓澡店|异空间|花房|无主动|无接待|拍照|挂机|参观|恋爱|相亲|约会|调情|偷情|团建|小游戏|占卜|指名|牛郎|女仆|花街')
    tag=tag_pattern.findall(pf_item["content"])
    if tag:
        _tag+=tag
    _tag=list(set(tag))

    pf_item["content"] = text.clean_close(pf_item["content"])
    pf_item["content"] = text.clean_partition(pf_item["content"])
    pf_item["content"] = text.clean_control(pf_item["content"])
    pf_item["content"] = text.clean_close(pf_item["content"])

    locs=f"{_server}{_estate}{_num1:02}-{_num2:02}-{_room:02}"
    tags='|'.join(_tag)

    rp_log=RolePlayFinder.query.filter_by(location=locs)
    rp_log = rp_log[0] if rp_log.count()>0 else None
    if not rp_log:
        rp_log=RolePlayFinder(location=locs,update_time=datetime.now(),
                            server=_server,estate=_estate,
                            num1=_num1,num2=_num2,room=_room,
                            #recruit = True if recruit else False,
                            name=name_str,
                            tags=tags,content=pf_item["content"])
        db.session.add(rp_log)
    else:
        if (datetime.now()-rp_log.update_time).days>0:
            rp_log.update_count+=1
        rp_log.update_time=datetime.now()
        rp_log.recruit = True if recruit else False
        rp_log.name=name_str
        rp_log.tags=tags
        rp_log.content=pf_item["content"]

    db.session.commit()
    meteion.log(f"{color('[RolePlayer]',way=CL_REVERSE)}"
                f"{bg_yellow(f'[{locs}]',front=COLOR.BLACK)}"
                + (bg_blue(f'<<{name_str}>>') if name else '')
                + bg_cyan(('[招]'if recruit else '')+tags,front=CL_BLACK)+
                f"{color(pf_item['content'],way=CL_HIGHLIGHT)}")
### }RolePlayer Filiter
