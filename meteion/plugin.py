import importlib,os

import meteion
from utils.color import *

def load_all_plugins():
    plugins=os.listdir(os.getcwd()+'\plugins')
    for plugin in plugins:
        if plugin.endswith(".py"):
            plugin_name=plugin[:-3]
            try:
                importlib.import_module(f"plugins.{plugin_name}", package=None)
                meteion.log(f"{bg_puple('[PluginManger]')}{plugin_name} loaded")
            except e:
                meteion.log(bg_red("[ERROR]")+'[Plugin]{e}')