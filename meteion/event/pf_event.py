import meteion

### {PF Handler and Trigger
pf_events={}
def pf_handler():
    return meteion.register(pf_events,"*")

def fire_pf_event(pf_item):
    for func in pf_events["*"]:
        func(pf_item)
### }PF Handler and Trigger