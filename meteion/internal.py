import meteion
from meteion.chat_type import *
from model.chatlog import ChatLog
from app import db

from utils.color import *

from datetime import datetime

### {Basic Event Handler
@meteion.post_handler("heartbeat")
def print_message(_,__):
    pass
    #meteion.log(bg_red('[HeartBeat]'))

pf_list={}
@meteion.post_handler("partyfinder")
def print_pf_message(_,raw):
    msg=raw.split("|")
    if len(msg)<6:
        return
    pf_item={"id":msg[0],"player":msg[1],"world":msg[2],"duty":msg[3],"time":msg[4],"content":msg[5]}
    meteion.fire_pf_event(pf_item)
    if pf_item["id"] in pf_list:
        pf_list[pf_item["id"]]=pf_item
        return
    pf_list[pf_item["id"]]=pf_item
    #meteion.log(f"{color('[Partyfinder]',way=CL_REVERSE)}{raw}")

@meteion.post_handler("chat")
def print_chat_message(_,msg):
    msg=msg.split("|")
    if len(msg)<3:
        return
    msg_type= msg[0]
    msg_type = msg_type if not msg_type.isnumeric() else f"{int(msg_type):04x}"
    msg_sender=msg[1]
    msg_content=msg[2]
    #
    chat_log=ChatLog(type=msg_type,sender=msg_sender,content=msg_content)
    db.session.add(chat_log)
    db.session.commit()
    #
    meteion.fire_chat_event(msg_type,msg_sender,msg_content)
    msg_log_level=chat_type_level[msg_type] if msg_type in chat_type_level else chat_type_level["unknown"]
    if msg_log_level < 5:
        meteion.log(bg_green('[ChatBox]')+ f"[Type:{msg_type}][Sender:{msg_sender}]{msg_content}")
### }Basic Event Handler