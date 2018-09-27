# -*- coding = 'utf-8 -*-

import argparse

def main():
    parser = argparse.ArgumentParser(description="this is auto calculator")
    parser.add_argument('-n',dest='n_arg',type=int)
    parser.add_argument('-r',dest='r_arg',required = True,type=int)
    parser.add_argument('-e',dest='e_arg')
    parser.add_argument('-a',dest='a_arg')
    args = parser.parse_args()
    
