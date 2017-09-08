# only for python 2.7
# convert to .mat
import OpenEXR, Imath, numpy
import os.path
import scipy.io as sio
import numpy as np

depth_list_file = 'E:/renderdoc/scripts/python/exr_depth_list.txt'
mat_depth_list_file = 'E:/renderdoc/scripts/python/mat_depth_list.txt'
depth_save_root = 'E:/renderdoc/capture_log/processed'

depthListFile = open(depth_list_file, 'r')
matDepthListFile = open(mat_depth_list_file, 'w')

farplane = 1e6 # maybe not accurate

while 1:
    exr_depth_file = depthListFile.readline()
    exr_depth_file = exr_depth_file.split('\n')[0]
    if exr_depth_file == '':
        break

    if not os.path.exists(exr_depth_file):
        print 'error: no such file, %s'%exr_depth_file
        continue

    filePrefix = exr_depth_file.split('/')[-1]
    filePrefix = filePrefix.split('_depth.exr')[0]
    print filePrefix

    pt = Imath.PixelType(Imath.PixelType.FLOAT)
    exrFile = OpenEXR.InputFile(exr_depth_file)
    dw = exrFile.header()['dataWindow']
    size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)

    depthstr = exrFile.channel('D', pt) # S for stencil and D for depth in channels
    depth = numpy.fromstring(depthstr, dtype = numpy.float32)
    depth.shape = (size[1], size[0]) # Numpy arrays are (row, col)

    sio.savemat('{0}/{1}_depth_raw.mat'.format(depth_save_root,filePrefix),{'depth':depth})
    matDepthListFile.write('{0}/{1}_depth_raw.mat \n'.format(depth_save_root,filePrefix))
    exrFile.close()

    # convert raw depth to real distance
    # assuming x means depth value in depth buffer and d means real depth from camera
    # x = log(1/d+1)/log(farp + 1) ==> d = (farp+1)^x-1
    depth_real = np.power(farplane+1, depth)-1
    depth_real = 1/depth_real
    sio.savemat('{0}/{1}_depth.mat'.format(depth_save_root,filePrefix),{'depth':depth_real})

depthListFile.close()
matDepthListFile.close()