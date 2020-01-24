import time
import random
import requests
import json
import credentials
import threading
from datetime import datetime, timedelta
import schedule
CTA_DATETIME = '%Y-%m-%dT%H:%M:%S'
CTA_LOCK = threading.Semaphore(1)
mm_bound_timer = False
chi_bound_timer = False
currentWeather = None
mode = 0
import board
import adafruit_dotstar as dotstar
from random import randrange
import math
from functools import partial
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# Use a service account
cred = credentials.Certificate('firestoreNonagon.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Create a callback on_snapshot function to capture changes
def on_snapshot(doc_snapshot, changes, read_time):
    global mode
    for doc in doc_snapshot:
        print(u'Received document snapshot: {}'.format(doc.id))
        if doc.id == 'current':
            print(doc.to_dict()['mode'])
            mode = doc.to_dict()['mode']

# Build document reference for the current state
doc_ref = db.collection(u'state').document(u'current')

# Watch the document
doc_watch = doc_ref.on_snapshot(on_snapshot)

# Using hardware SPI. 436 = 12*31 leds + 2*32 leds
num_pixels = 434
strips = dotstar.DotStar(board.SCLK, board.MOSI, num_pixels, brightness=0.1, baudrate=8000000, auto_write=False)

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
ORANGE = (255, 40, 0)
GREEN = (0, 255, 0)
TEAL = (0, 255, 120)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
MAGENTA = (255, 0, 20)
WHITE = (255, 255, 255)
BLANK = (0, 0, 0)
colors = [RED, ORANGE, YELLOW, GREEN, TEAL, CYAN,  BLUE, PURPLE, MAGENTA]
# https://openweathermap.org/weather-conditions
current_weather_base = "http://api.openweathermap.org/data/2.5/weather?q=Chicago,us&APPID="

cta_train_line_base = "http://lapi.transitchicago.com/api/1.0/ttpositions.aspx?rt=brn,p&outputType=JSON&key="
lastFrameNonagonColors = []
lastFrameSideColors = []

###
# Weather Functions
###

def getCurrentWeather():
    global currentWeather
    responseRaw = requests.get(current_weather_base+credentials.owm_api_key)
    response = json.loads(responseRaw.content)
    weatherCode = response['weather'][0]['id']
    temp = response['main']['temp']
    currentWeather = weatherCode, temp
    
def temperatureKToColor(tempK):
    temp = tempK * 1.8 - 459.67
    color = (0,0,0)
    if temp <= 0:
        # Purple / Pink
        color = (128, 0, 255)
    elif temp > 0 and temp < 20:
        # Dark Blue
        color = (64, 0, 255)
    elif temp >= 20 and  temp < 32:
        # blue
        color = (0, 0, 255)
    elif temp >= 32 and temp < 40:
        # light blue
        color = (0, 128, 255)
    elif temp >= 40 and temp < 50:
        # turqoise
        color = (0, 255, 191)
    elif temp >= 50 and temp < 60:
        # green
        color = (0, 255, 128)
    elif temp >= 60 and temp < 70:
        # yellow
        color = (255, 255, 0)
    elif temp >= 70 and temp < 80:
        # orange
        color = (255, 191, 0)
    elif temp >= 80 and temp < 90:
        # orangered
        color = (255, 128, 0)
    elif temp >= 90 and temp < 100:
        # pretty much red
        color = (255, 0 ,0)
    elif temp >= 100:
        # Purple/ Pink
        color = (128, 0, 255)
    return color

def getModeFromWeather(code, temp):
    color = temperatureKToColor(temp)
    if code>=200 and code<300:
        # Thunderstorms
        pass
    elif code>=300 and code<400:
        # Drizzle
        pass
    elif code>=500 and code<600:
        # Rain
        pass
    elif code>=600 and code<700:
        # Snow
        pass
    elif code>=700 and code<800:
        # Atmosphere (tornado/mist/ash)
        pass
    elif code==800:
        # Clear weather!
        pass
    elif code>800 and code<900:
        # Cloudy
        pass
    else:
        # Error? Unknown weather.
        pass

###
# Train Functions
###

def startTrainMode(direction):
    # Put into train mode
    print("Train probably fading in")
def stopTrainMode(direction):
    # Take out of train mode
    print("Train probably fading out")
def stopTrainTimer(direction):
    # Unlock train timer
    global chi_bound_timer, mm_bound_timer
    with CTA_LOCK:
        if direction == "chi":
            chi_bound_timer = False
        elif direction == "mm":
            mm_bound_timer = False
def startTrainTimerWithLock(lock, direction, timeDiff, timeToArrival):
    global chi_bound_timer, mm_bound_timer
    startTrainModeTime = timeDiff - timeToArrival
    print("Lock Acquired", lock)
    if not(lock) and timeDiff > timeToArrival and timeDiff > 60.0:
        print(timeDiff)
        if direction == "chi":
            chi_bound_timer = True
        elif direction == "mm":
            mm_bound_timer = True
        threading.Timer(startTrainModeTime, startTrainMode, args=[direction]).start()
        threading.Timer(startTrainModeTime+30, stopTrainMode, args=[direction]).start()
        threading.Timer(startTrainModeTime+90, stopTrainTimer, args=[direction]).start()
#Train Timings
#29:20 at chicago -> 29:59 probably audible -> 30:20 probably fading -> 31:25 stopped at merch Mart  => About a minute and a half before arrival at merch mart
#43:20 at merch mart -> 43:30 stopped -> 44: 00 leaving -> 45:00 probably audible -> 45:20 right nextdoor -> 45:40 at Chicago => About 40 seconds until arrival at chicago
# trDr = 1 for northbound and 5 for southbound
def getTrains():
    global mm_bound_timer, chi_bound_timer
    try:
        responseRaw = requests.post(cta_train_line_base + credentials.cta_api_key, data='''''', timeout=3)
        response = json.loads(responseRaw.content)
        print("Received API Response...")
        for train in response['ctatt']['route'][0]['train']:
            arrivalTime = datetime.strptime(train['arrT'], CTA_DATETIME)
            generatedTime = datetime.strptime(train['prdt'], CTA_DATETIME)
            timeDiff = (arrivalTime - generatedTime).total_seconds()
            # Train arriving at Merch Mart from Chicago
            if (train['trDr'] == '5' and train['nextStaNm']=="Merchandise Mart"):
                print("On the way to merch mart!")
                with CTA_LOCK:
                    startTrainTimerWithLock(mm_bound_timer, "mm", timeDiff, 90)
            # Train arriving at Chicago from Merch Mart
            if (train['trDr'] == '1' and train['nextStaNm']=="Chicago"):
                print("On the way to Chicago!")
                with CTA_LOCK:
                    startTrainTimerWithLock(chi_bound_timer, "chi", timeDiff, 20)
    except ReadTimeoutError as e:
        print("API Failure:", e)
    except Exception as e:
        print("Failure:", e)

def run_threaded(func):
    threading.Thread(target=func).start()

#currentWeather = getCurrentWeather()
#schedule.every(10).seconds.do(run_threaded, getTrains)
#schedule.every(10).minutes.do(run_threaded, getCurrentWeather)
# getModeFromWeather(currentWeather[0], currentWeather[1])


###
# Helper Functions
###

def blankStrip(background = BLANK):
    strips[0:434] = [background]*434
 
def setNonagonColor(n, color):
    strips[n*31:n*31+31] = [color]*31

def shiftLeft(colors, step):
    step = step % len(colors)
    return colors[step:] + colors[:step]

def shiftRight(colors, step):
    step = step % len(colors)
    return colors[-step:] + colors[:-step]

def setPatternOnEveryNonagon(pattern):
    for n in range(0,14):
        strips[n*31:(n*31)+31] = pattern

def setSide(n, side, color):
    nonagonStart = n*31
    sideStart = int(math.ceil(side*3.647))
    if sideStart+4 > 31:
        strips[nonagonStart+sideStart] = color
        strips[nonagonStart:nonagonStart+3] = [color] * 3
    else:
        strips[nonagonStart+sideStart:nonagonStart+sideStart+4] = [color]*4

def setPositionOnSide(n, side, pos, color):
    nonagonStart = n*31
    sideStart= int(math.ceil(side*3.647))
    positionWithinNonagon = (sideStart+pos) % 31
    strips[nonagonStart+positionWithinNonagon] = color

def generateSidesListFromNonagonAndSides(nonagon, sides):
    sidesList = []
    for side in sides:
        sidesList.append((nonagon, side))
    return sidesList

def singleLineFromStartAndStep(start, step):
    fillList = []
    itOne = start[0]
    itTwo = start[0]
    if len(start)>1:
        itTwo = start[1]
    itOne = (itOne+step)%9
    fillList.append(itOne)
    itTwo = (itTwo-step)
    if itTwo<0:
        itTwo = 9+itTwo
    if itOne!=itTwo:
        fillList.append(itTwo)
    return fillList

def fillListFromStartAndStep(start, step):
    fillList = start
    itOne = start[0]
    itTwo = start[0]
    if len(start)>1:
        itTwo = start[1]
    for i in range(0,step):
        itOne = (itOne+1)%9
        fillList.append(itOne)
        itTwo = (itTwo-1)
        if itTwo<0:
            itTwo = 9+itTwo
        if itOne!=itTwo:
            fillList.append(itTwo)
    return fillList

# Steps from 0 through 4
def sidesFromDirection(nonagon, step, direction, fill=True):
    func = singleLineFromStartAndStep
    if fill:
        func = fillListFromStartAndStep
    oddStart = {
        'top':      [4],
        'topLeft':  [5],
        'left':     [6],
        'botLeft':  [7,8],
        'bot':      [8,0],
        'botRight': [0,1],
        'right':    [2],
        'topRight': [3]
    }
    evenStart = {
        'top':      [4,5],
        'topLeft':  [6,5],
        'left':     [7],
        'botLeft':  [8],
        'bot':      [0],
        'botRight': [1],
        'right':    [2],
        'topRight': [4,3]
    }
    if (nonagon % 2 == 0):
        return generateSidesListFromNonagonAndSides(nonagon, func(evenStart[direction],step))
    else:
        return generateSidesListFromNonagonAndSides(nonagon, func(oddStart[direction],step))

def randomColor():
    return colors[randrange(9)]

def wheel(num):
    r =0
    g =0
    b = 0
    c = int(num/256)
    if c == 0:
        r = 255 - (num%256)
        g = num % 256
        b = 0
    elif c == 1:
        g = 255 - (num%256)
        b = num % 256
        r = 0
    else:
        b = 255 - (num%256)
        r = num % 256
        g = 0
    return (r,g,b)

###
# Pattern Functions
###
 
def rainbowCycle(wait):
    for j in range(768):
        for i in range(num_pixels):
            rc_index = (i * 768 // num_pixels) + j
            strips[i] = wheel(rc_index % 768)
        strips.show()
        time.sleep(wait) 
def bounce(background, foreground):
    pattern = [BLANK] * 31
    for frame in range(0,60):
        for i in range(num_pixels//3):
            if frame > 30:
                frame = 29 - (frame % 31)
            if frame == i: # or frame+15 == i or frame-15==i:
                pattern[i] = foreground
                #strips[(i+31)%61] = PURPLE
                #strips[(i+62)%93] = PURPLE
            else:
                pattern[i] = background           
                #strips[i+31] = BLUE
                #strips[i+62] = BLUE
        setPatternOnEveryNonagon(pattern)
        strips.show()

def solidRandomColors(wait=0.2):
    for n in range(0,14):
        strips[0:31] = [randomColor()]*31
        strips[31:62] = [randomColor()]*31
        strips[62:93] =  [randomColor()]*31
        strips[93:124] =  [randomColor()]*31
        strips[124:155]=  [randomColor()]*31
        strips[155:186] = [randomColor()]*31
        strips[186:217] = [randomColor()]*31
        strips[217:248] = [randomColor()]*31
        strips[248:279] = [randomColor()]*31
        strips[279:310] = [randomColor()]*31
        strips[310:341] = [randomColor()]*31
        strips[341:372] = [randomColor()]*31
        strips[372:403] = [randomColor()]*31
        strips[403:434] = [randomColor()]*31
        strips.show() 
        time.sleep(wait)

def solidColorCycle(wait=0.2):
    for n in range(0,14):
        setNonagonColor(n, colors[n%9])
        strips.show() 
        time.sleep(wait)

def solidRandomColorEveryOther(wait=1):
    for i in range(0,2):
        blankStrip()
        for q in range(0,14, 2):
            strips[(q+i)*31:(q+i+1)*31] = [randomColor()]*31
        strips.show()
        time.sleep(wait)

def fiveSolidRandomColors(wait=1):
    blankStrip()
    for i in range(0,5):
        x = randrange(0,14)
        setNonagonColor(x, randomColor())
    strips.show()
    time.sleep(wait)

def pinwheel(wait):
    for i in range(0,434):
        strips[0:434] = [(0,0,0)] * 434
        for q in range(0,62):
            strips[(i+(7*q))%434] = wheel(i)
            strips[(i+(7*q)+1)%434] = wheel(i+15)
            strips[(i+(7*q)+2)%434] = wheel(i+30)
        strips.show()
        time.sleep(wait)

def trail(length):
    for i in range(0,434):
        strips[0:434] = [(0,0,0)] *434
        for l in range(0, length):
            strips[(i+l)% 434] = wheel((i+l)%434)
        strips.show()

###
# Animation Core Functions
###

def groupCycleThroughSequence(group, colorSeq, wait):
    length = len(colorSeq)
    for i in range(0,length):
        for q, row in enumerate(group):
            color = colorSeq[(i+q)%length]
            for nonagon in row:
                setNonagonColor(nonagon, color)
        strips.show()
        time.sleep(wait)

def stepBetweenColors(startColor, endColor, stepCount, currentStep):
    r = ((endColor[0]-startColor[0]) * currentStep /stepCount)+startColor[0]
    g = ((endColor[1]-startColor[1]) * currentStep /stepCount)+startColor[1]
    b = ((endColor[2]-startColor[2]) * currentStep /stepCount)+startColor[2]
    return (int(r),int(g),int(b))

def getLastFrameColors(animation):
    global lastFrameNonagonColors
    if lastFrameNonagonColors!=[]:
        return lastFrameNonagonColors
    lastFrameColors = [BLANK]*14
    frame = animation[len(animation)-1]
    for g, group in enumerate(frame['groups']):
        for nonagon in group:
            lastFrameColors[nonagon] = frame['colors'][g]
    return lastFrameColors

def getLastFrameSideColors(animation):
    global lastFrameSideColors
    if lastFrameSideColors!=[]:
        return lastFrameSideColors
    lastFrameColors = [[BLANK]*9 for i in range(14)]
    frame = animation[len(animation)-1]
    for g, group in enumerate(frame['sides']):
        for side in group:
            lastFrameColors[side[0]][side[1]] = frame['colors'][g]
    return lastFrameColors

def animateNonagonGroups(animation, hangFrames, fadeFrames, backgroundColor = BLANK):
    global lastFrameNonagonColors
    lastFrameColors = getLastFrameColors(animation)
    for n, frame in enumerate(animation):
        for f in range(hangFrames+fadeFrames):
            blankStrip(backgroundColor)
            for g, group in enumerate(frame['groups']):
                color = frame['colors'][g]
                for nonagon in group:
                    if f < fadeFrames:
                        startColor = lastFrameColors[nonagon]
                        stepColor = stepBetweenColors(startColor, color, fadeFrames, f)
                        setNonagonColor(nonagon, stepColor)
                    else:
                        lastFrameColors[nonagon] = color
                        setNonagonColor(nonagon, color)
            strips.show()
    lastFrameNonagonColors = lastFrameColors

def animateSideGroups(animation, hangFrames, fadeFrames, backgroundColor = BLANK):
    global lastFrameSideColors
    lastFrameColors = getLastFrameSideColors(animation)
    for n, frame in enumerate(animation):
        for f in range(hangFrames+fadeFrames):
            blankStrip(backgroundColor)
            for g, group in enumerate(frame['sides']):
                color = frame['colors'][g]
                for side in group:
                    if f < fadeFrames:
                        startColor = lastFrameColors[side[0]][side[1]]
                        stepColor = stepBetweenColors(startColor, color, fadeFrames, f)
                        setSide(side[0], side[1], stepColor)
                    else:
                        lastFrameColors[side[0]][side[1]] = color
                        setSide(side[0], side[1], color)
            strips.show()
    lastFrameSideColors = lastFrameColors

###
# Groups Of Nonagons
###
everyNonagon = [[0,1,2,3,4,5,6,7,8,9,10,11,12,13]]

columnsLeftToRight = [[3,4],[1,2,5,6],[7,10, 11, 0],[8, 9, 12, 13]]
columnsRightToLeft= columnsLeftToRight[::-1]
rowsBottomToTop = [[0],[1,13],[2,12],[3,11],[4,10],[5,9],[6,8],[7]]
rowsTopToBottom = rowsBottomToTop[::-1]

bottomLeftToTopRightDiagonal = [[0,1],[2,3,13],[4,11,12],[5,10],[6,9],[7,8]]
bottomLeftToTopRightSharpDiagonal = [[1,3],[0,2,4],[5,11,13],[6,10,12],[7,9],[8]]
topRightToBottomLeftDiagonal = bottomLeftToTopRightDiagonal[::-1]
topRightToBottomLeftSharpDiagonal = bottomLeftToTopRightSharpDiagonal[::-1]

bottomRightToTopLeftDiagonal = [[0,13],[1,12],[2,11],[3,9,10],[4,5,8],[6,7]]
bottomRightToTopLeftSharpDiagonal = [[13],[0,12],[1,11,9],[2,10,8],[3,5,7],[4,6]]
topLeftToBottomRightDiagonal = bottomRightToTopLeftDiagonal[::-1]
topLeftToBottomRightSharpDiagonal = bottomRightToTopLeftSharpDiagonal[::-1]

triangles = [[0,2,4,6,8,10,12], [1,3,5,7,9,11,13]]

###
# Sets of Groups of Nonagons
###
eightDirectionGroups = [
    rowsTopToBottom,
    topLeftToBottomRightDiagonal,
    columnsLeftToRight,
    bottomLeftToTopRightDiagonal,
    rowsBottomToTop,
    bottomRightToTopLeftDiagonal,
    columnsRightToLeft,
    topRightToBottomLeftDiagonal
]

###
# Color Sequences
###
redAndBlue = [RED,BLUE]
redToBlueSeq8 = [RED, RED, ORANGE, ORANGE, CYAN, BLUE, MAGENTA, MAGENTA]
colorSeq2 = [RED, ORANGE, YELLOW, GREEN, TEAL, CYAN, BLUE, PURPLE, MAGENTA]
redFour = [CYAN,CYAN, BLUE, BLUE]
fourColdColors = [BLUE, PURPLE, BLUE, CYAN]
sixteenColdToWarmColors = [BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, MAGENTA, RED, RED, RED, RED, RED, RED, RED, MAGENTA]
TeganSequence = [RED, BLANK, BLANK, BLANK, BLANK, BLANK, BLANK, PURPLE, BLUE, GREEN, YELLOW, ORANGE]
ROYGCBPG = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, MAGENTA]

###
# Animation Generators
###

def colorSwapAnimation(groups, colorOne, colorTwo, colorBetween, hangFrames, fadeFrames):
    lengthOfGroup = len(groups)
    animation = []
    for i in range(1, int(lengthOfGroup/2)+1):
        colorList = [colorOne]*i +[colorBetween]*(lengthOfGroup-(2*i)) + [colorTwo]*i
        animation.append({
            'groups': groups,
            'colors': colorList
        })
    for i in range(int(lengthOfGroup/2), -1, -1):
        colorList =  [colorTwo]*i+[colorBetween]*(lengthOfGroup-(2*i)) + [colorOne]*i
        animation.append({
            'groups': groups,
            'colors': colorList
        })
    animateNonagonGroups(animation, hangFrames,fadeFrames)

def shiftColorSequenceOverNonagonGroups(groups, sequence, hangFrames, fadeFrames):
    animation = []
    for i in range(0, len(sequence)):
        animation.append({
            'groups': groups,
            'colors': shiftRight(sequence, i)
            })
    animateNonagonGroups(animation, hangFrames, fadeFrames)

def shiftColorSequenceOverSetOfNonagonGroups(setOfGroups, sequence, hangFrames, fadeFrames):
    animation = []
    for groupList in setOfGroups:
        for i in range(0, len(sequence)):
            animation.append({
                'groups': groupList,
                'colors': shiftRight(sequence, i)
                })
    animateNonagonGroups(animation, hangFrames, fadeFrames)

def traceSidesAnimation(nonagonGroups, sequence, direction, hangFrames, fadeFrames):
    animation = []
    for g, group in enumerate(nonagonGroups):

        for s in range(0, 5):
            sides = [[]]
            for n in group:
                sides[0] = sides[0] + sidesFromDirection(n, s, direction, False)
            animation.append({
                'sides': sides,
                'colors': [sequence[g]]})     
    animateSideGroups(animation, hangFrames, fadeFrames)

def fillSidesAnimation(nonagonGroups, seqeuence, fillSide, drainSide, width, hangFrames, fadeFrames):
    if width<5:
        width = 5
    animation = []
    numBuckets = len(nonagonGroups)
    buckets = [-1]*numBuckets
    filled = 0
    startIter = 0
    endIter = 1
    for i in range(numBuckets*width):
        sides = []
        colors = []
        if filled < width and endIter < numBuckets:
            if buckets[startIter] < 4:
                buckets[startIter] = buckets[startIter]+1
                filled = filled+1
            else:
                buckets[endIter] = buckets[endIter] + 1
                filled = filled+1
                if buckets[endIter] == 4:
                    endIter = endIter + 1
        # Remove a unit from the start bucket and add one to the end
        elif startIter < numBuckets:
            buckets[startIter] = buckets[startIter] - 1
            if buckets[startIter]<0:
                startIter = startIter+1
                if startIter == numBuckets:
                    break
            if endIter < numBuckets:
                buckets[endIter] = buckets[endIter] + 1
                filled = filled+1
                if buckets[endIter] == 4:
                    endIter = endIter + 1
        for b in range(0, numBuckets):
            if buckets[b]!=-1:
                sides.append([])
                colors.append(seqeuence[b])
                direction = fillSide
                if b == startIter and endIter>1:
                    direction = drainSide
                for n in nonagonGroups[b]:
                    sides[len(sides)-1] = sides[len(sides)-1] + sidesFromDirection(n, buckets[b], direction)

        animation.append({
        'sides': sides,
        'colors': colors
        })  

    animateSideGroups(animation, hangFrames, fadeFrames)

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
    cycleThroughColorSequenceWithEveryNonagon(fourColdColors, 15, 10)
    cycleThroughColorSequenceWithEveryNonagon(fourColdColors, 15, 10)
    shiftColorSequenceOverNonagonGroups(topLeftToBottomRightSharpDiagonal, sixteenColdToWarmColors, 1, 5)
    shiftColorSequenceOverNonagonGroups(topLeftToBottomRightSharpDiagonal, sixteenColdToWarmColors, 1, 5)
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

def singleFrameTrianglesRandomColor():
    animation = [{
        'groups': triangles,
        'colors': [randomColor(), randomColor()]
    }]
    animateNonagonGroups(animation, 10, 10)

modes = {
    0: (singleFrameSolidRandomColor, []),
    1: (singleFrameTrianglesRandomColor, []),
    2: (exMachinaMode, []),
    3: (colorSwapAnimation, [rowsTopToBottom, RED, BLUE, PURPLE, 10, 10]),
    4: (colorSwapAnimation, [rowsTopToBottom, RED, GREEN, PURPLE, 10, 10]),
    5: (colorSwapAnimation, [rowsTopToBottom, RED, YELLOW, PURPLE, 10, 10]),
    6: (rainbowCycle, [0]),
    7: (traceSidesAnimation, [rowsTopToBottom, ROYGCBPG, 'top', 1, 0]),
    8: (fillSidesAnimation, [topLeftToBottomRightDiagonal, [CYAN, BLUE, PURPLE, MAGENTA, RED, ORANGE], 'top', 'bot', 10, 1, 1])

}



import array

def remap_range(value, leftMin, leftMax, rightMin, rightMax):
    # this remaps a value from original (left) range to new (right) range
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
 
    # Convert the left range into a 0-1 range (int)
    valueScaled = int(value - leftMin) / int(leftSpan)
 
    # Convert the 0-1 range into a value in the right range.
    return int(rightMin + (valueScaled * rightSpan))

def handleAudio():
    dc_offset = 0  # DC offset in mic signal - if unusure, leave 0
    noise = 100  # Noise/hum/interference in mic signal
    samples = 60  # Length of buffer for dynamic level adjustment
    top = num_pixels + 1  # Allow dot to go slightly off scale
    
    peak = 0  # Used for falling dot
    dot_count = 0  # Frame counter for delaying dot-falling speed
    vol_count = 0  # Frame counter for storing past volume data
    
    lvl = 10  # Current "dampened" audio level
    min_level_avg = 0  # For dynamic adjustment of graph low & high
    max_level_avg = 512
    PEAK_FALL = 40
    # Collection of prior volume samples
    vol = array.array('H', [0] * samples)

    while True:
        n = mcp.read_adc(0)
        n = abs(n - 512 - dc_offset)  # Center on zero
    
        if n >= noise:  # Remove noise/hum
            n = n - noise

        # "Dampened" reading (else looks twitchy) - divide by 8 (2^3)
        lvl = int(((lvl * 7) + n) / 8)
    
        # Calculate bar height based on dynamic min/max levels (fixed point):
        height = top * (lvl - min_level_avg) / (max_level_avg - min_level_avg)
        # Clip output
        if height < 0:
            height = 0
        elif height > top:
            height = top
    
        # Keep 'peak' dot at top
        if height > peak:
            peak = height
    
        # Color pixels based on rainbow gradient
        for i in range(0, num_pixels):
            if i >= height:
                strips[i] = [0, 0, 0]
            else:
                strips[i] = wheel(remap_range(i, 0, (num_pixels - 1), 30, 150))
        if peak>0 and peak < num_pixels-1:
            strips[peak] = wheel(remap_range(peak, 0, (num_pixels - 1), 30, 150))

        dot_count = dot_count+1
        if dot_count >= PEAK_FALL:
            if peak > 0:
                peak = peak -1
            dot_count = 0
        # Save sample for dynamic leveling
        vol[vol_count] = n
    
        # Advance/rollover sample counter
        vol_count += 1
    
        if vol_count >= samples:
            vol_count = 0
    
        # Get volume range of prior frames
        min_level = vol[0]
        max_level = vol[0]
    
        for i in range(1, len(vol)):
            if vol[i] < min_level:
                min_level = vol[i]
            elif vol[i] > max_level:
                max_level = vol[i]
    
        # minlvl and maxlvl indicate the volume range over prior frames, used
        # for vertically scaling the output graph (so it looks interesting
        # regardless of volume level).  If they're too close together though
        # (e.g. at very low volume levels) the graph becomes super coarse
        # and 'jumpy'...so keep some minimum distance between them (this
        # also lets the graph go to zero when no sound is playing):
        if (max_level - min_level) < top:
            max_level = min_level + top
    
        # Dampen min/max levels - divide by 64 (2^6)
        min_level_avg = (min_level_avg * 63 + min_level) >> 6
        # fake rolling average - divide by 64 (2^6)
        max_level_avg = (max_level_avg * 63 + max_level) >> 6
        strips.show()
        #print(n)
threading.Thread(target=handleAudio).start()

try:        
    i = 0
    while True:
        # if mode in modes.keys():
        #     func, args = modes[mode]
        #     func(*args)
        #path() 
        #pinwheel(0)
        #columnsCycleThroughSequence(colorSeq)
        #rowCycleThroughSequence(colorSeq, 0.3)
        #exMachinaMode()
        
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
