from enum import Enum

class COLOR(Enum):
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    PURPLE = 5
    CYAN = 6
    WHITE = 7

class SHOW(Enum):
    DEFAULT = 0
    HIGHLIGHT = 1
    UNDERLINE = 4
    REVERSE = 7

CL_BLACK=COLOR.BLACK
CL_RED=COLOR.RED
CL_GREEN=COLOR.GREEN
CL_YELLOW=COLOR.YELLOW
CL_BLUE=COLOR.BLUE
CL_PURPLE=COLOR.PURPLE
CL_CYAN=COLOR.CYAN
CL_WHITE=COLOR.WHITE

CL_DEFAULT = SHOW.DEFAULT
CL_HIGHLIGHT = SHOW.HIGHLIGHT
CL_UNDERLINE = SHOW.UNDERLINE
CL_REVERSE = SHOW.REVERSE

def color(msg:str,front:COLOR=COLOR.WHITE,background=COLOR.BLACK,way=SHOW.DEFAULT):
    return f"\033[{front.value+30};{background.value+40}{';'+str(way.value)if way.value else ''}m{msg}\033[0m"

def bg_black(msg:str,front:COLOR=COLOR.WHITE,way=SHOW.DEFAULT):
    return color(msg,front,COLOR.BLACK,way)
def bg_red(msg:str,front:COLOR=COLOR.WHITE,way=SHOW.DEFAULT):
    return color(msg,front,COLOR.RED,way)
def bg_green(msg:str,front:COLOR=COLOR.WHITE,way=SHOW.DEFAULT):
    return color(msg,front,COLOR.GREEN,way)
def bg_yellow(msg:str,front:COLOR=COLOR.WHITE,way=SHOW.DEFAULT):
    return color(msg,front,COLOR.YELLOW,way)
def bg_blue(msg:str,front:COLOR=COLOR.WHITE,way=SHOW.DEFAULT):
    return color(msg,front,COLOR.BLUE,way)
def bg_puple(msg:str,front:COLOR=COLOR.WHITE,way=SHOW.DEFAULT):
    return color(msg,front,COLOR.PURPLE,way)
def bg_cyan(msg:str,front:COLOR=COLOR.WHITE,way=SHOW.DEFAULT):
    return color(msg,front,COLOR.CYAN,way)
def bg_white(msg:str,front:COLOR=COLOR.WHITE,way=SHOW.DEFAULT):
    return color(msg,front,COLOR.WHITE,way)

def ft_black(msg:str,background:COLOR=COLOR.BLACK,way=SHOW.DEFAULT):
    return color(msg,COLOR.BLACK,background,way)
def ft_red(msg:str,background:COLOR=COLOR.BLACK,way=SHOW.DEFAULT):
    return color(msg,COLOR.RED,background,way)
def ft_green(msg:str,background:COLOR=COLOR.BLACK,way=SHOW.DEFAULT):
    return color(msg,COLOR.GREEN,background,way)
def ft_yellow(msg:str,background:COLOR=COLOR.BLACK,way=SHOW.DEFAULT):
    return color(msg,COLOR.YELLOW,background,way)
def ft_blue(msg:str,background:COLOR=COLOR.BLACK,way=SHOW.DEFAULT):
    return color(msg,COLOR.BLUE,background,way)
def ft_puple(msg:str,background:COLOR=COLOR.BLACK,way=SHOW.DEFAULT):
    return color(msg,COLOR.PURPLE,background,way)
def ft_cyan(msg:str,background:COLOR=COLOR.BLACK,way=SHOW.DEFAULT):
    return color(msg,COLOR.CYAN,background,way)
def ft_white(msg:str,background:COLOR=COLOR.BLACK,way=SHOW.DEFAULT):
    return color(msg,COLOR.WHITE,background,way)