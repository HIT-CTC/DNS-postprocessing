#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 22:29:42 2021

@author: yh
"""

import h5py
import numpy as np
from pathlib import Path
import argparse as ap

class readHDF(object):
    def __init__(self, filename, path):
        self.path = Path(path)
        self.filename = self.path/filename
        
    def readInfo(self, var):
        f = h5py.File(self.filename, 'r')
        for svar in var:
            print('Variables name is {}'.format(svar))
            print('Type is', f[svar].dtype)
            if f[svar].shape != (1, ):
                print('The shape of the variables is ', f[svar].shape)
            else:
                print('The number of the variable is', f[svar][0])
            print('----------------------------')

        
#HDF5的读取：
# f = h5py.File('avg_recy.h5','r')   #打开h5文件
# 可以查看特定的变量
# varName = input('please input varName:')
# if(f.get(varName) is None):
#     print('There is no ' + varName)
# else:
#     print(type(f[varName]))
#     print(len(f[varName]))
#     print(f[varName].shape)
# 可以查看所有的变量
#for key in f.keys():
#     print(f[key].name)
#     print(f[key].shape)
if __name__ == '__main__':
    parser = ap.ArgumentParser(prog='HDFView', description='Generate a xdmf file to view HDF file.')
    parser.add_argument(
                        '-p', '--path',                # Option Name
                        required='False',               # Requirement
                        help='Type the Path',          # Help log
                        metavar='Path',                # [-p path]
                        default='.'
                        )
    parser.add_argument(
                        '-f', '--filename',            # Option Name
                        required='True',               # Requirement
                        help='Type the Filename(must)',# Help log
                        metavar='Filename'             # [-f filename]
                        )
    parser.add_argument(
                        '-v', '--variables',
                        action='extend',               # Action of option
                        nargs='+',                     # N args
                        help='Type the Variables(must)',
                        metavar='Variables'
                        )
    args = parser.parse_args()
    a = readHDF(args.filename, args.path).readInfo(args.variables)

