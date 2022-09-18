# Noetophoreon

A Python trigger framework for Dalamud Plugin [PostMeteion](https://github.com/gamous/PostMeteion)

**It's still under development! The data in the database is unreliable because the table structure may be changed in the near future. This project can only be deployed locally because it does not provide any security protection against attacks.**

The triggers in the Plugins folder are for reference only and work only on the CN client.

**Please note that some plugins in plugins are outside the goatcorp specification, and do so at your own risk.**

## Usage

```ps
pip -r requirements.txt
python app.py
```

## Config

Edit app.py

```python
###Config
local_port   = 15000
meteion.config['PORT'] = 12019
onebot.config['PORT']  = 5700
###
```

## Plugin

You can quickly customize a plugin to respond to WebHook events, as follows.

```python
import meteion
from utils.color import *

import re

@meteion.chat_handler('Echo') #register the func to chat_event with chat_type Echo
def something_handler(msg_sender,msg_content):
    hello_pattern = re.compile(r"Hello (?P<name>.+)") #regex to match the content
    hello=hello_pattern.match(msg_content)
    if not hello: return #the guard
	hello=hello.groupdict() #group payload catch
    meteion.do_command(f"/e {hello['name']}") #post a command to meteion
```

This takes effect as long as you save the code in the plugins directory.
