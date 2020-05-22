from constants import *
import board
import adafruit_dotstar as dotstar
from random import randrange, shuffle
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import time
import numpy as np 
import ast
from shapes import *

class Animation:
    def __init__(self):
        self.frames = {}
        self.hangFrames = 1
        self.fadeFrames = 0
        self.soundFrames = []
        self.soundThreshold = 0
        self.backgroundColor = BLANK


state = {
    'mode': [0],
    'args': ["[]"]
}
modeChanged = False

CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Using hardware SPI. 436 = 12*31 leds + 2*32 leds
num_pixels = 434
strips = dotstar.DotStar(board.SCLK, board.MOSI, num_pixels, brightness=0.1, baudrate=10000000, auto_write=False)

lastFrameNonagonColors = []
lastFrameSideColors = []

wheelIterator = 0

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

def nextInWheel(step = 1):
    global wheelIterator
    wheelIterator = (wheelIterator + step) % 768
    return wheelIterator

def wheelComplementaryColor(color):
    return (color + 384) % 768

def dimColor(color, fraction):
    dimColor = [0,0,0]
    dimColor[0] = int(color[0] * fraction)
    dimColor[1] = int(color[1] * fraction)
    dimColor[2] = int(color[2] * fraction)
    return dimColor

def complementaryColor(color):
    r = color[0]
    g = color[1]
    b = color[2]
    r2 = max(r,b,g) + min(r,b,g) - r   
    b2 = max(r,b,g) + min(r,b,g) - b
    g2 = max(r,b,g) + min(r,b,g) - g
    return [r2, g2, b2]    

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

def remap_range(value, remap):
    for m, maxes in enumerate(remap):
        if value <= maxes[0]:
            if m >0:
                return int((value / (maxes[0])*(maxes[1]-remap[m-1][1]))+remap[m-1][1])
            else:
                return int((value / maxes[0])* maxes[1])

def waitUntilSoundReachesThreshold(threshold):
    global modeChanged
    peakToPeak = 0
    noise = 15
    samplesLen = 10
    sampleArr = [0] * samplesLen
    sampleCount = 0
    fullSample = False
    while (peakToPeak<threshold or not fullSample) and not modeChanged:
        signalMax = 0
        signalMin = 1023
        sample = mcp.read_adc(0)
        sampleArr[sampleCount] = sample
        if sampleCount+1 == samplesLen:
            fullSample = True
        sampleCount =(sampleCount+1)%samplesLen
        for i in range(samplesLen):
            if sampleArr[i] > signalMax:
                signalMax = sampleArr[i]
            elif sampleArr[i] < signalMin:
                signalMin = sampleArr[i]
        
        peakToPeak = signalMax - signalMin
        peakToPeak = 0 if peakToPeak <= noise else peakToPeak-noise
        if peakToPeak < 0:
            peakToPeak = 0
        elif peakToPeak > 1023:
            peakToPeak = 1023
    modeChanged = False

def fillLedsBasedOnVolume(peak):
    blankStrip()
    for i in range(peak):
        strips[i] = RED
    strips.show()

def volumeMeterSides(peak):
    blankStrip()
    
    for i in range(peak):
        color = wheel(255 - int((i/40) * 255))
        groupNum = i //5
        fill = i % 5
        for nonagon in rowsBottomToTop[groupNum]:
            sides = sidesFromDirection(nonagon, fill, 'bot')
            for side in sides:
                setSide(nonagon, side[1], color)
    strips.show()

def handleAudio(remap, rateOfPeakDescent, functionCalledWithPeak, **kwargs):
    global modeChanged
    peak = 0
    noise = 15
    samplesLen = 10
    sampleArr = [0] * samplesLen
    sampleCount = 0
    totalFrames = 0
    while not modeChanged: 
        signalMax = 0
        signalMin = 1023
        sample = mcp.read_adc(0)
        sampleArr[sampleCount] = sample
        sampleCount =(sampleCount+1)%samplesLen
        for i in range(samplesLen):
            if sampleArr[i] > signalMax:
                signalMax = sampleArr[i]
            elif sampleArr[i] < signalMin:
                signalMin = sampleArr[i]
        
        peakToPeak = signalMax - signalMin
        peakToPeak = 0 if peakToPeak <= noise else peakToPeak-noise
        if peakToPeak < 0:
            peakToPeak = 0
        elif peakToPeak > 1023:
            peakToPeak = 1023

        peakToPeak = remap_range(peakToPeak, remap)
        if (peak>=rateOfPeakDescent):
            peak = peak - rateOfPeakDescent
        elif (peak>0):
            peak - peak-1
        if peakToPeak > peak:
            peak = peakToPeak

        totalFrames = totalFrames+1
        functionCalledWithPeak(peak, **kwargs)
    modeChanged = False

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
    for i in range(0,768):
        strips[0:434] = [(0,0,0)] * 434
        for q in range(0,62):
            strips[(i+(7*q))%434] = wheel(i)
            strips[(i+(7*q)+1)%434] = wheel((i+30)%768)
            strips[(i+(7*q)+2)%434] = wheel((i+60)%768)
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

def animateNonagonGroups(animation, hangFrames, fadeFrames, soundFrames = [], soundThreshold=0,  backgroundColor = BLANK):
    global lastFrameNonagonColors
    lastFrameColors = getLastFrameColors(animation)
    for n, frame in enumerate(animation):
        for f in range(hangFrames+fadeFrames):
            blankStrip(backgroundColor)
            if soundThreshold > 0 and n in soundFrames and f >= fadeFrames:
                for g, group in enumerate(frame['groups']):
                    color = frame['colors'][g]
                    for nonagon in group:
                        lastFrameColors[nonagon] = color
                        setNonagonColor(nonagon, color)
                waitUntilSoundReachesThreshold(soundThreshold)
            else:
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

def applyScaleAndGetColor(color):
    if color == 255:
        return WHITE
    elif color == 254:
        return BLANK
    return wheel(int((color/253.0)*768))

def gifAnimation(name, hangFrames, fadeFrames):
    global gifs
    animation = gifs[name]['frames']
    for n, s in enumerate(animation):
        # for f in range(hangFrames+fadeFrames):
        #     if f < fadeFrames:
        strip = list(map(wheel, s))
        strips[0:434] = strip
        strips.show()




###
# Animations With Shape Objects
###

def drawShapes(shapes, borderWidth, backgroundColor, dimFactor=1):
    for p in range(0,434):
        numColors = 0
        color = backgroundColor
        r = 0
        g = 0
        b = 0
        for shape in shapes:
            if ((borderWidth==0 and shape.contains(PIXEL_POSITIONS[p][0], PIXEL_POSITIONS[p][1])) or 
            (borderWidth>0 and shape.containsInBorder(PIXEL_POSITIONS[p][0], PIXEL_POSITIONS[p][1], borderWidth))): 
                numColors = numColors + 1
                r = r + (shape.color[0] * shape.color[0])
                g = g + (shape.color[1] * shape.color[1])
                b = b + (shape.color[2] * shape.color[2])
        if numColors > 0:
            color = [int(math.sqrt(r/numColors)), int(math.sqrt(g/numColors)), int(math.sqrt(b/numColors))]
        strips[p] = dimColor(color, dimFactor)

def drawFallingRect():
    rect = Rectangle(50, 50, BLUE, 10, 100, None)
    while True:
        drawShapes([rect], 0, RED)
        rect.rotate(30)
        #rect.rotate(5)
        #print("**************")
        #for p in rect.points:
        #    print(p.x, " ", p.y)
        strips.show()    

def expandingRectangle():
    sq = Rectangle(50, 50, BLUE, 1, 1, Transformations(0,0,1,1))
    background = BLANK
    for i in range(0, 100):
        drawShapes([sq], 0, background)
        strips.show()
        sq.transformations = Transformations(0,0,1,1)
        sq.transform()

def drawSparkleWithPeak(peak, fadeFrames):
    baseColor = nextInWheel(3)
    if peak >= 28:
        peak = 28
    if peak < 3:
        peak = 3
    onNum = peak
    for n in range(0,14):
        mask = [BLANK] * 31
        mask[0:onNum] = [wheel((baseColor+n*50)%768)] * onNum
        shuffle(mask)
        for i in range(0, fadeFrames):        
            for p in range(0,31):
                strips[n*31+p] = stepBetweenColors(strips[n*31+p], mask[p], fadeFrames, i)
    strips.show()

def sparkleAudio(fadeFrames=2):
    handleAudio(verticalSides, 3, drawSparkleWithPeak, fadeFrames=fadeFrames)

def oppositeRains():
    upTransform = Transformations(0,-2,0)
    downTransform = Transformations(0,2,0)
    circles = [Circle(42, 100, MAGENTA, 7, upTransform), Circle(70, 100, MAGENTA, 7, upTransform), 
            Circle(29, 0 , MAGENTA, 7, downTransform), Circle(56, 0, MAGENTA, 7 , downTransform)]
    for i in range(0, 100):
        drawShapes(circles, 0, BLANK)
        strips.show()
        if i == 50:
            circles[0].transformations = downTransform
            circles[1].transformations = downTransform
            circles[2].transformations = upTransform
            circles[3].transformations = upTransform
        circles[0].transform()
        circles[1].transform()
        circles[2].transform()
        circles[3].transform()
   
def drawRainingSquares(colorWheelLowerBound=256, colorWheelUpperBound=512):
    global modeChanged
    squares = []
    for i in range(0,10):
        transformation = Transformations(0, randrange(1,3), 0)
        squares.append(Rectangle(i*10,randrange(0,SCREEN), wheel(randrange(colorWheelLowerBound,colorWheelUpperBound)), 10, 10, transformation))
    while not modeChanged:
        drawShapes(squares, 0, BLANK)

        # Perform Transform & check for offscreens
        for j in range(0, len(squares)):
            squares[j].transform()
            if squares[j].isOffscreen(SCREEN, SCREEN):
                squares[j].y = 0
                squares[j].color = wheel(randrange(colorWheelLowerBound,colorWheelUpperBound))
                squares[j].transformations = Transformations(0, randrange(1,3), 0)
        strips.show()
    modeChanged = False

def pinwheelAudio(color = None, backgroundColor = None):
    rect = Rectangle(50, 50, color, 10, 100, None)
    handleAudio(verticalSides, 3, drawPinwheelWithPeak, rect=rect, color=color, backgroundColor=backgroundColor)

def drawPinwheelWithPeak(peak, rect, color, backgroundColor):
    rect.rotate(peak)
    if color == None or backgroundColor == None:
        wheelPos = nextInWheel()
        color = wheel(wheelPos)
        backgroundColor = wheel(wheelComplementaryColor(wheelPos))
    rect.color = color
    drawShapes([rect], 0, backgroundColor)
    strips.show()

def drawFireWithPeak(peak, circles, colorWheelLowerBound=20, colorWheelUpperBound=60, backgroundColorWheel=0):
    if peak < 11:
        peak = 10
    drawShapes(circles, 0, wheel(backgroundColorWheel), peak/39.0)
    strips.show()
    for i in range(0, len(circles)):
        circles[i].transform()
        if circles[i].isOffscreen(SCREEN, SCREEN):
            circles[i].x = 25+(i*5)
            circles[i].y = SCREEN
            circles[i].color = wheel(randrange(colorWheelLowerBound,colorWheelUpperBound))
            circles[i].transformations = Transformations(randrange(-2,2), randrange(-5,-2), 0)

def fireAudio(colorWheelLowerBound=20, colorWheelUpperBound=60, backgroundColorWheel=0):
    circles = []
    radius = 5
    for i in range(0,10):
        transformation = Transformations(randrange(-2,2), randrange(-5, -2), 0)
        circles.append(Circle(
            SCREEN_X_BEGIN+(i*5), 
            randrange(0,SCREEN), 
            wheel(randrange(colorWheelLowerBound,colorWheelUpperBound)), 
            radius, 
            transformation)
        )

    handleAudio(
        verticalSides, 
        3,
        drawFireWithPeak, 
        circles=circles, 
        colorWheelLowerBound=colorWheelLowerBound, 
        colorWheelUpperBound=colorWheelUpperBound, 
        backgroundColorWheel=backgroundColorWheel, 
    )

def fireRandom(colorWheelLowerBound=20, colorWheelUpperBound=60, backgroundColorWheel=0):
    global modeChanged
    circles = []
    radius = 5
    for i in range(0,10):
        transformation = Transformations(randrange(-2,2), randrange(-5,-2), 0)
        circles.append(Circle(
            SCREEN_X_BEGIN+(i*5), 
            randrange(0,SCREEN), 
            wheel(randrange(colorWheelLowerBound,colorWheelUpperBound)), 
            radius, 
            transformation)
        )
    
    r1 = randrange(10,39)
    while not modeChanged:
        r2 = randrange(10,39)
        step = 3
        if r1 - r2 > 0:
            step = -3
        for i in range(r1,r2, step):
            drawFireWithPeak(i, circles,
                colorWheelLowerBound=colorWheelLowerBound, 
                colorWheelUpperBound=colorWheelUpperBound, 
                backgroundColorWheel=backgroundColorWheel
            )
        r1 = r2
    modeChanged = False

def expandingCircles(borderWidth = 0):
    global modeChanged
    circles = []
    expandLength = [randrange(20,30),randrange(20,30),randrange(40,60),randrange(60,100),randrange(60,90)]
    frame = 0
    background = BLANK
    for i in range(0,5):
        circles.append(Circle(randrange(0,SCREEN), randrange(0,SCREEN), randomColor(), 1, None))

    while not modeChanged:
        drawShapes(circles, borderWidth, background)
        #frame = (frame+1) % 2
        if frame == 1:
            background = BLANK
        else:
            background = BLANK

        # Perform Transform & check for offscreens
        for j in range(0, len(circles)):
            #squares[j].color = complementaryColor(squares[j].color)
            circles[j].alterSize(1)
            expandLength[j] = expandLength[j] - 1
            if expandLength[j] < 0:
                circles[j] = Circle(randrange(SCREEN_X_BEGIN, SCREEN_X_END), randrange(0,SCREEN), randomColor(), 1, None)
                expandLength[j] = randrange(20,90)

        # Draw to screen and wait
        strips.show()
    modeChanged = False

def audioCircle(peak):
    blankStrip()
    circle = Circle(50, 50, RED, peak, None)
    drawShapes([circle], 0, BLANK)
    strips.show()

def solidColorDimmer(peak, denominator=39.0):
    fraction = peak / denominator
    if fraction < 0.25:
        fraction = 0.25
    blankStrip(dimColor(RED, fraction))
    strips.show()

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

def shiftColorSequenceOverNonagonGroups(groups, sequence, hangFrames, fadeFrames, soundFrames=[], soundThreshold=0, backgroundColor=BLANK):
    animation = []
    for i in range(0, len(sequence)):
        animation.append({
            'groups': groups,
            'colors': shiftRight(sequence, i)
            })
    animateNonagonGroups(animation, hangFrames, fadeFrames, soundFrames, soundThreshold, backgroundColor)

def shiftColorSequenceOverSetOfNonagonGroups(setOfGroups, sequence, hangFrames, fadeFrames, soundFrames=[], soundThreshold=0, backgroundColor=BLANK):
    animation = []
    for groupList in setOfGroups:
        for i in range(0, len(sequence)):
            animation.append({
                'groups': groupList,
                'colors': shiftRight(sequence, i)
                })
    animateNonagonGroups(animation, hangFrames, fadeFrames, soundFrames, soundThreshold, backgroundColor)

def traceSidesAnimation(nonagonGroups, sequence, direction, hangFrames, fadeFrames, soundFrames=[], soundThreshold=0, backgroundColor = BLANK):
    animation = []
    for g, group in enumerate(nonagonGroups):

        for s in range(0, 5):
            sides = [[]]
            for n in group:
                sides[0] = sides[0] + sidesFromDirection(n, s, direction, False)
            animation.append({
                'sides': sides,
                'colors': [sequence[g]]})     
    animateSideGroups(animation, hangFrames, fadeFrames, backgroundColor)

def fillSidesAnimation(nonagonGroups, seqeuence, fillSide, drainSide, width, hangFrames, fadeFrames, soundFrames=[], soundThreshold=0, backgroundColor = BLANK):
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

    animateSideGroups(animation, hangFrames, fadeFrames, backgroundColor)

###
# Modes
###    
def cycleThroughColorSequenceWithNonagonTriangles(sequence, hangFrames, fadeFrames):
    shiftColorSequenceOverNonagonGroups(triangles, sequence, hangFrames, fadeFrames)

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

def singleFrameSolidRandomColor(hangFrames=10, fadeFrames=10, threshold=0):
    animation = [{
        'groups': everyNonagon,
        'colors': [randomColor()]
    }]
    animateNonagonGroups(animation, hangFrames, fadeFrames, [0], threshold)

def singleFrameTrianglesRandomColor(hangFrames=10, fadeFrames=10, threshold=0):
    animation = [{
        'groups': triangles,
        'colors': [randomColor(), randomColor()]
    }]
    animateNonagonGroups(animation, hangFrames, fadeFrames, [0], threshold)
