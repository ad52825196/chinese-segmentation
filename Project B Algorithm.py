#-------------------------------------------------------------------------------
# Name:        Project B
# Purpose:     Chinese Word Segmentation
#
# Author:      cz
#
# Created:     10/12/2012
# Copyright:   (c) cz 2012
#-------------------------------------------------------------------------------
# UTF-8

import string

def input_string(text):
    list_ch=[]
    for i in range(len(text)):
        list_ch.append(text[i])
    return list_ch

def input_dic(a):
    dic=[]
    lex=open(a,"r")
    for line in lex:
        if line[-1]=="\n":
            dic.append(line[:-1])
        else:
            dic.append(line)
    lex.close()
    return dic

def add_word(a,dic):
    if len(a)>1 and a not in dic:
        dic.append(a)
        word="\n".join(dic)+"\n"
        lex=open("lexicon/dict.txt","w")
        lex.write(word)
        lex.close()
    return dic

def delete_word(a,dic):
    if len(a)>1 and a in dic:
        for i in range(len(dic)):
            if a==dic[i]:
                dic=dic[:i]+dic[i+1:]
                break
        word="\n".join(dic)+"\n"
        lex=open("lexicon/dict.txt","w")
        lex.write(word)
        lex.close()
    return dic

def sentence_seg(a):
    n="1234567890１２３４５６７８９０"
    t=0
    new=[]
    for i in range(len(a)):
        if i==len(a)-1:
            new.append(a[t:i+1])
        elif i+1<len(a) and a[i] in "；。？！" and a[i+1] not in "”’":
            new.append(a[t:i+1])
            t=i+1
        elif i+2<len(a) and a[i]+a[i+1]+a[i+2]=="。’”":
            new.append(a[t:i+3])
            t=i+3
        elif i+1<len(a) and a[i]+a[i+1] in ["。”","。’","","……"]:
            new.append(a[t:i+2])
            t=i+2
        elif a[i] in "，：" and i+1<len(a):
            if a[i+1] not in n or a[i-1] not in n:
                new.append(a[t:i+1])
                t=i+1
        elif a[i]=="\n" or a[i]=="\u3000":
            new.append(a[t:i])
            t=i+1
    s=""
    p=1
    for i in range(len(new)):
        t=""
        for j in range(len(new[i])):
            if new[i][j]!="\n":
                t=t+new[i][j]
        new[i]=t
        if new[i]!="" and new[i]!=" " and new[i]!="  ":
            s=s+"{0}.{1}\n".format(p,new[i])
            p=p+1
    return new,s,p

def one(p,new):
    if p==0:
        return new
    else:
        t=0
        for i in range(len(new)):
            if new[i]!="" and new[i]!=" " and new[i]!="  ":
                t=t+1
            if t==p:
                return [new[i]]
        return new

def first(new,sk):
    sp=0
    for i in range(len(new)):
        if " " in new[i]:# spaces
            j=0
            while j<len(new[i]):
                if sk==0:
                    if new[i][j]==" ":
                        new[i]=new[i][:j]+"|"+new[i][j+1:]
                        sp=1
                        j=j+1
                        while j<len(new[i]) and new[i][j]==" ":
                            new[i]=new[i][:j]+new[i][j+1:]
                else:
                    while j<len(new[i]) and new[i][j]==" ":
                        new[i]=new[i][:j]+new[i][j+1:]
                j=j+1
        j=0# number
        n="1234567890１２３４５６７８９０"
        m="年月日"
        p=",.:，：．"
        while j<len(new[i]):
            if new[i][j] in n:
                t=j
                mark=0
                while new[i][j] in n:
                    j=j+1
                    if j==len(new[i]):
                        new[i]=new[i][:t]+"|"+new[i][t:j]+"|"
                        mark=1
                        break
                    if new[i][j] in m:
                        new[i]=new[i][:t]+"|"+new[i][t:j]+"|"+new[i][j]+"|"+new[i][j+1:]
                        mark=1
                        break
                    if new[i][j] in p:
                        j=j+1
                if mark==0:
                    new[i]=new[i][:t]+"|"+new[i][t:j]+"|"+new[i][j:]
            j=j+1
        j=0# website
        n=string.ascii_lowercase
        m=n+"./:"+string.digits
        while j<len(new[i]):
            if new[i][j] in n:
                t=j
                mark=0
                while new[i][j] in m:
                    j=j+1
                    if j==len(new[i]):
                        new[i]=new[i][:t]+"|"+new[i][t:j]+"|"
                        mark=1
                        break
                if mark==0:
                    new[i]=new[i][:t]+"|"+new[i][t:j]+"|"+new[i][j:]
            j=j+1
        j=0# punctuation
        while j<len(new[i]):
            if new[i][j]=="、":
                new[i]=new[i][:j]+"|"+new[i][j]+"|"+new[i][j+1:]
                j=j+2
            j=j+1
        j=0# devide
        t=0
        k=[]
        if len(new[i])!=0:
            if new[i][-1]!="|":
                new[i]=new[i]+"|"
            while j<len(new[i]):
                if new[i][j]=="|":
                    k.append(new[i][t:j])
                    t=j+1
                j=j+1
            new[i]=k
        j=0# remove
        while j<len(new[i]):
            if new[i][j]=="":
                new[i][j:j+1]=[]
            j=j+1
    return(new,sp)

def cut(new,dic):
    n="1234567890１２３４５６７８９０"+string.ascii_lowercase
    for i in range(len(new)):
        j=0
        while j <len(new[i]):
            if new[i][j][0] not in n and len(new[i][j])!=1:
                (s,t)=rmm(new[i][j],new[i][j][-7:],dic,[])
                t=t[::-1]
                new[i][j:j+1]=[]
                for k in range(len(t)):
                    new[i][j:j]=[t[k]]
                    j=j+1
            else:
                j=j+1
    return new

def rmm(s,s1,dic,t):
    if len(s)==0:
        return s,t
    else:
        if len(s1)==1 or s1=="……" or s1=="——" or s1 in dic:
            t.append(s1)
            s=s[:len(s)-len(s1)]
            rmm(s,s[-7:],dic,t)
            return s,t
        else:
            return rmm(s,s1[1:],dic,t)

def final(new,single_name,double_name,blacklist,whitelist):
    for i in range(len(new)):
        j=0
        while j <len(new[i]):
            if new[i][j] in double_name or new[i][j] in single_name:
                t=j
                j=j+1
                m=0
                p=0
                while m<2 and j<len(new[i]):
                    if len(new[i][j])==1 and new[i][j] not in blacklist:
                        j=j+1
                    elif new[i][j] in whitelist:
                        p=1
                        m=m+1
                        new[i][t:j+1]=[new[i][t]+new[i][t+1]]
                    else:
                        break
                    m=m+1
                j=j-1
                if j-t==1 and p==0:
                    new[i][t:j+1]=[new[i][t]+new[i][t+1]]
                if j-t==2 and p==0:
                    new[i][t:j+1]=[new[i][t]+new[i][t+1]+new[i][t+2]]
                    j=j-2
            j=j+1
    return new

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

def combine(new):
    s=""
    for i in range(len(new)):
        for j in range(len(new[i])):
            s=s+new[i][j]+"|"
        s=s+"\n"
    return s

def rectify(s):
    s=slide("韩|正在","right",1,s)
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
    s=s.replace("无|一|例|外地","无一例外|地")
    s=s.replace("堺|屋|太|一向","堺屋太一|向")
    s=s.replace("每|一|个人","每一个|人")
    return s

def main():
    text=""
    list_ch=input_string(text)
    single_name=input_dic("lexicon/single.txt")
    double_name=input_dic("lexicon/double.txt")
    dic=input_dic("lexicon/dict.txt")
    blacklist=input_dic("lexicon/blacklist.txt")
    whitelist=input_dic("lexicon/whitelist.txt")
    (new,s,p)=sentence_seg(list_ch)
    if p>2:
        p=int(input("Would you like to select one of the above sentences to look at the result of word segmentation?\nIf yes, please input the indicated sentence No.\nIf no, please input 0."))
    new=one(p,new)
    backup=new[:]
    (new,sp)=first(new,0)
    if sp==1:
        if input("Space has been detected.\nDo you want to neglect the space?\n(1=Yes,0=No)")!="0":
            (new,sp)=first(backup,1)
    new=cut(new,dic)
    new=final(new,single_name,double_name,blacklist,whitelist)
    s=combine(new)
    s=rectify(s)

main()