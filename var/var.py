#!/home/yh/anaconda3/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 22:29:42 2021

@author: yh
"""

import h5py
import numpy as np
#HDF5的读取：
f = h5py.File('avg_recy.h5','r')   #打开h5文件
# 可以查看特定的变量
varName = input('please input varName:')
if(f.get(varName) is None):
    print('There is no ' + varName)
else:
    print(type(f[varName]))
    print(len(f[varName]))
    print(f[varName].shape)
# 可以查看所有的变量
#for key in f.keys():
#     print(f[key].name)
#     print(f[key].shape)