def slide(old_word,direction,length,s):
    if old_word in s:
        if direction=="left":
            length=-length
        new_word=""
        for word in old_word:
            if word!="|":
                new_word+=word
        n=old_word.find("|")
        if 0<n+length<len(new_word):
            new_word=new_word[:n+length]+"|"+new_word[n+length:]
            s=s.replace(old_word,new_word)
        else:
            return s
    return s
def concat(old_word,s):
    if old_word in s:
        new_word=""
        for word in old_word:
            if word!="|":
                new_word+=word
        s=s.replace(old_word,new_word)
    return s

def divide(old_word,position,s):
    if old_word in s:
        new_word=old_word[:position]+"|"+old_word[position:]
        s=s.replace(old_word,new_word)
    return s

def rectify(s):
    s=s.replace("无|一|例|外地","无一例外|地")
    s=s.replace("堺|屋|太|一向","堺屋太一|向")
    s=s.replace("每|一|个人","每一个|人")
    s=slide("生|命中","right",1,s)
    s=slide("黄浦|江畔","right",1,s)
    s=slide("改|造成","right",1,s)
    s=slide("项|目的","right",1,s)
    s=slide("极|大地","right",1,s)
    s=slide("会|期中","right",1,s)
    s=slide("半|年会","right",1,s)
    s=slide("厕|所在","right",1,s)
    s=slide("出|现在","right",1,s)
    s=slide("黄浦|江北","right",1,s)
    return s
