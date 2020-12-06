#!/usr/bin/python
import h5py
import sys
import argparse as ap
from pathlib import Path
from output import readHDF

class xdmfGener(object):
    def __init__(self, path, fn, varlist):
        self.path = Path(path).expanduser().resolve()
        self.fn   = self.path/fn
        self.varlist = varlist
        #----------- Read Information -----------#
        # You can use only
        self.geo  = h5py.File(self.fn, 'r')[varlist[0]].shape
        self.dim  = len(self.geo)
        self.xc   = readHDF(self.fn, 'xc')
        self.yc   = readHDF(self.fn, 'yc')
        self.zc   = readHDF(self.fn, 'zc')
        self.lem  = [len(self.zc), len(self.yc), len(self.xc)]

    def dump(self, fn_out, slab_mesh=[None, None, None], slab_var=[None, None, None]):
        #------------- Geometry Info -------------#
        def geo_plot(varname, index):
            array = getattr(self, varname)
            length = index[1] - index[0] + 1
            if len(array) == length:
                outfile.write(4*'\t'+'<DataItem Dimensions="{}" NumberType="Float" Precision="8" Format="HDF">\n'.format(len(array)))
                outfile.write(5*'\t'+'{}:/{}\n'.format(self.fn, varname))
                outfile.write(4*'\t'+'</DataItem>\n')
            else:
                outfile.write(4*'\t'+'<DataItem ItemType="HyperSlab" Dimensions="{}">\n'.format(length))
                outfile.write(5*'\t'+'<DataItem Dimensions="3 1" Format="XML">\n')

                outfile.write(6*'\t'+'{}\n'.format(index[0]))
                outfile.write(6*'\t'+'1\n')
                outfile.write(6*'\t'+'{}\n'.format(length))
                outfile.write(5*'\t'+'</DataItem>\n')
                outfile.write(5*'\t'+'<DataItem Dimensions="{}" NumberType="Float" Precision="8" Format="HDF">\n'.format(len(array)))
                outfile.write(6*'\t'+'{}:/{}\n'.format(self.fn, varname))
                outfile.write(5*'\t'+'</DataItem>\n')
                outfile.write(4*'\t'+'</DataItem>\n')
        #------------ Attribute Info ------------#
        def attr_plot(varname):
            if list(self.geo) == [len_vz, len_vy, len_vx]:
                outfile.write(3*'\t'+'<Attribute Name="{}" AttributeType="Scalar" Center="Node">\n'.format(varname))
                outfile.write(4*'\t'+'<DataItem Dimensions="{} {} {}" NumberType="Float" Precision="8" Format="HDF">\n'.format(self.geo[0],self.geo[1],self.geo[2]))
                outfile.write(5*'\t'+'{}:/{}\n'.format(self.fn, varname))
                outfile.write(4*'\t'+'</DataItem>\n')
                outfile.write(3*'\t'+'</Attribute>\n')
            else:
                outfile.write(3*'\t'+'<Attribute Name="{}" AttributeType="Scalar" Center="Node">\n'.format(varname))
                outfile.write(4*'\t'+'<DataItem ItemType="HyperSlab" Dimensions="{} {} {}">\n'.format(len_vz, len_vy, len_vx))
                outfile.write(5*'\t'+'<DataItem Dimensions="3 3" Format="XML">\n')
                outfile.write(6*'\t'+'{} {} {}\n'.format(slab_var[0][0], slab_var[1][0], slab_var[2][0]))
                outfile.write(6*'\t'+'1 1 1\n')
                outfile.write(6*'\t'+'{} {} {}\n'.format(len_vz, len_vy, len_vx))
                outfile.write(5*'\t'+'</DataItem>\n')
                outfile.write(5*'\t'+'<DataItem Dimensions="{} {} {}" NumberType="Float" Precision="8" Format="HDF">\n'.format(self.geo[0],self.geo[1], self.geo[2]))
                outfile.write(6*'\t'+'{}:/{}\n'.format(self.fn, varname))
                outfile.write(5*'\t'+'</DataItem>\n')
                outfile.write(4*'\t'+'</DataItem>\n')
                outfile.write(3*'\t'+'</Attribute>\n')

        #----- Judge If It Is The Same Mesh -----#
        for i in range(len(slab_var)):
            if slab_var[i] == None:
                slab_var[i] = [0, self.geo[i]-1]
        for i in range(len(slab_mesh)):
            if slab_mesh[i] == None:
                slab_mesh[i] = [0, self.lem[i]-1]
        len_xc = slab_mesh[2][1] - slab_mesh[2][0] + 1
        len_yc = slab_mesh[1][1] - slab_mesh[1][0] + 1
        len_zc = slab_mesh[0][1] - slab_mesh[0][0] + 1
        len_vx = slab_var[2][1] - slab_var[2][0] + 1
        len_vy = slab_var[1][1] - slab_var[1][0] + 1
        len_vz = slab_var[0][1] - slab_var[0][0] + 1
        if len_xc != len_vx or len_yc != len_vy or len_zc != len_vz:
            print('The shape of mesh and var is not the same.')
            print('Var:[{}, {}, {}]\n'.format(len_vx, len_vy, len_vz),
                  'Mesh:[{}, {}, {}]'.format(len_xc, len_yc, len_zc))
            sys.exit(1)
        #--------------- Dump File ---------------#
        outfile = open(self.path/fn_out, 'w')
        outfile.write('<?xml version="1.0" ?>\n')
        outfile.write('<!DOCTYPE Xdmf SYSTEM "Xdmf.dtd" []>\n')
        outfile.write('<Xdmf Version="2.0">\n')
        outfile.write('\t'+'<Domain>\n')
        outfile.write(2*'\t'+'<Grid Name="Structured Grid" GridType="Uniform">\n')
        outfile.write(3*'\t'+'<Topology TopologyType="3DRectMesh" NumberOfElements="{} {} {}"/>\n'.format(len_zc, len_yc, len_xc))
        outfile.write(3*'\t'+'<Geometry GeometryType="VXVYVZ">\n')
        #--------- Geometry Information ---------#
        geo_plot('xc', slab_mesh[2])
        geo_plot('yc', slab_mesh[1])
        geo_plot('zc', slab_mesh[0])
        outfile.write(3*'\t'+'</Geometry>\n')
        #--------- Attribute Infomation ---------#
        for var in self.varlist:
            attr_plot(var)
        outfile.write(2*'\t'+'</Grid>\n')
        outfile.write('\t'+'</Domain>\n')
        outfile.write('</Xdmf>\n')

if __name__ == '__main__':
    parser = ap.ArgumentParser(prog='HDFView', description='Generate a xdmf file to view HDF file.')
    parser.add_argument(
                        '-p', '--path',                # Option Name
                        required='True',               # Requirement
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
                        '-x', '--xrange',
                        action='extend',            
                        nargs=2,                     
                        help='Range of mesh x.',
                        type=int,
                        metavar='Num'
                        )
    parser.add_argument(
                        '-y', '--yrange',
                        action='extend',            
                        nargs=2,                     
                        help='Range of mesh y.',
                        type=int,
                        metavar='Num'
                        )
    parser.add_argument(
                        '-z', '--zrange',
                        action='extend',            
                        nargs=2,                     
                        help='Range of mesh z.',
                        type=int,
                        metavar='Num'
                        )
    parser.add_argument(
                        '--x2range',
                        action='extend',            
                        nargs=2,                     
                        help='Range of geometry x.',
                        type=int,
                        metavar='Num'
                        )
    parser.add_argument(
                        '--y2range',
                        action='extend',            
                        nargs=2,                     
                        help='Range of geometry y.',
                        type=int,
                        metavar='Num'
                        )
    parser.add_argument(
                        '--z2range',
                        action='extend',            
                        nargs=2,                     
                        help='Range of geometry z.',
                        type=int,
                        metavar='Num'
                        )
    args = parser.parse_args()
    
    xdmfGener(args.path,args.filename,args.variables).dump(args.output,[args.zrange,args.yrange,args.xrange], [args.z2range,args.y2range,args.x2range])
