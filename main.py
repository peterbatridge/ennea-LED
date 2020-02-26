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
import threading

STATE_LOCK = threading.Semaphore(1)


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
validFunctions = {
    'singleFrameSolidRandomColor': singleFrameSolidRandomColor,
    'singleFrameTrianglesRandomColor': singleFrameTrianglesRandomColor,
    'shiftColorSequenceOverNonagonGroups': shiftColorSequenceOverNonagonGroups,
    'shiftColorSequenceOverSetOfNonagonGroups': shiftColorSequenceOverSetOfNonagonGroups,
    'colorSwapAnimation': colorSwapAnimation,
    'fillSidesAnimation': fillSidesAnimation,
    'traceSidesAnimation': traceSidesAnimation,
    'rainbowCycle': rainbowCycle
}
fadeFramesArg = {
    'name': "Fade Frames",
    'optional': True,
    'rules': "0-100",
    'type': "number",
    'notes': "The number of cycles that will render between two frames with linearly interpolated colors. Recommended values between 0-10."
}
hangFramesArg = {
    'name': "Hang Frames",
    'optional': True,
    'rules': "0-10000",
    'type': "number" ,
    'notes': "The number of cycles that an animation will pause on each frame. Recommended values between 1-10."
}
soundFramesArg = {
    'name': "Sound Threshold Frames",
    'optional': True,
    'rules': "comma separated list",
    'type': "list of numbers",
    'notes': "Comma separated list of integers representing which frames in the animation to pause on until a sound threshold is met."
}
thresholdArg = {
    'name': "Sound Threshold",
    'optional': True,
    'rules': "0-1000",
    'type': "number",
    'notes': "The sound threshold for moving to the next frame in an animation. Recommended values between 0-200."
}
groupsOfNonagonsArg = {
    'name': "Groups of Nonagons",
    'optional': False,
    'rules': "select",
    'type': "groupOfNonagons",
    'notes': "Groups of nonagons, numbers can be seen in the reference image."
}
setsOfGroupsOfNonagonsArg = {
    'name': "Set of Groups of Nonagons",
    'optional': False,
    'rules': "select",
    'type': "setOfGroupsOfNonagons",
    'notes': "Sets of groups of nonagons, numbers can be seen in the reference image."
}
colorSequenceArg = {
    'name': "Color Sequence",
    'optional': False,
    'rules': "select",
    'type': "colorSequence",
    'notes': "List of colors."
}
soundMappingArg = {
    'name': "Sound Mapping",
    'optional': False,
    'rules': "select",
    'type': "audioMapping",
    'notes': "Mapping of sound amplitude ranges to peak value ranges."
}
colorOneArg = {
    'name': "Color One",
    'optional': False,
    'rules': "select",
    'type': "color",
    'notes': "A color."
}
colorTwoArg = {
    'name': "Color Two",
    'optional': False,
    'rules': "select",
    'type': "color",
    'notes': "A color."
}
colorThreeArg = {
    'name': "Color Three",
    'optional': False,
    'rules': "select",
    'type': "color",
    'notes': "A color."
}
directionArg = {
    'name': "Direction",
    'optional': False,
    'rules': "select",
    'type': "direction",
    'notes': "A direction."
}
modes = {
    '0': {
        'functionName': 'singleFrameSolidRandomColor',
        'args': [
            fadeFramesArg,
            hangFramesArg,
            thresholdArg
        ],
        'notes': "Will make all nonagons show the same random color. Takes no arguments or three arguments"
    },
    '1': {
        'functionName': 'singleFrameTrianglesRandomColor',
        'args': [
            fadeFramesArg,
            hangFramesArg,
            thresholdArg
        ],
        'notes': "Will make every other nonagon show the same random color. Takes no arguments or two arguments"
    },
    '2': {
        'functionName': 'shiftColorSequenceOverNonagonGroups',
        'args': [
            groupsOfNonagonsArg,
            colorSequenceArg,
            hangFramesArg,
            fadeFramesArg,
            soundFramesArg,
            thresholdArg,
            colorOneArg
        ],
        'notes': "Will make every other nonagon show the same random color. Takes no arguments or two arguments"
    },
    '3': {
        'functionName': 'shiftColorSequenceOverSetOfNonagonGroups',
        'args': [
            setsOfGroupsOfNonagonsArg,
            colorSequenceArg,
            hangFramesArg,
            fadeFramesArg,
            soundFramesArg,
            thresholdArg,
            colorOneArg
        ],
        'notes': "Will make every other nonagon show the same random color. Takes no arguments or two arguments"
    },
    '4': {
        'functionName': 'colorSwapAnimation',
        'args': [
            groupsOfNonagonsArg,
            colorOneArg,
            colorTwoArg,
            colorThreeArg,
            hangFramesArg,
            hangFramesArg
        ],
        'notes': "Will make every other nonagon show the same random color. Takes no arguments or two arguments"
    },
    '5': {
        'functionName': 'fillSidesAnimation',
        'args': [
            groupsOfNonagonsArg,
            colorSequenceArg,
            directionArg,
            directionArg,
            {
                'name': "Animation Width",
                'optional': False,
                'rules': "5-20",
                'type': "number" ,
                'notes': "The number of sides filled on the whole animation at once, recommended between 5-20"
            },
            hangFramesArg,
            fadeFramesArg
        ],
        'notes': "Will make every other nonagon show the same random color. Takes no arguments or two arguments"
    },
    '6': {
        'functionName': 'traceSidesAnimation',
        'args': [
            groupsOfNonagonsArg,
            colorSequenceArg,
            directionArg,
            hangFramesArg,
            fadeFramesArg
        ],
        'notes': "Will make every other nonagon show the same random color. Takes no arguments or two arguments"
    },
    '7': {
        'functionName': 'rainbowCycle',
        'args': [
            {
                'name': "Wait Time",
                'optional': False,
                'rules': '0-1',
                'type': "number",
                'notes': 'Amount of time in seconds between frames, zero is recommended, no higher than 1 second.'
            }
        ],
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
            STATE_LOCK.acquire()
            state = doc.to_dict()
            modeChanged = True
            STATE_LOCK.release()

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
    while True:
        STATE_LOCK.acquire()
        for m, mode in enumerate(state['mode']):
            # do an args check here
            if mode in modes.keys():
                func = validFunctions[modes[mode]['functionName']]
                args = ast.literal_eval(state['args'][m])
                try:
                    func(*args)
                except Exception as e:
                    print(func, args)
                    print("probably bad args", e)
        STATE_LOCK.release()
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
