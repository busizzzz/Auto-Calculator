# -*- coding = 'utf-8 -*-

import argparse
import random
import operator
import re
from fractions import Fraction

def numlist():
    




def main():
    parser = argparse.ArgumentParser(description="this is auto calculator")
    parser.add_argument('-n',help='控制生成题目的个数'type=int)
    parser.add_argument('-r',help='控制题目中数值（自然数、真分数和真分数分母）的范围'type=int)
    parser.add_argument('-e',help='题目文件目录')
    parser.add_argument('-a',help='答案文件目录')
    args = parser.parse_args()
    
if __name__ == '__main__':
    main()
    
