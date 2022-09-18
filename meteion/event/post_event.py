from flask import  request
import meteion

### {Post Handler and Trigger
post_events={}
def post_handler(event):
    return meteion.register(post_events,event)

def fire_post_event(req,event):
    if event not in post_events:
        return
    msg=request.stream.read().decode() if req.method=='POST' else ''
    for func in post_events[event]:
        func(event,msg)
### }Post Handler and Trigger