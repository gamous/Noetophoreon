import meteion.config
import httpx

### {Dalamud
#https://ff14.huijiwiki.com/wiki/%E6%96%87%E6%9C%AC%E6%8C%87%E4%BB%A4

def do_command(cmd):
    url = f"http://localhost:{meteion.config['PORT']}/command/"
    return httpx.request("POST", url, data=str(cmd)).text
def do_query(query):
    url = f"http://localhost:{meteion.config['PORT']}/query/"
    return httpx.request("POST", url, data=str(query)).text

def do_place(waymark):
    url = f"http://localhost:{meteion.config['PORT']}/place/"
    return httpx.request("POST", url, data=str(waymark)).text

def action(action_name):
    return do_command('/ac'+action_name)
def blue_action(action_name):
    return do_command('/blueaction'+action_name)
def pvp_action(action_name):
    return do_command('/pvpac'+action_name)
def addpvp_action(action_name):
    return do_command('/apa'+action_name)
def g_action(action_name):
    return do_command('/gaction'+action_name)
def ride(num):
    return do_command(f'/ridepillion <{num}> 1')
def logout():
    return do_command(f'/logout')
def shutdown():
    return do_command(f'/shutdown')

def IsLoggedIn():
    return do_query('login')
def LocalContentID():
    return do_query('cid')
def CurrentWorld():
    return do_query('currentworld')
def HomeWorld():
    return do_query('homeworld')
def ObjectID():
    return do_query('oid')
def TargetObjectID():
    return do_query('tid')
def PlayerNameID():
    return do_query('nid')
def PlayerName():
    return do_query('name')
def Job():
    return do_query('job')
def HP():
    return do_query('hp')
def MP():
    return do_query('mp')
def GP():
    return do_query('gp')
def CP():
    return do_query('cp')
def Buff():
    return do_query('buff')
def Position():
    return do_query('pos')
def Rotation():
    return do_query('rot')
def PlayerWhere():
    return do_query('where')
def Coord():
    return do_query('coord')
### }Dalamud