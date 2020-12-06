import numpy as np
import sys
from scipy.optimize import fminbound

#----------------------------------------#
#---------- Find Maximum Value ----------#
#----------------------------------------#
def findMax(varx, vary, n):
    z = np.polyfit(varx, vary, n)
    f = np.poly1d(z)
    lmax = fminbound(-f, varx[0], varx[len(varx)-1])
    max = f(lmax)
    return lmax, max

def dz(z):
    nz = len(z)
    dz = np.zeros(nz)
    dz[0] = 2*z[0]
    for i in range(1, nz-1):
        dz[i] = 2*(z[i] - z[i-1]) - dz[i-1]
    dz[nz-1] = dz[nz-2]
    return dz


#----------------------------------------#
#------- Boundary Layer Thickness -------#
#----------------------------------------#
class bound(object):
    def delta(u, z):
        nz = len(u)
        delta = 0.0
        i = 0
        while u[i] < 0.99:
            i += 1
        delta = z[i-1] + (0.99-u[i-1])/(u[i]-u[i-1])*(z[i]-z[i-1])
        return delta

    def theta(u, dz):
        nz = len(u)
        theta = 0.0
        for i in range(1, nz-1):
            theta += u[i]*(1-u[i])*dz[i]
            if u[i] >= 0.99:
                break
        return theta
        
    def delta_dis(u, dz):
        nz = len(u)
        delta_dis = 0.0
        for i in range(1, nz - 1):
            delta_dis = delta_dis + (1 - u[i]) * dz[i]
            if u[i] >= 0.99:
                break
        return delta_dis
    
    def delta_en(u, dz):
        nz = len(u)
        delta_en = 0.0
        for i in range(1, nz-1):
            delta_en = delta_en+u[i]*(1-u[i]*u[i])*dz[i]
            if u[i] >= 0.99:
                break
        return delta_en
        
#----------------------------------------#
#------- Normalization Of Profile -------#
#----------------------------------------#
class profNorm(object):
    def uplus(var, utau):
        return var/utau

    def zplus(z, utau, nu):
        return z*utau/nu

    def usplus(var, utau):
        return var/utau/utau

#-----------------------------------------#
#---------- Average Of The Data ----------#
#-----------------------------------------#
class avg(object):
    def avg3d(var, direction):
        if var.ndim != 3:
            print('Error: Dims of the array is {}, but it must be three.'.format(var.ndim))
            sys.exit()

        if direction == 1:
            var_tar = np.zeros((var.shape[1], var.shape[2]))
            nloop   = var.shape[0]
            for i in range(nloop):
                var_tar = var_tar + var[i, :, :]

        if direction == 2:
            var_tar = np.zeros((var.shape[0], var.shape[2]))
            nloop   = var.shape[1]
            for i in range(nloop):
                var_tar = var_tar + var[:, i, :]

        if direction == 3:
            var_tar = np.zeros((var.shape[0], var.shape[1]))
            nloop   = var.shape[2]
            for i in range(nloop):
                var_tar = var_tar + var[:, :, i]

        return var_tar/nloop

    def avg2d(var, direction):
        if var.ndim != 2:
            print('Error: Dims of the array is {}, but it must be 2.'.format(var.ndim))
            sys.exit()

        if direction == 1:
            var_tar = np.zeros((var.shape[1]))
            nloop   = var.shape[0]
            for i in range(nloop):
                var_tar = var_tar + var[i, :]

        if direction == 2:
            var_tar = np.zeros((var.shape[0]))
            nloop   = var.shape[1]
            for i in range(nloop):
                var_tar = var_tar + var[:, i]
        
        return var_tar/nloop

    def avg1d(var):
        if var.ndim != 1:
            print('Error: Dims of the array is {}, but it must be 1.'.format(var.ndim))
            sys.exit()

        nloop = var.shape[0]
        for i in range(nloop):
            var_tar = var_tar + var[i, :]

        return var_tar/nloop

class div(object):
    def div1(var, d, dire):
        if var.ndim != 3:
            print('Error!: Dims of array is {}, but it must be 3'.format(var.ndim))
            sys.exit()

        dx, dy, dz = 0, 0, 0
        if dire == 1:
            dx = 1
        elif dire == 2:
            dy = 1
        elif dire == 3:
            dz = 1

        m = 0

        sh_in = var.shape
        var_out = np.zeros((sh_in[0]-2, sh_in[1]-2, sh_in[2]-2))
        for k in range(var_out.shape[0]):
            for j in range(var_out.shape[1]):
                for i in range(var_out.shape[2]):
                    if dire == 1:
                        m = i
                    elif dire == 2:
                        m = j
                    elif dire == 3:
                        m = k
                    var_out[k, j, i] = (var[k+1, j+1, i+1] - var[k+1-dz, j+1-dy, i+1-dx])*d[m]
        return var_out

    def div2(var, d2pp, d2pm, dire):
        if var.ndim != 3:
            print('Error!: Dims of array is {}, but it must be 3'.format(var.ndim))
            sys.exit()

        dx, dy, dz = 0, 0, 0
        if dire == 1:
            dx = 1
        elif dire == 2:
            dy = 1
        elif dire == 3:
            dz = 1

        m = 0

        sh_in = var.shape
        var_out = np.zeros((sh_in[0], sh_in[1]-2, sh_in[2]-2))
        for k in range(1, var_out.shape[0]-1):
            for j in range(var_out.shape[1]):
                for i in range(var_out.shape[2]):
                    if dire == 1:
                        m = i
                    elif dire == 2:
                        m = j
                    elif dire == 3:
                        m = k
                    var_out[k, j, i] = (var[k+1+dz, j+1+dy, i+1+dx]*d2pp[m] + var[k+1-dz, j+1-dy, i+1-dx]*d2pm[m]
                                    - var[k+1, j+1, i+1]*(d2pp[m]+d2pm[m]))
        return var_out


if __name__ == '__main__':
    var4test = np.array([[[1,2,3],[1,2,3]],[[1,2,3],[1,2,3]]])

    print(findMax([1,2,3,4,5],[1,2,3,4,5],3))
