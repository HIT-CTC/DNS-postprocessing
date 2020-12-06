#!/usr/bin/python

import h5py
import numpy as np
import re
from pathlib import Path
from prof import avg, div

#----------------------------------------#
#---------- Get Var Dictionary ----------#
#----------------------------------------#
def varDict(fn):
    vardict = {}
    with h5py.File(fn, 'r') as f:
        varlist = f.keys()
        for var in varlist:
            if var[0] in ['u', 'v', 'w', 'p']:
                vardict[var] = False
    return vardict

def confDict(varlist, vardict):
    for var in varlist:
        if var in vardict.keys():
            vardict[var] = True
    return vardict
    
def readHDF(fn, var):
    with h5py.File(fn, 'r') as f:
        sh_in = f[var].shape
        dims = len(sh_in)
        if dims == 1:
            if sh_in[0] == 1:
                var_out = f[var][0]
            else:
                var_out = f[var][:]
        elif dims == 2:
            var_out = f[var][:,:]
        elif dims == 3:
            var_out = f[var][:,:,:]
        f.close()
    return var_out
        
def norAll(var):
    return avg.avg2d(avg.avg3d(var, 3), 2)
    
#----------------------------------------#
#------------ Postprocessing ------------#
#----------------------------------------#
class outputData(object):
    def __init__(self, path, fn, varlist, flag_nor=True):
        self.path     = Path(path).expanduser().resolve()
        self.fn       = self.path/fn
        self.varlist  = varlist
        self.var_dict = varDict(self.fn)
        self.var_dict = confDict(self.varlist, self.var_dict)
        #---- Get Basic Information From File ----#
        self.zc   = readHDF(self.fn, 'zc'  )
        self.nu   = readHDF(self.fn, 'nu'  )
        self.tau  = readHDF(self.fn, 'tau' )
        self.utau = readHDF(self.fn, 'utau')
        self.zplus= self.zc*self.utau/self.nu
        for var, var_flag in self.var_dict.items():
            if var_flag:
                if flag_nor:
                    nor = 1
                    for str in var:
                        if str in ['u', 'v', 'w']:
                            nor *= 1/self.utau
                        elif str in ['p']:
                            nor *= 1/self.tau
                        elif str in ['x', 'y', 'z']:
                            nor *= self.nu/self.utau
                    setattr(self, var, norAll(readHDF(self.fn, var))*nor)
        
    def outputData(self, outputname):
        i = 0
        varlist = []
        for var_str, var_flag in self.var_dict.items():
            if var_flag:
                varlist.append(var_str)
        varlist.insert(0, 'zplus')
        varlist.insert(0, 'zc')
        filename  = '{}.dat'.format(outputname)
        filename = self.path/filename
        head_str1 = ''
        head_str2 = ''
        for var_str in varlist:
            i += 1
            head_str1 += '{:^14s}'.format('C'+str(i))
            head_str2 += '{:^14s}'.format(var_str)
        title_head = '{:40s}'.format('Statistics of Retau={} Rem={}'.format(self.utau/self.nu, 1/self.nu))+'\n'
        head_str1 += '\n'
        head_str2 += '\n'
        spl_head = 80*'-'+'\n'
        # Write text in file
        outfile = open(filename, 'w')
        outfile.write(title_head+head_str1+head_str2+spl_head*2)
        for i in range(len(self.zc)):
            for var_str in varlist:
                var = getattr(self, var_str)[i]
                if var_str in ['rethe', 'redel', 'rex', 'retau', 'redeldi', 'redelen']:
                    outfile.write('{:14.2e}'.format(var))
                elif var_str in ['zc', 'zplus']:
                    outfile.write('{:14.6f}'.format(var))
                else:
                    outfile.write('{:14.6e}'.format(var))
            outfile.write('\n')
        print('File generated complete')
        outfile.close()


if __name__ == '__main__':
    path = '/home/xlc/DATA/it_Data'
    fn = 'avg_recy.h5'
    varlist = ['u','v','w']
    a = outputData(path,fn,varlist).outputData('doubt_vec')
