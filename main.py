import random
import requests
import json
import credentials
from datetime import datetime, timedelta
from functools import partial
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from constants import *
from animation import *
import ast

# Use a service account
cred = credentials.Certificate('firestoreNonagon.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def onModeSnapshot(doc_snapshot, changes, read_time):
    global state, modeChanged
    for doc in doc_snapshot:
        print(u'Received document snapshot: {}'.format(doc.id))
        if doc.id == 'current':
            print(doc.to_dict())
            state = doc.to_dict()
            modeChanged = True

constantsDocRef = db.collection(u'constants')

def onConstantsSnapshot(doc_snapshot, changes, read_time):
    global colorsDict, colorSequences, groupsOfNonagons, setsOfGroupsOfNonagons
    for doc in doc_snapshot:
        print(u'Received document snapshot: {}'.format(doc.id))
        docDict = doc.to_dict()
        print(docDict)
        if doc.id == 'colors':
            for c in colorsDict.keys():
                if c not in docDict.keys():
                    constantsDocRef.document('colors').update({c : str(colorsDict[c])})
            for c in docDict.keys():
                if c not in colorsDict.keys():
                    colorsDict[c] = ast.literal_eval(docDict[c])
                    print("adding", docDict[c])
            print(colorsDict)
        elif doc.id == 'colorSequences':
            for c in colorSequences.keys():
                if c not in docDict.keys():
                    constantsDocRef.document('colorSequences').update({c : str(colorSequences[c])})        
        elif doc.id == 'groupsOfNonagons':
            for c in groupsOfNonagons.keys():
                if c not in docDict.keys():
                    constantsDocRef.document('groupsOfNonagons').update({c : str(groupsOfNonagons[c])})
        elif doc.id == 'setsOfGroupsOfNonagons':
            for c in setsOfGroupsOfNonagons.keys():
                if c not in docDict.keys():
                    constantsDocRef.document('setsOfGroupsOfNonagons').update({c : str(setsOfGroupsOfNonagons[c])})
            for c in docDict.keys():
                if c not in setsOfGroupsOfNonagons.keys():
                    setsOfGroupsOfNonagons[c] = ast.literal_eval(docDict[c])

modeDocRef = db.collection(u'state').document(u'current')
modeDocRef.on_snapshot(onModeSnapshot)
constantsDocRef.on_snapshot(onConstantsSnapshot)

###
# Modes
###    
def cycleThroughColorSequenceWithNonagonTriangles(sequence, hangFrames, fadeFrames):
    shiftColorSequenceOverNonagonGroups(triangles, sequence, hangFrames, fadeFrames)

def randomColorTriangles(hangFrames, fadeFrames):
    shiftColorSequenceOverNonagonGroups(triangles,[randomColor(), randomColor()], hangFrames, fadeFrames)

def cycleThroughColorSequenceWithEveryNonagon(sequence, hangFrames, fadeFrames):
    shiftColorSequenceOverNonagonGroups(everyNonagon, sequence, hangFrames, fadeFrames)
    
def exMachinaMode():
    cycleThroughColorSequenceWithEveryNonagon(coldFour, 15, 10)
    cycleThroughColorSequenceWithEveryNonagon(coldFour, 15, 10)
    shiftColorSequenceOverNonagonGroups(topLeftToBottomRightSharpDiagonal, coldToWarmSixteen, 1, 5)
    shiftColorSequenceOverNonagonGroups(topLeftToBottomRightSharpDiagonal, coldToWarmSixteen, 1, 5)
    fillSidesAnimation(topLeftToBottomRightDiagonal, [RED]*len(topLeftToBottomRightDiagonal), 'top', 'bot', 10, 1, 1)
    fillSidesAnimation(topLeftToBottomRightSharpDiagonal, [RED]*len(topLeftToBottomRightDiagonal), 'top', 'bot', 10, 1, 1)
    fillSidesAnimation(topLeftToBottomRightDiagonal, [RED]*len(topLeftToBottomRightDiagonal), 'top', 'bot', 10, 1, 1)
    fillSidesAnimation(topLeftToBottomRightSharpDiagonal, [RED]*len(topLeftToBottomRightDiagonal), 'top', 'bot', 10, 1, 1)

def singleFrameSolidRandomColor():
    animation = [{
        'groups': everyNonagon,
        'colors': [randomColor()]
    }]
    animateNonagonGroups(animation, 10, 10)

def singleFrameSolidRandomColorWaitForSound(threshold):
    animation = [{
        'groups': everyNonagon,
        'colors': [randomColor()]
    }]
    animateNonagonGroups(animation, 1, 10, [0], threshold)

def singleFrameTrianglesRandomColor():
    animation = [{
        'groups': triangles,
        'colors': [randomColor(), randomColor()]
    }]
    animateNonagonGroups(animation, 10, 10)

# def handleAudioThreaded():
#     threading.Thread(target=handleAudio).start()

modes = {
    0: (singleFrameSolidRandomColor, []),
    1: (singleFrameTrianglesRandomColor, []),
    2: (exMachinaMode, []),
    3: (colorSwapAnimation, [rowsTopToBottom, RED, BLUE, PURPLE, 10, 10]),
    4: (colorSwapAnimation, [rowsTopToBottom, RED, GREEN, PURPLE, 10, 10]),
    5: (colorSwapAnimation, [rowsTopToBottom, RED, YELLOW, PURPLE, 10, 10]),
    6: (rainbowCycle, [0]),
    7: (traceSidesAnimation, [rowsTopToBottom, rainbowEight, 'top', 1, 0]),
    8: (fillSidesAnimation, [topLeftToBottomRightDiagonal, [CYAN, BLUE, PURPLE, MAGENTA, RED, ORANGE], 'top', 'bot', 10, 1, 1]),
    9: (handleAudio, [individualLeds, 31, fillLedsBasedOnVolume]),
    10: (handleAudio, [verticalSides, 1, volumeMeterSides]),
    11: (handleAudioWithFrequency, [verticalSides, 1, volumeMeterSides]),
    12: (singleFrameSolidRandomColorWaitForSound, [150])
}

try:        
    i = 0
    while True:
        if state['mode'] in modes.keys():
            func, args = modes[state['mode']]
            func(*args)
        #path() 
        #pinwheel(0)
        #columnsCycleThroughSequence(colorSeq)
        #rowCycleThroughSequence(colorSeq, 0.3)
        #exMachinaMode()
      #  
        pass
        #fillSidesAnimation(rowsTopToBottom, ROYGCBPG, 'top', 'bot', 10, 1, 0)
        
        # fillSidesAnimation(triangles, redAndBlue, 'topRight', 'botLeft', 1, 1, 0)
        # fillSidesAnimation(triangles[::-1], redAndBlue, 'botLeft', 'topRight', 1, 1, 0)

        # fillSidesAnimation(topLeftToBottomRightSharpDiagonal, [MAGENTA], 10, 1, 1)
        # fillSidesAnimation(topLeftToBottomRightDiagonal, [MAGENTA], 10, 1, 1)
        # fillSidesAnimation(columnsLeftToRight, [MAGENTA], 10, 1, 1)
        #rain()
        #shiftColorSequenceOverNonagonGroups(bottomLeftToTopRightDiagonal, TeganSequence , 10, 10)
        
        
        #shiftColorSequenceOverSetOfNonagonGroups(eightDirectionGroups, redToBlueSeq8, 10, 10)
        #cycleThroughColorSequenceWithNonagonTriangles([RED, BLUE, ORANGE, GREEN], 10 ,10)
        #

        #colorSwapAnimation(bottomLeftToTopRightDiagonal, RED, BLUE, PURPLE, 10, 10)
        #groupCycleThroughSequenceFade(columnsLeftToRight, redToBlueSeq8, 10, 10, 0) 
        #cycleThroughSides()
        #sidesWithSequences(sideList, 2, 0)
      #  
        #trail(217)
        # Increase or decrease this to speed up or slow down the animation.
        #slice_alternating(0.1)
     
        #rain()
        #setStripColor
    
        #(WHITE, 0.5)
     
        # Increase or decrease this to speed up or slow down the animation.
        #slice_rainbow(0.1)
     
        #time.sleep(0.5)
     
        # Increase this number to slow down the rainbow animation.
        #bounce()
        #s
        #()
        #solidColorCycle
        #()
        #single_snake()
        #solidRandomColorEveryOther()
    #rain()

    #five_random_solid_colors()
                #schedule.run_pending()
                #rainbowCycle
                #(i)
except KeyboardInterrupt:
    print("Exiting due to keyboard interrupt.")
    strips.deinit()
#except Exception as e:
#    print("Error:", e)
