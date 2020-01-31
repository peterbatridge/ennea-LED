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

###
# Available Functions
###
# modes = {
#     0: (singleFrameSolidRandomColor, []),
#     1: (singleFrameTrianglesRandomColor, []),
#     2: (exMachinaMode, []),
#     3: (colorSwapAnimation, [rowsTopToBottom, RED, BLUE, PURPLE, 10, 10]),
#     6: (rainbowCycle, [0]),
#     7: (traceSidesAnimation, [rowsTopToBottom, rainbowEight, 'top', 1, 0]),
#     8: (fillSidesAnimation, [topLeftToBottomRightDiagonal, [CYAN, BLUE, PURPLE, MAGENTA, RED, ORANGE], 'top', 'bot', 10, 1, 1]),
#     9: (handleAudio, [individualLeds, 31, fillLedsBasedOnVolume]),
#     10: (handleAudio, [verticalSides, 1, volumeMeterSides]),
#     11: (singleFrameSolidRandomColorWaitForSound, [150])
# }
# #    11: (handleAudioWithFrequency, [verticalSides, 1, volumeMeterSides]),

modes = {
    0: {
        'functionName': 'singleFrameSolidRandomColor',
        'args': {
            'fadeFrames': {
                'optional': True,
                'rules': "0-10000",
                'type': "number"
            },
            'hangFrames': {
                'optional': True,
                'rules': "0-10000",
                'type': "number"
            }
        },
        'notes': "Will make all nonagons show the same random color. Takes no arguments or two arguments"
    },
    1: {
        'functionName': 'singleFrameTrianglesRandomColor',
        'args': {
            'fadeFrames': {
                'optional': True,
                'rules': "0-10000",
                'type': "number"
            },
            'hangFrames': {
                'optional': True,
                'rules': "0-10000",
                'type': "number"
            }
        },
        'notes': "Will make every other nonagon show the same random color. Takes no arguments or two arguments"
    }
}

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
        elif doc.id == 'colorSequences':
            for c in colorSequences.keys():
                if c not in docDict.keys():
                    constantsDocRef.document('colorSequences').update({c : str(colorSequences[c])})
            for c in docDict.keys():
                if c not in colorSequences.keys():
                    colorSequences[c] = ast.literal_eval(docDict[c])
        elif doc.id == 'groupsOfNonagons':
            for c in groupsOfNonagons.keys():
                if c not in docDict.keys():
                    constantsDocRef.document('groupsOfNonagons').update({c : str(groupsOfNonagons[c])})
            for c in docDict.keys():
                if c not in groupsOfNonagons.keys():
                    groupsOfNonagons[c] = ast.literal_eval(docDict[c])
        elif doc.id == 'setsOfGroupsOfNonagons':
            for c in setsOfGroupsOfNonagons.keys():
                if c not in docDict.keys():
                    constantsDocRef.document('setsOfGroupsOfNonagons').update({c : str(setsOfGroupsOfNonagons[c])})
            for c in docDict.keys():
                if c not in setsOfGroupsOfNonagons.keys():
                    setsOfGroupsOfNonagons[c] = ast.literal_eval(docDict[c])
        elif doc.id == 'audioMappings':
            for c in audioMappings.keys():
                if c not in docDict.keys():
                    constantsDocRef.document('audioMappings').update({c : str(audioMappings[c])})
            for c in docDict.keys():
                if c not in audioMappings.keys():
                    audioMappings[c] = ast.literal_eval(docDict[c])

modeDocRef = db.collection(u'state').document(u'current')
modeDocRef.on_snapshot(onModeSnapshot)
constantsDocRef.on_snapshot(onConstantsSnapshot)
constantsDocRef.document('modes').set(modes)


try:        
    i = 0
    while True:
        for m, mode in enumerate(state['mode']):
            # do an args check here
            if mode in modes.keys():
                func = ast.literal_eval(modes[mode]['functionName'])
                args = ast.literal_eval(state['args'][m])
                try:
                    func(*args)
                except Exception as e:
                    print("probably bad args", e)
        #path() 
        #pinwheel(0)
        #columnsCycleThroughSequence(colorSeq)
        #rowCycleThroughSequence(colorSeq, 0.3)
        #exMachinaMode()
      #  
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
