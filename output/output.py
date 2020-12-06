#!/usr/bin/python

import h5py
import numpy as np
import re
import argparse as ap
import sys
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
    
def readHDF(fn, var, blockz=None, blocky=None, blockx=None):
    with h5py.File(fn, 'r') as f:
        sh_in = f[var].shape
        dims = len(sh_in)
        if dims == 1:
            if blockz == None:
                blockz=[0, 1, sh_in[0], 1]
            if sh_in[0] == 1:
                var_out = f[var][0]
            else:
                var_out = f[var][h5py.MultiBlockSlice(blockz[0], blockz[1], blockz[2], blockz[3])][:]
        elif dims == 2:
            if blockz == None:
                blockz=[0, 1, sh_in[0], 1]
            if blocky == None:
                blocky=[0, 1, sh_in[1], 1]
            var_out = f[var][h5py.MultiBlockSlice(blockz[0], blockz[1], blockz[2], blockz[3]),
                             h5py.MultiBlockSlice(blocky[0], blocky[1], blocky[2], blocky[3])][:,:]
        elif dims == 3:
            if blockz == None:
                blockz=[0, 1, sh_in[0], 1]
            if blocky == None:
                blocky=[0, 1, sh_in[1], 1]
            if blockx == None:
                blockx=[0, 1, sh_in[2], 1]
            var_out = f[var][h5py.MultiBlockSlice(blockz[0], blockz[1], blockz[2], blockz[3]),
                             h5py.MultiBlockSlice(blocky[0], blocky[1], blocky[2], blocky[3]),
                             h5py.MultiBlockSlice(blockx[0], blockx[1], blockx[2], blockx[3])][:,:,:]
        f.close()
    return var_out
        
def norAll(var):
    return avg.avg2d(avg.avg3d(var, 3), 2)
    
def check(fn):
    print(h5py.File(fn, 'r').keys())
    
#----------------------------------------#
#------------ Postprocessing ------------#
#----------------------------------------#
class outputData(object):
    def __init__(self, path, fn, varlist, flag_nor=True, blockz=None, blocky=None, blockx=None):
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
                    setattr(self, var, norAll(readHDF(self.fn, var, blockz, blocky, blockx))*nor)
        
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
    parser = ap.ArgumentParser(prog='Output', description='Output data in a text file')
    parser.add_argument(
                        '-p', '--path',                # Option Name
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
                        '-o', '--output',              # Option Name
                        required='True',               # Requirement
                        help='Type the output(must)'  ,# Help log
                        metavar='Filename'             # [-f filename]
                        )
    parser.add_argument(
                        '-v', '--variables',
                        action='extend',               # Action of option
                        nargs='+',                     # N args
                        help='Type the Variables(must)',
                        metavar='Variables'
                        )
    parser.add_argument(
                        '-c', '--check',
                        action='store_true',            
                        help='Check all variables',
                        )
    parser.add_argument(
                        '-n', '--normalize',
                        action='store_false',            
                        help='Disable normalization',
                        )
    parser.add_argument(
                        '-x', '--blockx',
                        action='extend',            
                        nargs=4,                     
                        help='Select hyberslab of in x-direction(start, stride, count, block).',
                        type=int,
                        metavar='Int'
                        )
    parser.add_argument(
                        '-y', '--blocky',
                        action='extend',            
                        nargs=4,                     
                        help='Select hyberslab of in y-direction(start, stride, count, block).',
                        type=int,
                        metavar='Int'
                        )
    parser.add_argument(
                        '-z', '--blockz',
                        action='extend',            
                        nargs=4,                     
                        help='Select hyberslab of in z-direction(start, stride, count, block).',
                        type=int,
                        metavar='Int'
                        )
    args = parser.parse_args()
    if args.check:
        print('The variables are:')
        check(Path(args.path).expanduser().resolve()/args.filename)
        sys.exit(0)

    outputData(args.path, args.filename, args.variables, args.normalize, args.blockz, args.blocky, args.blockx).outputData(args.output)
