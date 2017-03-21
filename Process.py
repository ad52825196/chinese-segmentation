a=open("lexicon/dict.txt","r")
b=open("dict.txt","w")
c=[]
for i in a:
    if i not in c:
        c.append(i)
c.sort()
c.sort(key=lambda x:len(x))
for i in c:
    b.write(i)
a.close()
b.close()