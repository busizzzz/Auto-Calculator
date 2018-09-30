# -*- coding = 'utf-8 -*-

import argparse
import random
import operator
import re
import time
from fractions import Fraction

start =time.clock()

def numlist(i,r):#获取数值列表
    nlist=[]#数值列表
    m=0
    while m <= i:
        nlist.append(Fraction(random.randint(1, r), random.randint(1, r)))
        m+=1
    return nlist

def symlist():#获取符号列表
    slist=[]#符号列表
    syb=0#判断加减或是乘除的变量
    i=random.randint(1, 3)#符号数
    for x in range(i):
        sy=random.choice(['+','-','×','÷'])
        if sy=='+'or sy=='-':
            syb +=10**(i-x-1)
        else :
            syb += 2 * (10 ** (i - x - 1))
        slist.append(sy)
    return slist,i,syb



def f(fraction):#真分数的表达
    if fraction.numerator%fraction.denominator==0:
        return '%d'%(fraction.numerator/fraction.denominator)
    elif fraction.numerator>fraction.denominator:
        a=int(fraction.numerator/fraction.denominator)
        b, c = fraction.numerator - a * fraction.denominator, fraction.denominator
        return '%d%s%d%s%d' % (a,'’',b,'/',c)
    else:
        b, c = fraction.numerator, fraction.denominator
        return '%d%s%d' % (b,'/',c)
    
def rf(f):#假分数转化为分数
    line = re.sub(r'[\’\/]', ' ', f)
    wo = line.split(' ')  # 空格分割单词
    wo = [int(x) for x in wo]
    i=len(wo)
    if i==1:
        return wo[0]
    elif i==2:
        return Fraction(wo[0], wo[1])
    else:return Fraction(wo[0]*wo[2]+wo[1], wo[2])
    
def calculate(a,b,s):#计算单元，a，b是数，c是符号
    ans=0
    if s=='+':
        ans=a+b
    elif s=='-':
        a,b=max(a,b),min(a,b)#防止结果为负数
        ans=a-b
    elif s=='×':
        ans=a*b
    else:ans=a/b
    return ans

def writeFormula(slist,numerical,syb):#算术表达式
    s=''
    if syb>100:
        if syb == 112 or syb ==212:
            s = '(%s %s %s %s %s) %s %s = ' % (f(numerical[0]), slist[0],
            f(numerical[1]),slist[1], f(numerical[2]), slist[2], f(numerical[3]))
        elif syb == 121 or syb ==122:
            s = '(%s %s %s) %s %s %s %s = ' % (f(numerical[0]), slist[0],
            f(numerical[1]),slist[1], f(numerical[2]), slist[2], f(numerical[3]))
        else:
            s = '%s %s %s %s %s %s %s = ' % (f(numerical[0]), slist[0],
            f(numerical[1]),slist[1], f(numerical[2]), slist[2], f(numerical[3]))
    elif syb>10:
        if syb == 12:
            s = '(%s %s %s)%s %s = ' % (f(numerical[0]), slist[0],
            f(numerical[1]), slist[1], f(numerical[2]))
        else:
            s = '%s %s %s %s %s = ' % (f(numerical[0]), slist[0],
            f(numerical[1]), slist[1], f(numerical[2]))
    else :
        s ='%s %s %s = ' % (f(numerical[0]),slist[0],f(numerical[1]))
    return s

def getFormula(n,r):#生成题目和答案列表
    Exercises,Answers,Exercises1,Exercises2=[],[],[],[]
    x=1
    while x<n+1:
        slist,i,syb=symlist()
        num=numlist(i,r)
        ans = num[0]
        legal = True
        for y in range(i):
            cal=calculate(ans,num[y+1],slist[y])
            if cal>=0:#判断算式是否合法
                ans=cal
            else:
                legal=False
                break
        if legal:#判断是否重复题目
            try:
                num=Answers.index(ans)#第一个重复答案的索引
                if operator.eq(Exercises1[num],slist) and operator.eq(Exercises2[num],num):
                    pass
            except ValueError as e:#可以写入
                Answers.append(ans)
                Exercises1.append(slist)
                Exercises2.append(num)
                Exercises.append('%d. %s'%(x,writeFormula(slist,num,syb)))
                x+=1
        else:pass
    return Exercises,Answers

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

def answers_read(fname):
    file = open(fname)
    read = file.readlines()
    ans=[]
    for line in read:
        line = re.sub(r'\n', ' ', line)
        ans.append(line.split(' ')[1])#字符串
    return ans

def exercises_read(fname):
    file = open(fname)
    read = file.readlines()
    ans2= []
    for line in read:
        line = re.sub(r'[\.\(\)\=\s]+', ' ', line)
        line = line.strip()  # 除去左右的空格
        wo = line.split( )  # 空格分割单词
        del wo[0]
        sy,nu=[],[]
        for x in range(len(wo)):
            if x%2:
                sy.append(wo[x])
            else:nu.append(rf(wo[x]))
        ans = nu[0]
        for y in range(len(sy)):
            ans = calculate(ans, nu[y + 1], sy[y])
        ans2.append(ans)
    return ans2

def checkAnswer(a,e,ra,re):
    correct,wrong=[],[]
    for x in range(len(ra)):
        if operator.eq(ra[x],f(re[x])):
            correct.append(x+1)
        else:wrong.append(x+1)

    file = open('Grade.txt', 'a')
    file.seek(0)
    file.truncate()  # 清空文件
    x1='Correct:%d%s\n'%(len(correct),correct)
    x2='Wrong:%d%s'%(len(wrong),wrong)
    file.write(x1)
    file.write(x2)
    file.close()
    print('比对成功，对比结果存入Grade.txt')



def main():
    parser = argparse.ArgumentParser(description="this is auto calculator")
    parser.add_argument('-n',help='控制生成题目的个数',type=int)
    parser.add_argument('-r',help='控制题目中数值（自然数、真分数和真分数分母）的范围',type=int)
    parser.add_argument('-e',help='题目文件目录')
    parser.add_argument('-a',help='答案文件目录')
    args = parser.parse_args()
    if args.n:
        n=args.n
    if args.r:
        r=args.r
        Exercises, Answers=getFormula(n,r)
        for x in range(n):
            Answers[x]='%d. %s'%(x+1,f(Answers[x]))
        print('n,r两个参数的值为%d,%d:'%(n,r))
        save('Exercises.txt',Exercises)
        save('Answers.txt',Answers)
    if args.e and args.a:#'Answers.txt','Exercises.txt'
        Answers1=args.a
        Exercises1=args.e
        checkAnswer(Answers1,Exercises1,answers_read(Answers1), exercises_read(Exercises1))
    end = time.clock()
    print('Running time: %s '%(end-start))

    
if __name__ == '__main__':
    main()
    
