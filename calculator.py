# -*- coding = 'utf-8 -*-

import argparse
import random
import operator
import re
import time
from fractions import Fraction

j=0
k=0

start =time.clock()

def numlist(i,r):#获取数值列表
    nlist=[]#数值列表
    for m in range(i+1):#根据i的值遍历输出数值列表
        nlist.append(Fraction(random.randint(1, r), random.randint(1, r)))
    return nlist

def symlist():#获取符号列表
    slist=[]#符号列表
    hsb=0#判断怎么加括号
    l=0#判断是否是减数运算
    i=random.randint(1, 3)#随机获取符号数目
    for x in range(i):
        sy=random.choice(['+','-','×','÷'])
        if sy=='+'or sy=='-':
            hsb +=10**(i-x-1)
        else :
            hsb += 2 * (10 ** (i - x - 1))
        slist.append(sy)
        if sy=='-':
            l=1
    return slist,hsb,i,l



def f(f):#分数的表达
    a=f.numerator
    b=f.denominator
    if a%b==0:#为整数
        return '%d'%(a/b)
    elif a<b:#为真分数
        return '%d%s%d' % (a,'/',b)
    else:#为带分数
        c=int(a/b)
        a = a - c * b
        return '%d%s%d%s%d' % (c,'’',a,'/',b)

    
def rf(f):#分数转化为整数、真分数和假分数
    line = re.sub(r'[\’\/]', ' ', f)
    line1 = line.split(' ')  # 空格分割单词
    line1 = [int(x) for x in line1]
    i=len(line1)
    if i==1:#为整数
        return line1[0]
    elif i==2:#为真分数
        return Fraction(line1[0], line1[1])
    else:#为假分数
        return Fraction(line1[0]*line1[2]+line1[1], line1[2])
    
def calculate(a,b,s):#计算单元，a，b是数，c是符号
    ans=0
    if s=='+':#加法运算
        ans=a+b
    elif s=='-':#减法运算
        a,b=max(a,b),min(a,b)#防止结果为负数
        ans=a-b
    elif s=='×':#乘法运算
        ans=a*b
    else:ans=a/b#除法运算
    return ans

def writeF(slist,num,hsb):#生成算术表达式
    global j,k
    s=''
    if hsb>100:
        if j==1 and k==0:
            s = '%s %s (%s %s %s) %s %s = ' % (f(num[0]), slist[0],
            f(num[1]),slist[1], f(num[2]), slist[2], f(num[3]))
        elif j==1 and k==1:
            s = '%s %s (%s %s (%s %s %s)) = ' % (f(num[0]), slist[0],
            f(num[1]),slist[1], f(num[2]), slist[2], f(num[3]))
        elif j==0 and k==1:
            s = '%s %s (%s %s %s %s %s) = ' % (f(num[0]), slist[0],
            f(num[1]),slist[1], f(num[2]), slist[2], f(num[3]))
        if hsb == 112 or hsb ==212:          
            s = '(%s %s %s %s %s) %s %s = ' % (f(num[0]), slist[0],
            f(num[1]),slist[1], f(num[2]), slist[2], f(num[3]))
        elif hsb == 121 or hsb ==122:
            s = '(%s %s %s) %s %s %s %s = ' % (f(num[0]), slist[0],
            f(num[1]),slist[1], f(num[2]), slist[2], f(num[3]))
        else:
            s = '%s %s %s %s %s %s %s = ' % (f(num[0]), slist[0],
            f(num[1]),slist[1], f(num[2]), slist[2], f(num[3]))
    elif hsb>10:
        if j==1 :
            s = '%s %s (%s %s %s) = ' % (f(num[0]), slist[0],
            f(num[1]), slist[1], f(num[2]))
        if hsb == 12:
            s = '(%s %s %s)%s %s = ' % (f(num[0]), slist[0],
            f(num[1]), slist[1], f(num[2]))
        else:
            s = '%s %s %s %s %s = ' % (f(num[0]), slist[0],
            f(num[1]), slist[1], f(num[2]))
    else :
        s ='%s %s %s = ' % (f(num[0]),slist[0],f(num[1]))
    return s

def getF(n,r):#生成题目和答案列表
    E,A,E1,E2=[],[],[],[]
    global j,k
    x=1
    while x<n+1:
        slist,hsb,i,l=symlist()
        num=numlist(i,r)
        num1=num
        legal = True
        if l==1:            
            if  num[0]<num[1]:
                num1[0],num1[1]=num[1],num[0]
            if i>=2 and calculate(num[0],num[1],slist[0])<num[2]:
                num1[0],num1[1],num1[2]=num[2],num[0],num[1]
                j=1
            if i>=3 and calculate(calculate(num[0],num[1],slist[0]),num[2],slist[1])<num[3]:
                num1[0],num1[1],num1[2],num1[3]=num[3],num[0],num[1],num[2]
                k=1        
        ans=num1[0]
        for y in range(i):
            cal=calculate(ans,num[y+1],slist[y])
            if cal>=0:#判断算式是否合法
                ans=cal
            else:
                legal=False
                break
        if legal:#判断是否重复题目
            try:
                num=A.index(ans)#第一个重复答案的索引
                if operator.eq(E1[num],slist) and operator.eq(E2[num],num):
                    pass
            except ValueError as e:#可以写入
                A.append(ans)
                E1.append(slist)
                E2.append(num1)
                E.append('%d. %s'%(x,writeF(slist,num1,hsb)))
                x+=1
        else:pass
    return E,A

def save(fname, data):#fname为写入文件的路径，data为要写入的数据列表.
    file = open(fname,'a')
    file.seek(0)
    file.truncate() 
    for i in range(len(data)):
        s = str(data[i]).replace('[','').replace(']','')
        s = s.replace("'",'').replace(',','') +'\n'
        file.write(s)
                  
    file.close()
    print('%s文件保存成功'%fname)







def main():
    parser = argparse.ArgumentParser(description="this is auto calculator")
    parser.add_argument('-n',help='控制生成题目的个数',type=int)
    parser.add_argument('-r',help='控制题目中数值（自然数、真分数和真分数分母）的范围',type=int)
    args = parser.parse_args()
    if args.n:
        n=args.n
        print('n值为%d'%n)
    if args.r:
        r=args.r
        print('r值为%d'%r)
        E, A=getF(n,r)
        for x in range(n):
            A[x]='%d. %s'%(x+1,f(A[x]))
        save('Exercises.txt',E)
        save('Answers.txt',A)

    end = time.clock()
    print('Running time: %s '%(end-start))

    
if __name__ == '__main__':
    main()
    
