#for python 2.7
def getfinalPassForGTAV():
    """ Returns the EventID of the pass that draws the final image without distortion (before HUD). """
    potentialPassIds = [i for i,call in enumerate(drawcalls) if call.name.find('Draw(3)') >= 0]
    # for id_val in potentialPassIds:
    #     print '{0}: {1}'.format(id_val,drawcalls[id_val].eventID)

    assert(len(potentialPassIds) > 1, 'Found not enough potential final passes for GTAV.')
    finalPassId = potentialPassIds[-2] # last Draw(3) for gta is distorted frame
    return drawcalls[finalPassId].eventID
    
def getColorBuffers(eventId):
    """ Sets the pipeline to eventId and returns the ids of bound render targets. """
    pyrenderdoc.SetEventID(None, eventId)
    commonState   = pyrenderdoc.CurPipelineState
    outputTargets = commonState.GetOutputTargets()
    return [t for t in outputTargets if str(t.Id) <> '0']

def getDepthBuffer():
    # find an event that use depth to initialise depth
    numColorTargets = 4
    potentialPos = [i for i,call in enumerate(drawcalls) if call.name.find('%d Targets + Depth)' % numColorTargets) >= 0]
    assert(len(potentialPos) >= 1, 'Found not enough potential events for depth.')
    # print 'parent pass containing depth {0}: {1}'.format(potentialPos[-1], drawcalls[potentialPos[0]].eventID)
    pChildrenDraws = drawcalls[potentialPos[0]].children
    pChildDraw = pChildrenDraws[-1] # last child contains all depth
    # print 'child pass containing depth {0}'.format(pChildDraw.eventID)

    pyrenderdoc.SetEventID(None, pChildDraw.eventID)

    # get depth target
    depthTarget = pyrenderdoc.CurPipelineState.GetDepthTarget()
    return depthTarget


config = {}
config['py_lib_dir']  = 'F:\\Anaconda2\\Lib'      # where we find the Python libraries
config['save_dir']    = 'E:/renderdoc/capture_log/processed' # where we store extraction results

# Add python libraries
import sys
sys.path.append(config['py_lib_dir'])

from os import mkdir
from os.path import dirname, basename, exists

list_file = 'E:\\renderdoc\\scripts\\python\\capture_list.txt'
depth_list_file = 'E:\\renderdoc\\scripts\\python\\exr_depth_list.txt'

listFile = open(list_file, 'r')
depthListFile = open(depth_list_file, 'w+')

while 1:
    curr_log_file = listFile.readline()
    # remote \n from readline()
    curr_log_file = curr_log_file.split('\n')[0]
    if curr_log_file == '':
        break

    if not exists(curr_log_file):
        print 'no such file, %s'%curr_log_file
        continue

    # open capture file
    pyrenderdoc.LoadLogfile(curr_log_file, curr_log_file, 0, 1)

    # creates a prefixes for files and directories from logfilename
    config['dir_prefix']  = lambda logFilename : ''       
    config['file_prefix'] = lambda logFilename : basename(logFilename)[:-4] + '_'

    # Get prefix and set up directory
    dirPrefix  = config['dir_prefix'](pyrenderdoc.LogFileName)
    filePrefix = config['file_prefix'](pyrenderdoc.LogFileName)
    saveDir    = '%s/%s' % (config['save_dir'], dirPrefix)
    if not exists(saveDir):
        mkdir(saveDir)
        pass
    # print 'Output directory is %s' % saveDir
    print 'File prefix is %s' % filePrefix

    # Get drawcalls
    drawcalls = pyrenderdoc.GetDrawcalls()
    # print 'Found %d drawcalls.' % len(drawcalls)


    # Save color frame
    finalPassId = getfinalPassForGTAV()
    assert(finalPassId == 0, 'Found not enough potential final passes.')
    # print 'color {0}'.format(finalPassId)

    colorbuffers = getColorBuffers(finalPassId)
    assert(len(colorbuffers) == 1, 'Found %d potential final render targets.' % len(colorbuffers))
    pyrenderdoc.SaveTexture(colorbuffers[0].Id, '{0}{1}_final.jpg'.format(saveDir, filePrefix))

    # Save depth target
    # depthTarget = pyrenderdoc.CurPipelineState.GetDepthTarget()
    depthTarget = getDepthBuffer()
    # print 'depth {0}'.format(depthTarget.Id)
    pyrenderdoc.SaveTexture(depthTarget.Id, '{0}{1}_depth.exr'.format(saveDir,filePrefix))
    depthListFile.write('{0}{1}_depth.exr \n'.format(saveDir,filePrefix))

    # print 'done.'

    pyrenderdoc.CloseLogfile()

listFile.close()
depthListFile.close()

# # get plane distance
# planeDist = pyrenderdoc.GetClipPlane()
# print '({0},{1})'.format(planeDist[0], planeDist[1])
# print '(%.15f, %e)'%(planeDist[0], planeDist[1])

# close pyrenderdoc
# pyrenderdoc.AppWindow.Close()

