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
import traceback, sys
import shared

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
    'rainbowCycle': rainbowCycle,
    'gifAnimation' : gifAnimation,
    'drawRainingSquares': drawRainingSquares,
    'oppositeRains': oppositeRains,
    'pinwheelAudio': pinwheelAudio,
    'fireAudio': fireAudio,
    'fireRandom': fireRandom,
    'expandingCircles': expandingCircles,
    'expandingRectangle': expandingRectangle,
    'sparkleAudio': sparkleAudio,
    'bounce': bounce,
    'solidRandomColors': solidRandomColors,
    'solidColorCycle': solidColorCycle,
    'solidRandomColorEveryOther': solidRandomColorEveryOther,
    'fiveSolidRandomColors': fiveSolidRandomColors,
    'individualPinwheels': individualPinwheels,
    'trail': trail,
    'exMachinaMode': exMachinaMode,
    'solidColorAudioMode': solidColorAudioMode,
    'randomMode': randomMode,
    'offMode': offMode
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
maxFramesArg = {
    'name': "Max Frames",
    'optional': True,
    'rules': "0-10000",
    'type': "number" ,
    'notes': "The number of cycles that an animation run before exiting its while loop"
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
    'name': "Background Color",
    'optional': False,
    'rules': "select",
    'type': "color",
    'notes': "A color."
}
colorOneOptionalArg = {
    'name': "Color One",
    'optional': True,
    'rules': "select",
    'type': "color",
    'notes': "A color."
}
colorTwoOptionalArg = {
    'name': "Color Two",
    'optional': True,
    'rules': "select",
    'type': "color",
    'notes': "A color."
}
colorBackgroundOptionalArg = {
    'name': "Background Color",
    'optional': True,
    'rules': "select",
    'type': "color",
    'notes': "A color."
}
colorWheelOptionalOneArg = {
    'name': "Color Wheel One",
    'optional': True,
    'rules': "0-768",
    'type': "number",
    'notes': "A color."
}
colorWheelOptionalTwoArg = {
    'name': "Color Wheel Two",
    'optional': True,
    'rules': "0-768",
    'type': "number",
    'notes': "A color."
}
colorWheelOptionalThreeArg = {
    'name': "Color Wheel Three",
    'optional': True,
    'rules': "0-768",
    'type': "number",
    'notes': "A color."
}
borderWidth = {
    'name': "Border Width",
    'optional': True,
    'rules': "0-10",
    'type': "number",
    'notes': "A number of pixels for border width"
}
directionArg = {
    'name': "Direction",
    'optional': False,
    'rules': "select",
    'type': "direction",
    'notes': "A direction."
}
waitTimeArg = {
    'name': "Wait Time",
    'optional': False,
    'rules': '0-1',
    'type': "number",
    'notes': 'Amount of time in seconds between frames, zero is recommended, no higher than 1 second.'
}
modes = {
    '0': {
        'functionName': 'singleFrameSolidRandomColor',
        'args': [
            hangFramesArg,
            fadeFramesArg,
            thresholdArg
        ],
        'notes': "Will make all nonagons show the same random color. Takes no arguments or three arguments"
    },
    '1': {
        'functionName': 'singleFrameTrianglesRandomColor',
        'args': [
            hangFramesArg,
            fadeFramesArg,
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
            colorThreeArg
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
            fadeFramesArg,
            soundFramesArg,
            thresholdArg,
            colorOneArg
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
            fadeFramesArg,
            soundFramesArg,
            thresholdArg,
            colorOneArg
        ],
        'notes': "Will make every other nonagon show the same random color. Takes no arguments or two arguments"
    },
    '7': {
        'functionName': 'rainbowCycle',
        'args': [
            waitTimeArg
        ],
        'notes': "Will make every other nonagon show the same random color. Takes no arguments or two arguments"
    },
    '8': {
        'functionName': 'gifAnimation',
        'args': [
            {
                'name': "Gif Name",
                'optional': False,
                'rules': 'select',
                'type': "gifNames",
                'notes': 'Just the name not the value'
            }
        ],
        'notes': "Will make every other nonagon show the same random color. Takes no arguments or two arguments"
    },
    '9': {
        'functionName': 'drawRainingSquares',
        'args': [
            maxFramesArg,
            {
                'name': "",
                'optional': True,
                'rules': "",
                'type': "",
                'notes': ""
            },
            {
                'name': "",
                'optional': True,
                'rules': "",
                'type': "",
                'notes': ""
            }
        ],
        'notes': ''
    },
    '10': {
        'functionName': 'oppositeRains',
        'args': [
            colorOneOptionalArg,
            colorTwoOptionalArg,
            colorBackgroundOptionalArg
        ],
        'notes': ''
    },
    '11': {
        'functionName': 'pinwheelAudio',
        'args': [
            maxFramesArg,
            colorOneOptionalArg,
            colorBackgroundOptionalArg,
        ],
        'notes': ''
    },
    '12': {
        'functionName': 'fireAudio',
        'args': [
            maxFramesArg
        ],
        'notes': ''
    },
    '13': {
        'functionName': 'fireRandom',
        'args': [
            maxFramesArg
        ],
        'notes': ''
    },
    '14': {
        'functionName': 'expandingCircles',
        'args': [
            maxFramesArg,
            borderWidth
        ],
        'notes': ''
    },
    '15': {
        'functionName': 'expandingRectangle',
        'args': [
        ],
        'notes': ''
    },
    '16': {
        'functionName': 'sparkleAudio',
        'args': [
            maxFramesArg,
            colorOneOptionalArg,
            colorBackgroundOptionalArg,
            {
                'name': "All Nonagons Boolean",
                'optional': True,
                'rules': "0-1",
                'type': "number",
                'notes': "Boolean 0 or 1 for whether the rainbow should be for all nonagons or not"
            }
        ],
        'notes': ''
    },
    '17': {
        'functionName': 'bounce',
        'args': [
            colorOneOptionalArg,
            colorTwoOptionalArg
        ],
        'notes': ''
    },
    '18': {
        'functionName': 'solidRandomColors',
        'args': [
            waitTimeArg
        ],
        'notes': ''
    },
    '19': {
        'functionName': 'solidColorCycle',
        'args': [
            waitTimeArg
        ],
        'notes': ''
    },
    '20': {
        'functionName': 'solidRandomColorEveryOther',
        'args': [
            waitTimeArg
        ],
        'notes': ''
    },
    '21': {
        'functionName': 'fiveSolidRandomColors',
        'args': [
            waitTimeArg
        ],
        'notes': ''
    },
    '22': {
        'functionName': 'individualPinwheels',
        'args': [
            waitTimeArg
        ],
        'notes': ''
    },
    '23': {
        'functionName': 'trail',
        'args': [
            {
                'name': "Trail Length",
                'optional': False,
                'rules': '1-50',
                'type': "number",
                'notes': 'Amount of pixels to trail'
            }
        ],
        'notes': ''
    },
    '24': {
        'functionName': 'exMachinaMode',
        'args': [
            thresholdArg
        ],
        'notes': ''
    },
    '25': {
        'functionName': 'solidColorAudioMode',
        'args': [
            thresholdArg,
            maxFramesArg
        ],
        'notes': ''
    },
    '30': {
        'functionName': 'randomMode',
        'args': [
            {
            'name': 'Include Audio Modes Boolean',
            'optional': True,
            'rules': '0-1',
            'type': 'number',
            'notes': 'This represents whether or not audio modes should be included'
            },
            thresholdArg,
            maxFramesArg
        ],
        'notes': ''
    },
    '31': {
        'functionName': 'offMode',
        'args': [],
        'notes': 'Blanks the strip every second'
    }
}

# Use a service account
cred = credentials.Certificate('/home/pi/Desktop/ennea-LED/firestoreNonagon.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def onModeSnapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        print(u'Received document snapshot: {}'.format(doc.id))
        if doc.id == 'current':
            print(doc.to_dict())
            print("Update the state!")
            shared.state = doc.to_dict()
            shared.modeChanged = True


constantsDocRef = db.collection(u'constants')

def onConstantsSnapshot(doc_snapshot, changes, read_time):
    global colorsDict, colorSequences, groupsOfNonagons, setsOfGroupsOfNonagons, gifs
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
        # elif doc.id == 'gifs':
        #     for c in gifs.keys():
        #         if c not in docDict.keys():
        #             constantsDocRef.document('gifs').update({c : str(gifs[c])})
        #     for c in docDict.keys():
        #         if c not in gifs.keys():
        #             gifs[c] = ast.literal_eval(docDict[c])

modeDocRef = db.collection(u'state').document(u'current')
modeDocRef.on_snapshot(onModeSnapshot)
constantsDocRef.on_snapshot(onConstantsSnapshot)
constantsDocRef.document('modes').set(modes)


try:
    while True:
        try:
            for m, mode in enumerate(shared.state['mode']):
                # do an args check here
                if mode in modes.keys():
                    func = validFunctions[modes[mode]['functionName']]
                    args = ast.literal_eval(shared.state['args'][m])
                    try:
                        #frequencyBreakdownByNonagon()
                        #solidColorAudioMode()
                        func(*args)
                    except Exception as e:
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        print(func, args)
                        print(e)
                        traceback.print_exc()
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("Probably had the state changed and the loop broke:", e)
            traceback.print_exc()
except KeyboardInterrupt:
    print("Exiting due to keyboard interrupt.")
    strips.deinit()
