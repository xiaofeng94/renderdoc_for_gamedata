# only for python 2.7
# convert to .mat

import OpenEXR, Imath, numpy
exr_root = 'E:/renderdoc/capture_log/processed'
filePrefix = 'GTA5_2017.08.29_22.48.31_frame7734_'

pt = Imath.PixelType(Imath.PixelType.FLOAT)
exrFile = OpenEXR.InputFile('{0}/{1}_depth.exr'.format(exr_root,filePrefix))
dw = exrFile.header()['dataWindow']
size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)

depthstr = exrFile.channel('D', pt) # S for stencil and D for depth in channels
depth = numpy.fromstring(depthstr, dtype = numpy.float32)
depth.shape = (size[1], size[0]) # Numpy arrays are (row, col)

import scipy.io as sio
sio.savemat("{0}/{1}_depth.mat".format(exr_root,filePrefix),{'depth':depth})

exrFile.close()

