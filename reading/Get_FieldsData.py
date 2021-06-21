'''
READING IN MAGNETIC FIELDS
'''
import h5py
import numpy
import os

class fields_class():
    def __init__(self,fdir):
        pass
    
    def read_MagneticFields(self,fname):
        # Read magnetic field data
        f_open = open(fname)
        n = f_open.readlines(4)
        f_open.close()

        nelements = 29 #TODO: maybe not a fantastic way to do this???

        data = numpy.loadtxt(fname,skiprows=4)
        data = numpy.reshape(data, [nelements,n[0],n[1],n[2]])

        self.s = data[0,:,:,:]
        self.u = data[1,:,:,:]
        self.v = data[2,:,:,:]
        
        self.R = data[3,:,:,:]
        self.Z = data[4,:,:,:]

        self.phi    = data[5,:,:,:]
        self.Bsups  = data[6,:,:,:]
        self.Bsupu  = data[7,:,:,:]
        self.Bsupv  = data[8,:,:,:]

        self.BR  = data[9,:,:,:]
        self.BZ  = data[10,:,:,:]

        self.Bphi   = data[11,:,:,:]
        self.Bx     = data[12,:,:,:]
        self.By     = data[13,:,:,:]
        self.Bz     = data[14,:,:,:]
        self.B      = data[15,:,:,:]

        self.Ksups  = data[16,:,:,:]
        self.Ksups  = data[17,:,:,:]
        self.Ksups  = data[18,:,:,:]
        self.KR     = data[19,:,:,:]
        self.KZ     = data[20,:,:,:]
        self.Kphi   = data[21,:,:,:]
        self.Kx     = data[22,:,:,:]
        self.Ky     = data[23,:,:,:]
        self.Kz     = data[24,:,:,:]
        
        self.max_variation      = data[25,:,:,:]
        self.gradB_variation    = data[26,:,:,:]
        self.curv_variation     = data[27,:,:,:]
        self.para_variation     = data[28,:,:,:]
    
    def read_gradB(self,fname):
        data = numpy.loadtxt(fname)
        self.gradBs     = data[:,:,:,0]
        self.gradBu     = data[:,:,:,1]
        self.gradBv     = data[:,:,:,2]
    
    def read_curvB(self,fname):
        data = numpy.loadtxt(fname)
        self.norm_curv  = data[:,:,:,0]
        self.geod_curv  = data[:,:,:,1]

    def read_divB(self,fname):
        data = numpy.loadtxt(fname)
        self.divdB_rzv  = data[:,:,:,0]
        self.mod_dB     = data[:,:,:,1]
    
    '''
    Internal functions -- avoid storage in memory
    '''
    def x(self):
        return self.R*numpy.cos(self.v)
    def y(self):
        return self.R*numpy.sin(self.v)
    def z(self):
        return self.Z
    
    def gradPx(self):
        return self.Ky*self.Bz - self.Kz*self.By
    def gradPy(self):
        return self.Kz*self.Bx - self.Kx*self.Bz
    def gradPz(self):
        return self.Kx*self.By - self.Ky*self.Bx

    def max_variation(self):
        return self.s[self.s>0.99]



class external():
    '''
    external fields sub-sub class (sub class of fields)
    '''
    def __init__(self,fname):
        data = h5py.File(fname,'r')
        self.R      = array(data['grid/R'])
        self.Z      = array(data['grid/Z'])
        self.V      = array(data['grid/V'])

        self.Rmax   = float(data['grid/Rmax'])
        self.Rmax   = float(data['grid/Rmin'])
        self.Rmax   = float(data['grid/Zmax'])
        self.Rmax   = float(data['grid/Zmin'])
        self.Rmax   = float(data['grid/Vmax'])
        self.Rmax   = float(data['grid/Vmin'])

        self.Br     = array(data['fields/Br'])
        self.Bz     = array(data['fields/Bz'])
        self.Bv     = array(data['fields/Bv'])

        self.dr     = array(data['derivatives/dr'])
        self.dz     = array(data['derivatives/dz'])
        self.dv     = array(data['derivatives/dv'])
        self.dBrdr  = array(data['derivatives/dBrdr'])
        self.dBrdz  = array(data['derivatives/dBrdz'])
        self.dBrdv  = array(data['derivatives/dBrdv'])
        self.dBzdr  = array(data['derivatives/dBzdr'])
        self.dBzdz  = array(data['derivatives/dBzdz'])
        self.dBzdv  = array(data['derivatives/dBzdv'])
        self.dBvdr  = array(data['derivatives/dBvdr'])
        self.dBvdz  = array(data['derivatives/dBvdz'])
        self.dBvdv  = array(data['derivatives/dBvdv'])

    '''
    Internal routines
    '''
    def dBzdr_fd(self):
        return numpy.diff(self.Bz,n=1,axis=1)/self.dr

    def dBzdz_fd(self):
        return numpy.diff(self.Bz,n=1,axis=2)/self.dz

    def dBzdv_fd(self):
        return numpy.diff(self.Bz,n=1,axis=3)/self.dv

    def dBvdr_fd(self):
        return numpy.diff(self.Bv,n=1,axis=1)/self.dr

    def dBvdz_fd(self):
        return numpy.diff(self.Bv,n=1,axis=1)/self.dz

    def dBvdv_fd(self):
        return numpy.diff(self.Bv,n=1,axis=1)/self.dv

    def B(self):
        return numpy.sqrt(self.Br**2 + self.Bz**2 + self.Bv**2)
    



'''
BINDING TO FIELDS
'''
def Get_Fields(self):
    # fields = fields()
    pass

