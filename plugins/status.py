import meteion
from meteion.action import do_command
from utils.color import *

### {Status Sync
player_status={}
@meteion.post_handler("heartbeat")
def status_sync(_,__):
    try:
        player_status["where"]=meteion.PlayerWhere()
        player_status["name"]=meteion.PlayerName()
    except Exception as e:
        meteion.log(bg_red("[ERROR]")+f'[StatusSync]{e}')
### }Status Sync