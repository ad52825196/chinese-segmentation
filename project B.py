#-------------------------------------------------------------------------------
# Name:        Project B
# Purpose:     Chinese Word Segmentation
#
# Author:      destiny
#
# Created:     10/12/2012
# Copyright:   (c) cz 2012
#-------------------------------------------------------------------------------
# UTF-8

from tkinter import*
from tkinter.simpledialog import*
import threading
import string
from tkinter.filedialog import*
from tkinter.messagebox import*
from rule import*
from codecs import*

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
        j=0# punctuation
        while j<len(new[i]):
            if new[i][j]=="、":
                new[i]=new[i][:j]+"|"+new[i][j]+"|"+new[i][j+1:]
                j=j+2
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
        if i<len(new)-1:
            if i%3==1:
                status.set("正在处理..")
            if i%3==2:
                status.set("正在处理....")
            if i%3==0:
                status.set("正在处理......")
            result.delete(1.0,END)
            result.insert(END,"请稍候...\n已完成{:.2f}%".format((i+1)/len(new)*100))
        if i==len(new)-1:
            result.delete(1.0,END)
            status.set("已完成")
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
def cut2(new,dic):
    n="1234567890１２３４５６７８９０"+string.ascii_lowercase
    for i in range(len(new)):
        if i<len(new)-1:
            if i%3==1:
                status.set("Running..")
            if i%3==2:
                status.set("Running....")
            if i%3==0:
                status.set("Running......")
            result.delete(1.0,END)
            result.insert(END,"Please Wait...\nHave already done {:.2f}%".format((i+1)/len(new)*100))
        if i==len(new)-1:
            result.delete(1.0,END)
            status.set("Over")
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





def combine(new):
    s=""
    for i in range(len(new)):
        for j in range(len(new[i])):
            s=s+new[i][j]+"|"
        s=s+"\n"
    return s
def main():
    text=entry.get(1.0,END)
    list_ch=input_string(text)
    (new,s,p)=sentence_seg(list_ch)
    if p>2:
        p=simpledialog.askinteger("史上最简洁有效分词工具","请输入要进行分词的句子序号\n(分句后可得),默认值为第一句",minvalue=1,maxvalue=p-1,initialvalue="1")
        if p==None:
            p=1
    new=one(p,new)
    backup=new[:]
    (new,sp)=first(new,0)
    if sp==1:
        if messagebox.askquestion("史上最简洁有效分词工具","检测到该语料有空格,是否忽略词间的空格?")==YES:
            (new,sp)=first(backup,1)
    new=cut(new,dic)
    new=final(new,single_name,double_name,blacklist,whitelist)
    s=combine(new)
    s=rectify(s)
    result.delete(1.0,END)
    result.insert(END,s)
def main2():
    text=entry.get(1.0,END)
    list_ch=input_string(text)
    (new,s,p)=sentence_seg(list_ch)
    if p>2:
        p=0
    new=one(p,new)
    backup=new[:]
    (new,sp)=first(new,0)
    if sp==1:
        if messagebox.askquestion("史上最简洁有效分词工具","检测到该语料有空格,是否忽略词间的空格?")==YES:
            (new,sp)=first(backup,1)
    new=cut(new,dic)
    new=final(new,single_name,double_name,blacklist,whitelist)
    s=combine(new)
    s=rectify(s)
    result.delete(1.0,END)
    result.insert(END,s)
def main3():
    text=entry.get(1.0,END)
    list_ch=input_string(text)
    (new,s,p)=sentence_seg(list_ch)
    if p>2:
        p=simpledialog.askinteger("A Powerful Tool","Please input the number of the sentence\n(You can get it by cutting sentences)\nDefault is the first one",minvalue=1,maxvalue=p-1,initialvalue="1")
        if p==None:
            p=1
    new=one(p,new)
    backup=new[:]
    (new,sp)=first(new,0)
    if sp==1:
        if messagebox.askquestion("A Powerful Tools","Spaces are detected\nDo you want to neglect those between words?")==YES:
            (new,sp)=first(backup,1)
    new=cut2(new,dic)
    new=final(new,single_name,double_name,blacklist,whitelist)
    s=combine(new)
    s=rectify(s)
    result.delete(1.0,END)
    result.insert(END,s)
def main4():
    text=entry.get(1.0,END)
    list_ch=input_string(text)
    (new,s,p)=sentence_seg(list_ch)
    if p>2:
        p=0
    new=one(p,new)
    backup=new[:]
    (new,sp)=first(new,0)
    if sp==1:
        if messagebox.askquestion("A Powerful Tools","Spaces are detected\nDo you want to neglect those between words?")==YES:
            (new,sp)=first(backup,1)
    new=cut2(new,dic)
    new=final(new,single_name,double_name,blacklist,whitelist)
    s=combine(new)
    s=rectify(s)
    result.delete(1.0,END)
    result.insert(END,s)
def us():
    us=Tk()
    us.title("关于史上最简洁有效分词工具")
    us.minsize(400,300)
    us.maxsize(400,300)
    class App:
        def __init__(self, master):
            global fram
            fram= Frame(master)
            fram.pack()
            Label(fram,text = '版本信息：',).grid(row=1,sticky=W)
            Label(fram,text = '版本号：分词 5.1.0 beta').grid(row=2,sticky=W)
            Label(fram,text = '运行环境：Windows系统',).grid(row=3,sticky=W)
            Label(fram,text = '支持语言：简体中文，英文',).grid(row=4,sticky=W)
            Label(fram,text = '运行平台：python 3.2.3',).grid(row=5,sticky=W)
            Label(fram,text = '发布时间：2013，01,03',).grid(row=6,sticky=W)
            Label(fram,text = '开发人员：陈桢，袁全宁，李健达，刘柏辰。',).grid(row=7,sticky=W)
            Label(fram,text = 'All rights reserved 2012-2013',).grid(row=8,sticky=W)
    class Cpp:
        def __init__(self, master):
            global frame
            frame= Frame(master)
            frame.pack()
            Label(frame,text = '联系我们：',).grid(row=1,sticky=W)
            Label(frame,text = '如果您有任何问题请联系我们：').grid(row=2,sticky=W)
            Label(frame,text = '通信地址：上海市闵行区东川路800号上海交通大学',).grid(row=3,sticky=W)
            Label(frame,text = '邮箱：597279890@qq.com',).grid(row=4,sticky=W)
            Label(frame,text = '电话：15326283060',).grid(row=5,sticky=W)
    app=App(us)
    global r
    r=[1]
    def vv():
        if r[0]!=1:
            r[0]=1
            frame.destroy()
            app=App(us)
    def connact():
        if r[0]==1:
            fram.destroy()
            r[0]=2
            app=Cpp(us)
    menubar = Menu(us)
    menubar.add_command(label="版本信息", command=vv)
    menubar.add_command(label="联系我们", command=connact)
    us.config(menu=menubar)
    us.mainloop()
def helpa():
        helpa=Tk()
        helpa.title("使用说明")
        Label(helpa,text = '界面--',).grid(row=1,sticky=W)
        Label(helpa,text = '      本程序提供两种语言界面,并可在使用进行切换。').grid(row=2,sticky=W)
        Label(helpa,text = '             切换方法:帮助--→语言切换',).grid(row=3,sticky=W)
        Label(helpa,text = '文本键入--',).grid(row=4,sticky=W)
        Label(helpa,text = '      文本输入即可直接输入,亦可从文件导入(格式限定为txt格式)。',).grid(row=5,sticky=W)
        Label(helpa,text = '             导入放法:文件--→打开',).grid(row=6,sticky=W)
        Label(helpa,text = '信息处理--',).grid(row=7,sticky=W)
        Label(helpa,text = '      用户运行此程序可应用文章分词,单词分句和文章分句功能',).grid(row=8,sticky=W)
        Label(helpa,text = '             触发方式:点击相应按钮即可',).grid(row=9,sticky=W)
        Label(helpa,text = '结果获取--',).grid(row=10,sticky=W)
        Label(helpa,text = '      结果在全部完成是会自动显示在结果框中,用户可以选择导出。',).grid(row=11,sticky=W)
        Label(helpa,text = '             直接点击保存按钮 或 文件--→保存',).grid(row=12,sticky=W)
        Label(helpa,text = '调整--',).grid(row=13,sticky=W)
        Label(helpa,text = '      词典调整--',).grid(row=14,sticky=W)
        Label(helpa,text = '          用户根据自己需要添加和删除词典中的词以获取更准确的分词结果',).grid(row=15,sticky=W)
        Label(helpa,text = '                 例如:当"直男"一词出现在我们生活中,老式的字典并不能分出文章中的此词 ',).grid(row=16,sticky=W)
        Label(helpa,text = '                      用户可应用 调整--→词典调整 方式加入该词,这样该词将可以被分出').grid(row=17,sticky=W)
        Label(helpa,text = '      规则调整--',).grid(row=18,sticky=W)
        Label(helpa,text = '          用户根据自己需要添加和删除规则以获取更准确的分词结果,规则包括分隔符的移动,添加和删除。',).grid(row=19,sticky=W)
        Label(helpa,text = '                 例如:当"网球拍卖完了"一词被分为网球拍|卖完了,而实际意思为网球|排卖|完了 ').grid(row=20,sticky=W)
        Label(helpa,text = '                      用户可应用 调整--→规则调整 方式加入该词,这样该词将不会被分错').grid(row=21,sticky=W)
        Label(helpa,text = '                      例如： 球|拍卖 分割向右移 1 位 ').grid(row=22,sticky=W)
        helpa.minsize(580,510)
        helpa.maxsize(580,510)
        mainloop
def load():
    status.set("准备就绪")
    filename=askopenfilename(filetypes=[("文本文档",".txt"),("所有文件","*")],title="打开")
    x=open(filename,"r")
    a=x.read()
    entry.delete(1.0,END)
    result.delete(1.0,END)
    entry.insert(END,a)
def load2():
    status.set("Ready")
    filename=askopenfilename(filetypes=[("Text Files",".txt"),("All files","*")],title="Open")
    x=open(filename,"r")
    a=x.read()
    entry.delete(1.0,END)
    result.delete(1.0,END)
    entry.insert(END,a)
def save():
    filename=asksaveasfilename(title="Save",filetypes=[("文本文档",".txt")],defaultextension=".txt")
    x=open(filename,"w")
    x.write(result.get(1.0,END))
def save2():
    filename=asksaveasfilename(title="Save",filetypes=[("Text Files",".txt")],defaultextension=".txt")
    x=open(filename,"w")
    x.write(result.get(1.0,END))
single_name=input_dic("lexicon/single.txt")
double_name=input_dic("lexicon/double.txt")
dic=input_dic("lexicon/dict.txt")
blacklist=input_dic("lexicon/blacklist.txt")
whitelist=input_dic("lexicon/whitelist.txt")
def zhongwen():
    genben.destroy()
    zhong()
def zhong():
    root = Tk()
    root.title("史上最简洁有效分词工具")
    root.minsize(800,600)
    root.maxsize(800,600)
    def here():
        status.set("抱歉了")
        here=Tk()
        here.title("温馨提示")
        label=Label(here,text="亲,你可以通过调整字典与规则来\n增加分词准确度\n在菜单栏中调整选项中可以进行调整\n调整后重启程序即可\n感谢您的支持与改进\n谢谢")
        label.pack()
        mainloop()
    def clr():
        status.set("准备就绪")
        entry.delete(1.0,END)
    def clrb():
        status.set("准备就绪")
        result.delete(1.0,END)
    def fenju():
        result.delete(1.0,END)
        a=entry.get(1.0,END)
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
        result.insert(END,s)
    def rule1():
        def do1():
                global p
                p=1
        def do2():
                global p
                p=2
        def do3():
                global p
                p=3
        def do4():
                global p
                p=4
        def add_rule(a,dic):
                dic.append(a)
                dic.append("    return s")
                word="\n".join(dic)+"\n"
                lex=open("rule.py","w","utf-8")
                lex.write(word)
                lex.close()
                return dic
        def inputdic(a):
            dic=[]
            lex=open(a,"r","utf-8")
            for line in lex:
                if line[-1]=="\n":
                    dic.append(line[:-1])
                else:
                    dic.append(line)
            lex.close()
            return dic[:-1]
        def do():
            rule=inputdic("rule.py")
            if p==1:
                n=e3.get()
                add_rule(("    s=slide("+'"'+e1.get()+'"'+',"right",'+str(n)+',s)'),rule)
            if p==2:
                n=e4.get()
                add_rule(("    s=slide("+'"'+e1.get()+'"'+',"left",'+str(n)+',s)'),rule)
            if p==3:
                add_rule("    s=concat("+'"'+e1.get()+'"'+",s)",rule)
            if p==4:
                n=e5.get()
                add_rule("    s=divide("+'"'+e1.get()+'",'+n+',s)',rule)
            showinfo("温馨提示","该改动将在程序重新启动后生效")
            root3.destroy()
            status.set("准备就绪")
        global root3
        root3=Tk()
        root3.title("规则调整")
        root3.minsize(250,150)
        root3.maxsize(250,150)
        Label(root3,text="请复制到右侧").grid(row=0,sticky=W)
        e1=Entry(root3)
        e1.grid(row=0,column=1)
        e3=Entry(root3,width=2,)
        e3.grid(row=1,column=1,sticky=W)
        e4=Entry(root3,width=2,)
        e4.grid(row=2,column=1,sticky=W)
        e5=Entry(root3,width=2,)
        e5.grid(row=3,column=1,sticky=W)
        Radiobutton(root3,text = '分割向右移',value=1,command=do1).grid(row=1,sticky=W)
        Radiobutton(root3,text = '分割向左移',value=2,command=do2).grid(row=2,sticky=W)
        Radiobutton(root3,text = '分割符删除',value=3,command=do3).grid(row=4,sticky=W)
        Radiobutton(root3,text = '分割加于第',value=4,command=do4).grid(row=3,sticky=W)
        a=Button(root3,text="确定",command=do)
        b=Button(root3,text="取消",command=root3.destroy)
        a.place(x=170,y=50)
        b.place(x=170,y=90)
        c=Label(root3,text="位",)
        d=Label(root3,text="位",)
        c.place(x=105,y=25)
        d.place(x=105,y=50)
        e=Label(root3,text="个字后",)
        e.place(x=105,y=80)
        root3.mainloop()
    def dic1():
        global root2
        status.set("字典调整")
        root2=Tk()
        root2.minsize(250,120)
        root2.maxsize(250,120)
        label=Label(root2,text="请输要进行改动的词语",font="10")
        root2.title("词典调整")
        label.pack(pady=5)
        global a
        a=Text(root2,height=1,width=20,font="60")
        a.pack(pady=10)
        global ad
        ad=Button(root2,text="增加",command=add,font="20")
        ad.place(x=45,y=75,width=70)
        minus=Button(root2,text="移除",command=minu,font="20")
        minus.place(x=135,y=75,width=70)
        root2.mainloop()
    def add():
        c=a.get(1.0,END)[:-1]
        add_word(c,dic)
        root2.destroy()
        status.set("准备就绪")
    def minu():
        global dic
        d=a.get(1.0,END)[:-1]
        dic=delete_word(d,dic)
        root2.destroy()
        status.set("准备就绪")
        return dic
    def lau():
        root.destroy()
        english()

    class StatusBar(Frame):
        def __init__(self, master):
            Frame.__init__(self, master)
            self.label = Label(self,bd=1, relief=SUNKEN, anchor=W)
            self.label.pack(fill=X)
        def set(self, format, *args):
            self.label.config(text=format % args)
            self.label.update_idletasks()
        def clear(self):
            self.label.config(text="")
            self.label.update_idletasks()
    global status
    status = StatusBar(root)
    status.pack(side=BOTTOM, fill=X)
    status.set("准备就绪")
    menubar = Menu(root)
    file= Menu(menubar,tearoff=0)
    file.add_command(label="打开(O)...",command=load)
    file.add_command(label="保存(S)...", command=save)
    file.add_separator()
    file.add_command(label="退出(Q)", command=root.destroy)
    menubar.add_cascade(label="文件(F)", menu=file,)


    dictionary= Menu(menubar,tearoff=0)
    dictionary.add_command(label="修改字典",command=dic1)
    dictionary.add_command(label="修改规则", command=rule1)
    menubar.add_cascade(label="调整(R)", menu=dictionary)


    about=Menu(menubar,tearoff=0)
    about.add_command(label="使用手册",command=helpa)
    about.add_command(label="语言切换",command=lau)
    about.add_command(label="关于...",command=us)
    menubar.add_cascade(label="帮助(H)", menu=about)
    root.config(menu=menubar)

    shuru=Label(root,text="亲,请在下面的框框里输入想要操作的语料",bg="gray",width=40)
    shuru.pack()
    shuru.config(font='Helvetica -%d bold' %20)
    global entry
    entry=Text(root,height=15,width=100,)
    scrolla=Scrollbar(root,command=entry.yview,width=10)
    entry.configure(yscrollcommand=scrolla.set)
    entry.pack()
    scrolla.place_configure(x=760,y=30,height=200)
    class Cpp:
        def __init__(self, master):
            fram= Frame(master)
            fram.pack()
            self.fenci=Button(fram,text="分句",command=fenju)
            self.fenci.pack(side=LEFT,pady=10,padx=10,ipadx=10)
            self.fenci.config(font='Helvetica -%d bold' %16)
            self.fenju=Button(fram,text="单句分词",command=main)
            self.fenju.pack(side=LEFT,pady=10,padx=10,ipadx=10)
            self.fenju.config(font='Helvetica -%d bold' %16)
            self.fenju=Button(fram,text="全文分词",command=main2)
            self.fenju.pack(side=LEFT,pady=10,padx=10,ipadx=10)
            self.fenju.config(font='Helvetica -%d bold' %16)
            self.baocun=Button(fram,text="清除",command=clr)
            self.baocun.pack(side=LEFT,pady=10,padx=10,ipadx=10)
            self.baocun.config(font='Helvetica -%d bold' %16)
            self.tuichu=Button(fram,text="退出",command=root.destroy)
            self.tuichu.pack(side=RIGHT,pady=10,padx=10,ipadx=10)
            self.tuichu.config(font='Helvetica -%d bold' %16)
    app=Cpp(root)
    class Dpp:
        def __init__(self, master):
            frame= Frame(master)
            frame.pack()
            shuchu=Label(root,text="亲,请看看下面这个框框里是不是预期的结果",bg="gray",width=40)
            shuchu.pack()
            shuchu.config(font='Helvetica -%d bold' %20)
            global result
            result=Text(root,height=15,width=100, name="shuchu")
            scroll=Scrollbar(root,command=result.yview,width=10)
            result.configure(yscrollcommand=scroll.set)
            result.pack()
            scroll.place_configure(x=760,y=312,height=200)
    app=Dpp(root)
    def again():
        if messagebox.askyesno("史上最简洁有效分词工具","是否想要再来一次")==True:
            clr()
            clrb()
        else:
            if messagebox.askyesno("史上最简洁有效分词工具","您确定要退出?",icon=WARNING)==True:
                root.destroy()
            else:
                clr()
                clrb()
    class Epp:
        def __init__(self, master):
            global frame
            frame = Frame(master)
            frame.pack()
            self.good=Button(frame,text="简直就是太完美了",command=again)
            self.good.pack(side=LEFT,pady=10)
            self.bad=Button(frame,text="差一点就太完美了",command=here)
            self.bad.pack(side=LEFT,pady=10)
            self.baocun=Button(frame,text="清除",command=clrb)
            self.baocun.pack(side=LEFT,padx=10)
            self.qingchu=Button(frame,text="保存",command=save)
            self.qingchu.pack(side=RIGHT)
    app=Epp(root)
    mainloop()
#-----------------------------------------------------------------------------------------------------------------------------------------------------
def eng():
    genben.destroy()
    english()
def english():
    root = Tk()
    root.title("A really powerful tool")
    root.minsize(800,600)
    root.maxsize(800,600)
    def here():
        here=Tk()
        here.title("Tips")
        label=Label(here,text="You can get a better result\nif you do some change on dictionary and rule\nwhich can be operated in rectify.\nThank you for using!!!")
        label.pack()
        status.set("Sorry")
        mainloop()
    def clr():
        status.set("Ready")
        entry.delete(1.0,END)
    def clrb():
        status.set("Ready")
        result.delete(1.0,END)
    def fenju():
        result.delete(1.0,END)
        a=entry.get(1.0,END)
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
        result.insert(END,s)
    def rule2():
        def do1():
                global p
                p=1
        def do2():
                global p
                p=2
        def do3():
                global p
                p=3
        def do4():
                global p
                p=4
        def add_rule(a,dic):
                dic.append(a)
                dic.append("    return s")
                word="\n".join(dic)+"\n"
                lex=open("rule.py","w","utf-8")
                lex.write(word)
                lex.close()
                return dic
        def inputdic(a):
            dic=[]
            lex=open(a,"r","utf-8")
            for line in lex:
                if line[-1]=="\n":
                    dic.append(line[:-1])
                else:
                    dic.append(line)
            lex.close()
            return dic[:-1]
        def do():
            rule=inputdic("rule.py")
            if p==1:
                n=e3.get()
                add_rule(("    s=slide("+'"'+e1.get()+'"'+',"right",'+str(n)+',s)'),rule)
            if p==2:
                n=e4.get()
                add_rule(("    s=slide("+'"'+e1.get()+'"'+',"left",'+str(n)+',s)'),rule)
            if p==3:
                add_rule("    s=concat("+'"'+e1.get()+'"'+",s)",rule)
            if p==4:
                n=e5.get()
                add_rule("    s=divide("+'"'+e1.get()+'",'+n+',s)',rule)
            showinfo("Info","The change will be applied when the program is restarted.")
            root3.destroy()
            status.set("Ready")
        global root3
        root3=Tk()
        root3.title("Rules")
        root3.minsize(250,150)
        root3.maxsize(250,150)
        Label(root3,text="Please copy to the right").grid(row=0,sticky=W)
        e1=Entry(root3)
        e1.grid(row=0,column=1)
        e3=Entry(root3,width=2,)
        e3.grid(row=1,column=1,sticky=W)
        e4=Entry(root3,width=2,)
        e4.grid(row=2,column=1,sticky=W)
        e5=Entry(root3,width=2,)
        e5.grid(row=3,column=1,sticky=W)
        Radiobutton(root3,text = 'move right position',value=1,command=do1).grid(row=1,sticky=W)
        Radiobutton(root3,text = 'move left position',value=2,command=do2).grid(row=2,sticky=W)
        Radiobutton(root3,text = 'delete segement',value=3,command=do3).grid(row=4,sticky=W)
        Radiobutton(root3,text = 'add segement on',value=4,command=do4).grid(row=3,sticky=W)
        a=Button(root3,text="OK",command=do)
        b=Button(root3,text="Cancel",command=root3.destroy)
        a.place(x=190,y=50)
        b.place(x=180,y=90)
        root3.mainloop()
    def dic1():
        global root2
        status.set("Dictionary ...")
        root2=Tk()
        root2.minsize(300,120)
        root2.maxsize(300,120)
        label=Label(root2,text="please input the word you want to operate",)
        root2.title("Dictionary")
        label.pack(pady=5)
        global a
        a=Text(root2,height=1,width=30,font="60")
        a.pack(pady=10)
        global ad
        ad=Button(root2,text="Add",command=add,font="20")
        ad.place(x=55,y=75,width=70)
        minus=Button(root2,text="Delete",command=minu,font="20")
        minus.place(x=155,y=75,width=70)
        root2.mainloop()
    def add():
        c=a.get(1.0,END)[:-1]
        add_word(c,dic)
        root2.destroy()
        status.set("Ready")
    def minu():
        d=a.get(1.0,END)[:-1]
        delete_word(d,dic)
        root2.destroy()
        status.set("Ready")
    def lau():
        root.destroy()
        zhong()
    class StatusBar(Frame):
        def __init__(self, master):
            Frame.__init__(self, master)
            self.label = Label(self,bd=1, relief=SUNKEN, anchor=W)
            self.label.pack(fill=X)
        def set(self, format, *args):
            self.label.config(text=format % args)
            self.label.update_idletasks()
        def clear(self):
            self.label.config(text="")
            self.label.update_idletasks()
    global status
    status = StatusBar(root)
    status.pack(side=BOTTOM, fill=X)
    status.set("Ready")
    menubar = Menu(root)
    file= Menu(menubar,tearoff=0)
    file.add_command(label="Open...",command=load2)
    file.add_command(label="Save...", command=save2)
    file.add_separator()
    file.add_command(label="Quit", command=root.destroy)
    menubar.add_cascade(label="File", menu=file,)

    dictionary= Menu(menubar,tearoff=0)
    dictionary.add_command(label="dictionary",command=dic1)
    dictionary.add_command(label="rule", command=rule2)
    menubar.add_cascade(label="Rectify", menu=dictionary)

    about=Menu(menubar,tearoff=0)
    about.add_command(label="User instruction",command=helpa)
    about.add_command(label="Change language",command=lau)
    about.add_command(label="About us...",command=us)
    menubar.add_cascade(label="Help", menu=about)
    root.config(menu=menubar)

    shuru=Label(root,text="Dear, Please entry words here",bg="gray",width=40)
    shuru.pack()
    shuru.config(font='Helvetica -%d bold' %20)
    global entry
    entry=Text(root,height=15,width=100,)
    scrolla=Scrollbar(root,command=entry.yview,width=10)
    entry.configure(yscrollcommand=scrolla.set)
    entry.pack()
    scrolla.place_configure(x=760,y=30,height=200)
    class Cpp:
        def __init__(self, master):
            fram= Frame(master)
            fram.pack()
            self.fenci=Button(fram,text="cut sentences",command=fenju)
            self.fenci.pack(side=LEFT,pady=10,padx=10,ipadx=10)
            self.fenci.config(font='Helvetica -%d bold' %16)
            self.fenju=Button(fram,text="operate a sentence",command=main3)
            self.fenju.pack(side=LEFT,pady=10,padx=10,ipadx=10)
            self.fenju.config(font='Helvetica -%d bold' %16)
            self.fenju=Button(fram,text="operate all",command=main4)
            self.fenju.pack(side=LEFT,pady=10,padx=10,ipadx=10)
            self.fenju.config(font='Helvetica -%d bold' %16)
            self.baocun=Button(fram,text="Clear",command=clr)
            self.baocun.pack(side=LEFT,pady=10,padx=10,ipadx=10)
            self.baocun.config(font='Helvetica -%d bold' %16)
            self.tuichu=Button(fram,text="Quit",command=root.destroy)
            self.tuichu.pack(side=RIGHT,pady=10,padx=10,ipadx=10)
            self.tuichu.config(font='Helvetica -%d bold' %16)
    app=Cpp(root)
    class Dpp:
        def __init__(self, master):
            frame= Frame(master)
            frame.pack()
            shuchu=Label(root,text="Dear, Please check if follows are RIGHT",bg="gray",width=40)
            shuchu.pack()
            shuchu.config(font='Helvetica -%d bold' %20)
            global result
            result=Text(root,height=15,width=100, name="shuchu")
            scroll=Scrollbar(root,command=result.yview,width=10)
            result.configure(yscrollcommand=scroll.set)
            result.pack()
            scroll.place_configure(x=760,y=312,height=200)
    app=Dpp(root)
    def again():
        if messagebox.askyesno("A powerful tool","Try Again?")==True:
            clr()
            clrb()
        else:
            if messagebox.askyesno("A powerful tool","are you sure to quit?",icon=WARNING)==True:
                root.destroy()
            else:
                clr()
                clrb()
    class Epp:
        def __init__(self, master):
            frame = Frame(master)
            frame.pack()
            self.good=Button(frame,text="Perfect",command=again)
            self.good.pack(side=LEFT,pady=10)
            self.bad=Button(frame,text="Good",command=here)
            self.bad.pack(side=LEFT,pady=10)
            self.baocun=Button(frame,text="Clear",command=clrb)
            self.baocun.pack(side=LEFT,padx=10)
            self.qingchu=Button(frame,text="Save",command=save2)
            self.qingchu.pack(side=RIGHT)
    app=Epp(root)
    mainloop()
genben = Tk()
genben.title("语言选择")
genben.minsize(250,120)
genben.maxsize(250,120)
label=Label(genben,text="请选择界面语言\n(Choose language)",)
label.config(font='Helvetica -%d bold' %16)
label.place(x=50,y=20)
ad=Button(genben,text="简体中文",command=zhongwen,font="30")
ad.config(font='黑体' )
ad.place(x=45,y=75,width=70)
minus=Button(genben,text="English",command=eng,font="20")
minus.place(x=135,y=75,width=70)
genben.mainloop()