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
def onColorsSnapshot(doc_snapshot, changes, read_time):
    global colorsDict
    for doc in doc_snapshot:
        print(u'Received document snapshot: {}'.format(doc.id))
        if doc.id == 'current':
            print(doc.to_dict())
modeDocRef = db.collection(u'state').document(u'current')
colorsDocRef = db.collection(u'constants').document(u'colors')
colorSequencesDocRef = db.collection(u'constants').document(u'colorSequences')
groupsOfNonagonsDocRef = db.collection(u'constants').document(u'groupsOfNonagons')
setsOfGroupsOfNonagonsDocRef = db.collection(u'constants').document(u'setsOfGroupsOfNonagons')
modeDocRef.on_snapshot(onModeSnapshot)
modeDocRef.on_snapshot(onColorsSnapshot)




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
