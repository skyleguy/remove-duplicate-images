import shutil, os
from PIL import Image
from os import listdir
from os.path import isfile, join
from pathlib import Path
from random import randint
import shutil
import time
import _thread

mypath = '/Users/kylelobsinger/Documents/remove-dupes/'
initialLocation = 'photo_library'
outPath = 'out'
directoryList = listdir(mypath + initialLocation)
processCount = 500

def loadObjects():
    start = time.time()
    print('loading images')
    myObjects = []
    placement = 0
    if len(directoryList) > 1:
        for x in range(len(directoryList)):
            if x % processCount == 0:
                print(x)
            if ('jp' in directoryList[x].lower() or 'png' in directoryList[x].lower()):
                i = Image.open(mypath + initialLocation + '/' + directoryList[x])
                width, height = i.size
                pixels = i.load()
                i.close()
                pixels = getRandomPixels(pixels, width, height)
                myObjects.append({
                    'name': directoryList[x],
                    'width': width,
                    'height': height,
                    'pixels': pixels,
                    'size': os.stat(mypath + initialLocation + '/' + directoryList[x]).st_size,
                    'biggest': directoryList[x],
                    'index': placement
                })
                placement += 1
    print('loading done')
    print("Loading took", time.time() - start, "to run")
    return myObjects

def getRandomPixels(pixels, width, height):
    randomPixels = []
    randomPixels.append(pixels[0,0])
    randomPixels.append(pixels[width - 1, height - 1])
    randomPixels.append(pixels[0, height - 1])
    randomPixels.append(pixels[width - 1, 0])
    randomPixels.append(pixels[width/2, height/2])
    randomPixels.append(pixels[0, height/2])
    randomPixels.append(pixels[width/2, 0])
    randomPixels.append(pixels[width - 1, height/2])
    randomPixels.append(pixels[width/2, height - 1])
    randomPixels.append(pixels[width/4, height/4])
    randomPixels.append(pixels[0, height/4])
    randomPixels.append(pixels[width/4, 0])
    randomPixels.append(pixels[width - 1, height/4])
    randomPixels.append(pixels[width/4, height - 1])
    randomPixels.append(pixels[width/8, height/8])
    randomPixels.append(pixels[0, height/8])
    randomPixels.append(pixels[width/8, 0])
    randomPixels.append(pixels[width - 1, height/8])
    randomPixels.append(pixels[width/8, height - 1])
    randomPixels.append(pixels[width/2, height/8])
    return randomPixels

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
    for x in range(20):
        if currObj['pixels'][x] != copyObj['pixels'][x]:
            return False
    return True

def copyObjToNewLocation(obj):
    shutil.copy2(mypath + initialLocation + '/' + obj['biggest'], mypath + outPath + '/' + obj['biggest'])

def biggerFileSize(currObj, copyObj):
    if currObj['size'] >= copyObj['size']:
        return currObj
    return copyObj

def tryToMakeDirectory():
    if os.path.isdir(mypath + '/' + outPath):
        print('folder existed, so deleting it and making new one')
        shutil.rmtree(mypath + '/' + outPath)
    os.mkdir(mypath + '/' + outPath)

def printSimilar(objects):
    start = time.time()
    x = 0
    for currImage in objects:
        copyToNewPlace = False
        if len(objects) > 1:
            if currImage['index'] % processCount == 0:
                print('processing: ' + str(currImage['index']))
            for image in objects[x+1:]:
                if areEqualSize(currImage, image):
                    if areSamePictureAllPixels(currImage, image):
                        if currImage['size'] >= image['size']:
                            image['biggest'] = currImage['name']
                            objects[image['index']] = image
                        copyToNewPlace = False
                        break
                    else:
                        copyToNewPlace = True
                else:
                    copyToNewPlace = True
            if copyToNewPlace:
                copyObjToNewLocation(currImage)
        x += 1
    copyObjToNewLocation(objects[-1])
    print("checking images", time.time() - start, "to run")

tryToMakeDirectory()
myObjects = loadObjects()
print('started with: ' + str(len(myObjects)))
printSimilar(myObjects)
print('ended with: ' + str(len(listdir(mypath + '/' + outPath))))
print('cut ' + str((len(myObjects) - len(listdir(mypath + '/' + outPath)))) + ' duplicates')