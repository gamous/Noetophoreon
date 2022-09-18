from utils.color import *
import time

def log(log:str):
    logline= bg_blue(f"[{time.strftime('%H:%M', time.localtime())}]",way=SHOW.REVERSE) + bg_blue('[MeteionLog]') + log
    print(logline)