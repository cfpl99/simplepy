#生成任意个数、任意位数且互不重复的随机数：
import random
n1=int(input('随机数个数='))
n2=int(input('随机数长度='))
l=[]
s='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'#这里可以加入你想要的字符
while True:
    name=''
    for _ in range(n2):
        i=random.choice(s)
        name=name+i
    if name not in l:
        l.append(name)
        if len(l)==n1:
            for j in l:
                print(j)
            break
