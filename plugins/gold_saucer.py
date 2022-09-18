import meteion
from meteion import do_command
from utils.color import *
import re

activity_repeater_on=False
@meteion.chat_handler("NPCDialogueAnnouncements")
def goldsaucer_activity_repeater(msg_sender,msg_content):
    if not msg_sender=="来宾接待员":
        return
    activity_pattern = re.compile(r"由金碟游乐场主办的活动“(?P<name>.+)”\n正在(?P<loc>.+)进行中。")
    activity=activity_pattern.match(msg_content)
    if not activity:
        return
    if activity_repeater_on:
        do_command(f"/cwl8 金碟活动:{activity['name']}")
