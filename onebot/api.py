from onebot.config import config

import httpx
import json

def send_private_msg(msg):
    if config["RECV_USER"]==0:return
    url = f"http://127.0.0.1:{config['PORT']}/send_private_msg"
    headers = {
    'content-type': "application/json",
    'authorization': config["AUTHORIZATION"]
    }
    payload = json.dumps({"user_id":config["RECV_USER"],"message":msg})
    return httpx.request("POST", url, data=payload, headers=headers).text