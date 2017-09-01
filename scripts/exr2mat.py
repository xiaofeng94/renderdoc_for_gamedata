# only for python 2.7

import OpenEXR, Imath, numpy

exr_root = 'E:/renderdoc/capture_log/processed'

pt = Imath.PixelType(Imath.PixelType.FLOAT)
exrFile = OpenEXR.InputFile("{0}/py_depth3.exr".format(exr_root))
dw = exrFile.header()['dataWindow']
size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)

depthstr = exrFile.channel('D', pt) # S for stencil and D for depth in channels
depth = numpy.fromstring(depthstr, dtype = numpy.float32)
depth.shape = (size[1], size[0]) # Numpy arrays are (row, col)

print depth[0, 0]

import scipy.io as sio
sio.savemat("{0}/py_depth3.mat".format(exr_root),{'depth':depth})

exrFile.close()
