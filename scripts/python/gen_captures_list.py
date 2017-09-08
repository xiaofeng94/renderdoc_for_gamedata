# for python 2.7
import os

def generateListTxt(targetFileName, rootDir):
    #should check whether targetFile exists
    targetFile = open(targetFileName, 'w+')

    for parent, dirNames, fileNames in os.walk(rootDir):  
        for fileName in fileNames:
            fullName = '%s/%s'%(capture_file_root, fileName)
            targetFile.write('%s\n'%fullName)

    targetFile.close()


capture_file_root = 'E:/playing-for-data/data/captures' # no \\ in file path
target_file = 'capture_list.txt'

generateListTxt(target_file, capture_file_root)

print 'Done..'