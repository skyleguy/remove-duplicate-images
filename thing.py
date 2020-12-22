import shutil, os
from os import listdir
from os.path import isfile, join
from pathlib import Path
from PIL import Image
from random import randint
import shutil

mypath = '/Users/kylelobsinger/Documents/remove-dupes/'
initialLocation = 'test_pics'
outPath = 'out'
directoryList = listdir(mypath + '/' + initialLocation)

def loadObjects():
    print('loading images')
    myObjects = []
    for x in range(len(directoryList)):
        if x % 50 == 0:
            print(x)
        if x is not len(directoryList) - 1 and len(directoryList) > 1:
            i = Image.open(mypath + initialLocation + '/' + directoryList[x])
            width, height = i.size
            pixels = i.load()
            myObjects.append({
                'name': directoryList[x],
                'width': width,
                'height': height,
                'pixels': pixels,
                'size': os.stat(mypath + initialLocation + '/' + directoryList[x]).st_size
            })
            i.close()
    print('loading done')
    return myObjects

def areEqualSize(currObj, copyObj):
    return currObj['height'] == copyObj['height'] and currObj['width'] == copyObj['width']

def areSamePictureRandomTimes(currObj, copyObj, randomTimes):
    for x in range(randomTimes):
        randomX = randint(0, currObj['width'] - 1)
        randomY = randint(0, currObj['height'] - 1)
        if currObj['pixels'][randomX, randomY] != copyObj['pixels'][randomX,randomY]:
            return False
    return True

def areSamePictureAllPixels(currObj, copyObj):
    for x in range(currObj['width']):
        for y in range(currObj['height']):
            if currObj['pixels'][x,y] != copyObj['pixels'][x,y]:
                return False
    return True

def copyObjToNewLocation(obj):
    shutil.copy(mypath + initialLocation + '/' + obj['name'], mypath + outPath + '/' + obj['name'])

def biggerFileSize(currObj, copyObj):
    print('comparing file size of ' + currObj['name'] + ' and ' + copyObj['name'])
    if currObj['size'] >= copyObj['size']:
        return currObj
    return copyObj

def tryToMakeDirectory():
    if os.path.isdir(mypath + '/' + outPath):
        print('folder existed, so deleting it and making new one')
        shutil.rmtree(mypath + '/' + outPath)
    os.mkdir(mypath + '/' + outPath)

def printSimilar(objects):
    for x in range(len(objects)):
        copyToNewPlace = False
        if x is not len(objects) - 1 and len(objects) > 1:
            currImage = objects[x]
            for y in range(x + 1, len(directoryList) - 1):
                isCopyImage = objects[y]
                if areEqualSize(currImage, isCopyImage):
                    if areSamePictureRandomTimes(currImage, isCopyImage, 20):
                        copyToNewPlace = False
                        break
                    else:
                        copyToNewPlace = True
                else:
                    copyToNewPlace = True
            if copyToNewPlace:
                copyObjToNewLocation(currImage)

tryToMakeDirectory()
myObjects = loadObjects()
printSimilar(myObjects)
