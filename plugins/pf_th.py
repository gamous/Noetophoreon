import meteion
from utils.color import *
from utils import text

import re

### {TreasureHunter_Filter
@meteion.pf_handler()
def th_filter(pf_item):
    ###type和价格分开匹配
    info_pattern=re.compile(r"[gG](?P<map_type>\d{1,2})\D+(?P<map_count>\d{1,2})图底?(?P<price>\d{1,2})[wW万]?(?P<res>\D.+)")
    info = info_pattern.search(pf_item["content"])
    if not info:return
    info=info.groupdict()
    map_count=int(info['map_count'])
    price    =int(info['price'])
    res      =text.clean_partition(info['res'])
    meteion.log(f"{bg_yellow('[TreasureHunt]',front=CL_WHITE)}"
        +color(f"[{info['map_type']}][Count:{map_count:02}]",way=CL_REVERSE)
        +bg_yellow( f"[Price:{price/map_count:.2f}/map]",front=CL_RED)
        +F"[{pf_item['player']}]{res}")
### }TreasureHunter_Filter