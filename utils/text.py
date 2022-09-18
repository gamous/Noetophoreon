import re

def clean_partition(text:str):
    text=' '.join(re.split(r'[。，,.|\n]|\s+',text)).strip()
    text=' '.join(re.split(r'\s+',text))
    return text


def clean_close(text:str):
    #close_pattern=re.compile(r"[\(（{《<「【[［]\\[?］]】」>》}）\)]")
    close_strs=["[]",'［］','【】','【/】','「」','<>','《》',r'{}','()','（）']
    for v in close_strs:
        text=text.replace(v,' ')
    return text

control_chars=list(map(chr, list(range(0,32)) + list(range(127,160))))
def clean_control(text:str):
    for v in control_chars:
        text=text.replace(v,' ')
    return text
