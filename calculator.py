# -*- coding = 'utf-8 -*-

import argparse
import random
import operator
import re
from fractions import Fraction

def symlist():#获取符号列表
    slist=[]
    syb=0
    i=random.randint(1, 3)
    for x in range(i):
        sy=random.choice(['+','-','×','÷'])
        if sy=='+'or sy=='-':
            syb +=10**(i-x-1)
        else :
            syb += 2 * (10 ** (i - x - 1))
        slist.append(sy)
    return symbol,i,syb

def numlist(i,r):#获取数值列表
    nlist=[]
    n=1
    m=0
    if r < 10:
        n = int(10 / r)
    if n==1:
        while m <= i:
            nlist.append(Fraction(random.randint(1, r), random.randint(1, r)))
            m+=1
    else:
        while m <= i:
            nu = Fraction(random.randint(1, r * n), random.randint(1, r * n))
            if nu<=r:
                nlist.append(nu)
                m += 1
    return nlist

def calculate(a,b,s):#计算
    ans=0
    if s=='+':
        ans=a+b
    elif s=='-':
        a,b=max(a,b),min(a,b)
        ans=a-b
    elif s=='×':
        ans=a*b
    else:ans=a/b
    return ans

def cf(fraction):#真分数的表达
    if fraction.numerator%fraction.denominator==0:
        return '%d'%(fraction.numerator/fraction.denominator)
    elif fraction.numerator>fraction.denominator:
        a=int(fraction.numerator/fraction.denominator)
        b, c = fraction.numerator - a * fraction.denominator, fraction.denominator
        return '%d%s%d%s%d' % (a,'’',b,'/',c)
    else:
        b, c = fraction.numerator, fraction.denominator
        return '%d%s%d' % (b,'/',c)
    
def rcf(fra):#真分数转化为分数
    line = re.sub(r'[\’\/]', ' ', fra)
    wo = line.split(' ')  # 空格分割单词
    wo = [int(x) for x in wo]
    i=len(wo)
    if i==1:
        return wo[0]
    elif i==2:
        return Fraction(wo[0], wo[1])
    else:return Fraction(wo[0]*wo[2]+wo[1], wo[2])





    
    




def main():
    parser = argparse.ArgumentParser(description="this is auto calculator")
    parser.add_argument('-n',help='控制生成题目的个数'type=int)
    parser.add_argument('-r',help='控制题目中数值（自然数、真分数和真分数分母）的范围'type=int)
    parser.add_argument('-e',help='题目文件目录')
    parser.add_argument('-a',help='答案文件目录')
    args = parser.parse_args()
    
if __name__ == '__main__':
    main()
    
