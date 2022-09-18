import meteion

### {Chat Handler and Trigger
chat_events={}
def chat_handler(msg_type):
    return meteion.register(chat_events,msg_type)

def fire_chat_event(msg_type,msg_sender,msg_content):
    if msg_type not in chat_events:
        return
    for func in chat_events[msg_type]:
        func(msg_sender,msg_content)
### }Chat Handler and Trigger