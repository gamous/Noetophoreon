from meteion.logger import *
from utils.color import *

def register(target:dict,event:str):
    def decorate(func):
        if event not in target:
            target[event]=[]
        target[event].append(func)
        log(f"{bg_cyan('[ModuleManger]')}{func.__name__} register on {event}")
        def wrapper(msg):
            func(msg)
        return wrapper
    return decorate