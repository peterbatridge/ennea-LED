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
import shared
import pyaudio
import audioop
import threading
from enum import Enum
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25


form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1  # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 1024 # 212 samples for buffer
dev_index = 2 # device index found by p.get_device_info_by_index(ii)

audio = pyaudio.PyAudio() # create pyaudio instantiation
lastVolumeData = []
volumeDataLock = threading.Lock()

def updateUSBAudio(in_data, frame_count, time_info, status):
    global lastVolumeData, volumeDataLock
    if volumeDataLock.acquire(False):
        try:
            lastVolumeData = in_data
        finally:
            volumeDataLock.release()
    return (in_data, pyaudio.paContinue)

# create pyaudio stream
stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                       input_device_index = dev_index, input = True, \
                       frames_per_buffer=chunk, stream_callback=updateUSBAudio)
    
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Using hardware SPI. 436 = 12*31 leds + 2*32 leds
num_pixels = 434
strips = dotstar.DotStar(board.SCLK, board.MOSI, num_pixels, brightness=0.2, baudrate=4000000, auto_write=False)

lastFrameNonagonColors = []
lastFrameSideColors = []
lastFramePeak = 0
lastRandomColor = BLANK
wheelIterator = 0
volumeData = []
lastVolumeData = []
counter = 0
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

def randomColor(avoidColor=None):
    rand = randrange(9)
    if avoidColor == colors[rand]:
        return colors[(rand+2)%9]
    return colors[rand]

def nextInWheel(step = 1):
    global wheelIterator
    wheelIterator = (wheelIterator + step) % 768
    return wheelIterator

def wheelComplementaryColor(color):
    return (color + 384) % 768

def dimColor(color, fraction):
    if fraction > 1:
        fraction = 1
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
    return [r,g,b]

def remap_range(value, remap):
    #global volumeData

    #volumeData.append(value)
    #if len(volumeData) >= 40:
    #    volumeData.pop(0)
    #    volumeSorted = sorted(volumeData)
       #print(value, volumeSorted[25], volumeSorted[50], volumeSorted[90])
    #    highest = remap[len(remap)-1][1]
    #    if value < volumeSorted[35]:
    #        return int((value / volumeSorted[35]) * highest)
    #    else:
    #        return highest
    
    for m, maxes in enumerate(remap):
        if value <= maxes[0]:
            if m >0:
                return int((value / (maxes[0])*(maxes[1]-remap[m-1][1]))+remap[m-1][1])
            else:
                return int((value / maxes[0])* maxes[1])

def waitUntilSoundReachesThreshold(threshold):
    global lastVolumeData
    audioRMS = 0
    while (audioRMS<threshold) and not shared.modeChanged:
        audioRMS = audioop.rms(lastVolumeData, 2)
    shared.modeChanged = False

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

class AudioType(Enum):
    PEAK_TO_PEAK = 1
    RMS = 2
    FFT = 3
    FFT_SUM = 4

def audioPP(mode, fData):
    return min(audioop.maxpp(fData, 2), 100)
        
def audioRMS(mode, fData):
    return min(audioop.rms(fData, 2), 100)
        
def audioFFT(mode, fData):
    window = np.hanning(len(fData)).astype(np.float32)
    data = fData * window
    fft = np.fft.rfft(data)
    fft = np.delete(fft, len(fft)-1)
    power = np.log10(np.abs(fft)) ** 2
    power = np.reshape(power, (32, 16))
    matrix = np.int_(np.average(power, axis =1))
    matrix = matrix[0:14]
    noise = [8,6,6,5,4,3,3,3,3,3,3,3,3,3]
    reducedNoise = np.subtract(matrix, noise)
    for i in range(0,14):
        if reducedNoise[i] < 0:
            reducedNoise[i] = 0
    #print(reducedNoise, np.sum(reducedNoise))
    if mode == AudioType.FFT_SUM:
        ret = np.sum(reducedNoise)
        #print(ret)
        return ret #min(np.sum(reducedNoise), 100)                
    new_fft = [0.] * 14
    for i, bucket in enumerate(reducedNoise):
        new_fft[i] = remap_range(bucket, [[10, 28], [100, 31]])
    return new_fft

switch = {
    AudioType.PEAK_TO_PEAK: audioPP,
    AudioType.RMS: audioRMS,
    AudioType.FFT: audioFFT,
    AudioType.FFT_SUM: audioFFT
}


def audio(remap, rateOfPeakDescent, functionCalledWithData, maxFrames = 0, mode = AudioType.FFT_SUM, **kwargs):
    global lastVolumeData, volumeDataLock
    totalFrames = 0
    peak = 0
    while not shared.modeChanged and (maxFrames == 0 or maxFrames > totalFrames):
        latest = 0
        if volumeDataLock.acquire(False):
            try:
                fData = np.frombuffer(lastVolumeData, np.int16)    
            finally:
                volumeDataLock.release()
        else:
            continue
        data = switch[mode](mode, fData)
        #print(data)
        if mode != AudioType.FFT:
            mapped_data = remap_range(data, remap)
            if peak > rateOfPeakDescent:
                peak = peak - rateOfPeakDescent
            elif peak > 0:
                peak = peak - 1

            if mapped_data > peak:
                peak = mapped_data
        else:
            peak = data
        functionCalledWithData(peak, **kwargs)
        totalFrames = totalFrames + 1
    shared.modeChanged = False

###
# Pattern Functions
###
def offMode(wait = 1):
    blankStrip()
    time.sleep(wait)

def rainbowCycle(wait = 0):
    for j in range(768):
        for i in range(num_pixels):
            rc_index = (i * 768 // num_pixels) + j
            strips[i] = wheel(rc_index % 768)
        strips.show()
        time.sleep(wait) 
def bounce(foregroundColor = RED, backgroundColor = BLANK):
    pattern = [BLANK] * 31
    for frame in range(0,60):
        for i in range(num_pixels//14):
            if frame > 30:
                frame = 29 - (frame % 31)
            if frame == i: # or frame+15 == i or frame-15==i:
                pattern[i] = foregroundColor
                #strips[(i+31)%61] = PURPLE
                #strips[(i+62)%93] = PURPLE
            else:
                pattern[i] = backgroundColor           
                #strips[i+31] = BLUE
                #strips[i+62] = BLUE
        setPatternOnEveryNonagon(pattern)
        strips.show()

def solidRandomColors(wait = 0.2):
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

def solidColorCycle(wait = 0.2):
    for n in range(0,14):
        setNonagonColor(n, colors[n%9])
        strips.show() 
        time.sleep(wait)

def solidRandomColorEveryOther(wait = 1):
    for i in range(0,2):
        blankStrip()
        for q in range(0,14, 2):
            strips[(q+i)*31:(q+i+1)*31] = [randomColor()]*31
        strips.show()
        time.sleep(wait)

def fiveSolidRandomColors(wait = 1):
    blankStrip()
    for i in range(0,5):
        x = randrange(0,14)
        setNonagonColor(x, randomColor())
    strips.show()
    time.sleep(wait)

def individualPinwheels(wait = 0):
    if wait > 0.1:
        wait = 0.1
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

class Animation:
    def __init__(self, frames = None, soundFrames = None, hangFrames = None, fadeFrames = None, soundThreshold = None, backgroundColor = None):
        self.frames = [] if frames is None else frames
        self.hangFrames = 1 if hangFrames is None else hangFrames
        self.fadeFrames = 0 if fadeFrames is None else fadeFrames
        self.soundFrames = [] if soundFrames is None else soundFrames
        self.soundThreshold = 0 if soundThreshold is None else soundThreshold
        self.backgroundColor = BLANK if backgroundColor is None else backgroundColor

def stepBetweenColors(startColor, endColor, stepCount, currentStep):
    r = ((endColor[0]-startColor[0]) * currentStep /stepCount)+startColor[0]
    g = ((endColor[1]-startColor[1]) * currentStep /stepCount)+startColor[1]
    b = ((endColor[2]-startColor[2]) * currentStep /stepCount)+startColor[2]
    return (int(r),int(g),int(b))

def getLastFrameColors(animationFrames):
    global lastFrameNonagonColors
    if lastFrameNonagonColors!=[]:
        return lastFrameNonagonColors
    lastFrameColors = [BLANK]*14
    frame = animationFrames[len(animationFrames)-1]
    for g, group in enumerate(frame['groups']):
        for nonagon in group:
            lastFrameColors[nonagon] = frame['colors'][g]
    return lastFrameColors

def getLastFrameSideColors(animationFrames):
    global lastFrameSideColors
    if lastFrameSideColors!=[]:
        return lastFrameSideColors
    lastFrameColors = [[BLANK]*9 for i in range(14)]
    frame = animationFrames[len(animationFrames)-1]
    for g, group in enumerate(frame['sides']):
        for side in group:
            lastFrameColors[side[0]][side[1]] = frame['colors'][g]
    return lastFrameColors

def animateNonagonGroups(animation):
    global lastFrameNonagonColors
    lastFrameColors = getLastFrameColors(animation.frames)
    for n, frame in enumerate(animation.frames):
        for f in range(animation.hangFrames+animation.fadeFrames):
            blankStrip(animation.backgroundColor)
            if animation.soundThreshold > 0 and n in animation.soundFrames and f >= animation.fadeFrames:
                for g, group in enumerate(frame['groups']):
                    color = frame['colors'][g]
                    for nonagon in group:
                        lastFrameColors[nonagon] = color
                        setNonagonColor(nonagon, color)
                waitUntilSoundReachesThreshold(animation.soundThreshold)
            else:
                for g, group in enumerate(frame['groups']):
                    color = frame['colors'][g]
                    for nonagon in group:
                        if f < animation.fadeFrames:
                            startColor = lastFrameColors[nonagon]
                            stepColor = stepBetweenColors(startColor, color, animation.fadeFrames, f)
                            setNonagonColor(nonagon, stepColor)
                        else:
                            lastFrameColors[nonagon] = color
                            setNonagonColor(nonagon, color)
                strips.show()
    lastFrameNonagonColors = lastFrameColors

def animateSideGroups(animation):
    global lastFrameSideColors
    lastFrameColors = getLastFrameSideColors(animation.frames)
    for n, frame in enumerate(animation.frames):
        for f in range(animation.hangFrames+animation.fadeFrames):
            blankStrip(animation.backgroundColor)
            for g, group in enumerate(frame['sides']):
                color = frame['colors'][g]
                for side in group:
                    if f < animation.fadeFrames:
                        startColor = lastFrameColors[side[0]][side[1]]
                        stepColor = stepBetweenColors(startColor, color, animation.fadeFrames, f)
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

def gifAnimation(name):
    global gifs
    animation = gifs[name]['frames']
    for n, s in enumerate(animation):
        strip = list(map(applyScaleAndGetColor, s))
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

def expandingRectangle():
    global lastRandomColor
    newColor = randomColor(lastRandomColor)
    sq = Rectangle(50, 50, newColor, 1, 1, Transformations(0,0,1,1))
    background = lastRandomColor
    for i in range(0, 100):
        drawShapes([sq], 0, background)
        strips.show()
        sq.transformations = Transformations(0,0,1,1)
        sq.transform()
    lastRandomColor = newColor

def drawSparkleWithPeak(peak, fadeFrames, color, backgroundColor, allNonagons):
    baseColor = nextInWheel(3)
    if color != BLANK:
        baseColor = color
    if peak >= 28:
        peak = 28
    if peak < 3:
        peak = 3
    onNum = peak
    for n in range(0,14):
        mask = [backgroundColor] * 31
        increment = n*50
        if allNonagons == 1:
            increment = 0
        if color != BLANK:
            mask[0:onNum] = [color] * onNum
        else:
            mask[0:onNum] = [wheel((baseColor+increment)%768)] * onNum
        shuffle(mask)
        for i in range(0, fadeFrames):        
            for p in range(0,31):
                strips[n*31+p] = stepBetweenColors(strips[n*31+p], mask[p], fadeFrames, i)
    strips.show()

def sparkleAudio(maxFrames = 0, color = BLANK, backgroundColor = BLANK, allNonagons = 0, fadeFrames=2):
    audio(usbSparkle, 3, drawSparkleWithPeak, maxFrames, AudioType.RMS, fadeFrames=fadeFrames, color = color, backgroundColor = backgroundColor, allNonagons = allNonagons)

def oppositeRains(topColor = MAGENTA, bottomColor = MAGENTA, backgroundColor = BLANK):
    upTransform = Transformations(0,-2,0)
    downTransform = Transformations(0,2,0)
    circles = [Circle(42, 100, bottomColor, 7, upTransform), Circle(70, 100, bottomColor, 7, upTransform), 
            Circle(29, 0 , topColor, 7, downTransform), Circle(56, 0, topColor, 7 , downTransform)]
    for i in range(0, 100):
        drawShapes(circles, 0, backgroundColor)
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
   
def drawRainingSquares(maxFrames = 0, colorWheelLowerBound = 256, colorWheelUpperBound = 512):
    squares = []
    for i in range(0,10):
        transformation = Transformations(0, randrange(3,5), 0)
        squares.append(Circle(i*10,randrange(0,SCREEN), wheel(randrange(colorWheelLowerBound,colorWheelUpperBound)), 10, transformation))
    totalFrames = 0
    while not shared.modeChanged and (maxFrames == 0 or maxFrames > totalFrames):
        drawShapes(squares, 0, BLANK)

        # Perform Transform & check for offscreens
        for j in range(0, len(squares)):
            squares[j].transform()
            if squares[j].isOffscreen(SCREEN, SCREEN):
                squares[j].y = 0
                squares[j].color = wheel(randrange(colorWheelLowerBound,colorWheelUpperBound))
                squares[j].transformations = Transformations(0, randrange(3,5), 0)
        strips.show()
        totalFrames = totalFrames + 1
    shared.modeChanged = False

def pinwheelAudio(maxFrames = 0, color = BLANK, backgroundColor = BLANK):
    rect = Rectangle(50, 50, color, 10, 100, None)
    audio([[10, 35],[60, 80],[100000,81]], 1, drawPinwheelWithPeak, maxFrames, AudioType.FFT_SUM, rect=rect, color=color, backgroundColor=backgroundColor)

def drawPinwheelWithPeak(peak, rect, color, backgroundColor):
    rect.rotate(-peak)
    if color == BLANK and backgroundColor == BLANK:
        wheelPos = nextInWheel()
        color = wheel(wheelPos)
        backgroundColor = wheel(wheelComplementaryColor(wheelPos))
    rect.color = color
    drawShapes([rect], 0, backgroundColor)
    strips.show()

def drawFireWithPeak(peak, circles, colorWheelLowerBound=20, colorWheelUpperBound=60, backgroundColorWheel=0):
    if peak < 6:
        peak = 5
    drawShapes(circles, 0, wheel(backgroundColorWheel), peak/100.0)
    strips.show()
    for i in range(0, len(circles)):
        circles[i].transform()
        if circles[i].isOffscreen(SCREEN, SCREEN):
            circles[i].x = 25+(i*5)
            circles[i].y = SCREEN
            circles[i].color = wheel(randrange(colorWheelLowerBound,colorWheelUpperBound))
            circles[i].transformations = Transformations(randrange(-2,2), randrange(-5,-2), 0)

def fireAudio(maxFrames = 0, colorWheelLowerBound=20, colorWheelUpperBound=60, backgroundColorWheel=0):
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

    audio(
        [[4, 20],[60, 99],[100000,100]], 
        5,
        drawFireWithPeak,
        maxFrames,
        AudioType.FFT_SUM,
        circles=circles, 
        colorWheelLowerBound=colorWheelLowerBound, 
        colorWheelUpperBound=colorWheelUpperBound, 
        backgroundColorWheel=backgroundColorWheel, 
    )

def fireRandom(maxFrames = 0, colorWheelLowerBound=20, colorWheelUpperBound=60, backgroundColorWheel=0):
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
    totalFrames = 0
    while not shared.modeChanged and (maxFrames == 0 or maxFrames > totalFrames):
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
        totalFrames = totalFrames + 1
    shared.modeChanged = False

def expandingCircles(maxFrames = 0, borderWidth = 0):
    circles = []
    expandLength = [randrange(20,30),randrange(20,30),randrange(40,60),randrange(60,100),randrange(60,90)]
    background = BLANK
    for i in range(0,5):
        circles.append(Circle(randrange(0,SCREEN), randrange(0,SCREEN), randomColor(), 1, None))

    totalFrames = 0
    while not shared.modeChanged and (maxFrames == 0 or maxFrames > totalFrames):
        drawShapes(circles, borderWidth, background)

        # Perform Transform & check for offscreens
        for j in range(0, len(circles)):
            circles[j].alterSize(1)
            expandLength[j] = expandLength[j] - 1
            if expandLength[j] < 0:
                circles[j] = Circle(randrange(SCREEN_X_BEGIN, SCREEN_X_END), randrange(0,SCREEN), randomColor(), 1, None)
                expandLength[j] = randrange(20,90)

        # Draw to screen and wait
        strips.show()
        totalFrames = totalFrames + 1
    shared.modeChanged = False

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

def randomColorForSolidColorAudio(avoidColor = None):
    colorSet = [RED, ORANGE, GREEN, CYAN, BLUE, PURPLE]
    rand = randrange(6)
    if avoidColor == colors[rand]:
        return colors[(rand+2)%6]
    return colorSet[rand]


def boundlessColorDimmer(peak, denominator, threshold):
    global lastRandomColor, lastFramePeak, counter
    fraction = peak / denominator
    if fraction <= 0.025:
        fraction = 0.025
        
    if peak > threshold:
        if counter == 0:
            lastRandomColor = randomColorForSolidColorAudio(lastRandomColor)
            counter = 15
    if counter > 0:
        counter = counter - 1
    color = dimColor(lastRandomColor, fraction)
    startColor = dimColor(lastRandomColor, (lastFramePeak / denominator))
    if fraction > 0.025:
        blankStrip(stepBetweenColors(startColor, color, 1, 0))
        lastFramePeak = peak
        strips.show()
    #blankStrip(stepBetweenColors(startColor, color, 4, 2))
    #strips.show()
    #blankStrip(stepBetweenColors(startColor, color, 4, 3))
    #strips.show()

    blankStrip(color)
    strips.show()

def solidColorAudioMode(threshold = 75, maxFrames = 0): 
    global lastRandomColor
    mapping = [[4, 10],[50, 99],[100000,100]] 
    lastRandomColor = randomColorForSolidColorAudio(lastRandomColor)
    audio(
        mapping, 
        2,
        boundlessColorDimmer,
        maxFrames, 
        AudioType.FFT_SUM,
        denominator = 100.0,
        threshold = threshold
    )   

###
# Animation Generators
###

def colorSwapAnimation(groups, colorOne, colorTwo, colorBetween, hangFrames, fadeFrames):
    lengthOfGroup = len(groups)
    animation = Animation(hangFrames = hangFrames, fadeFrames = fadeFrames)
    for i in range(1, int(lengthOfGroup/2)+1):
        colorList = [colorOne]*i +[colorBetween]*(lengthOfGroup-(2*i)) + [colorTwo]*i
        animation.frames.append({
            'groups': groups,
            'colors': colorList
        })
    for i in range(int(lengthOfGroup/2), -1, -1):
        colorList =  [colorTwo]*i+[colorBetween]*(lengthOfGroup-(2*i)) + [colorOne]*i
        animation.frames.append({
            'groups': groups,
            'colors': colorList
        })
    animateNonagonGroups(animation)

def shiftColorSequenceOverNonagonGroups(groups, sequence, hangFrames, fadeFrames, soundFrames=[], soundThreshold=0, backgroundColor=BLANK):
    animation = Animation(hangFrames = hangFrames, fadeFrames = fadeFrames, soundFrames = soundFrames, soundThreshold = soundThreshold, backgroundColor = backgroundColor)
    for i in range(0, len(sequence)):
        animation.frames.append({
            'groups': groups,
            'colors': shiftRight(sequence, i)
            })
    animateNonagonGroups(animation)

def shiftColorSequenceOverSetOfNonagonGroups(setOfGroups, sequence, hangFrames, fadeFrames, soundFrames=[], soundThreshold=0, backgroundColor=BLANK):
    animation = Animation(hangFrames = hangFrames, fadeFrames = fadeFrames, soundFrames = soundFrames, soundThreshold = soundThreshold, backgroundColor = backgroundColor)
    for groupList in setOfGroups:
        for i in range(0, len(sequence)):
            animation.frames.append({
                'groups': groupList,
                'colors': shiftRight(sequence, i)
                })
    animateNonagonGroups(animation)

def traceSidesAnimation(nonagonGroups, sequence, direction, hangFrames, fadeFrames, soundFrames=[], soundThreshold=0, backgroundColor = BLANK):
    animation = Animation(hangFrames = hangFrames, fadeFrames = fadeFrames, soundFrames = soundFrames, soundThreshold = soundThreshold, backgroundColor = backgroundColor)
    for g, group in enumerate(nonagonGroups):
        for s in range(0, 5):
            sides = [[]]
            for n in group:
                sides[0] = sides[0] + sidesFromDirection(n, s, direction, False)
            animation.frames.append({
                'sides': sides,
                'colors': [sequence[g]]})     
    animateSideGroups(animation)

def fillSidesAnimation(nonagonGroups, seqeuence, fillSide, drainSide, width, hangFrames, fadeFrames, soundFrames=[], soundThreshold=0, backgroundColor = BLANK):
    if width<5:
        width = 5
    numBuckets = len(nonagonGroups)
    buckets = [-1]*numBuckets
    filled = 0
    startIter = 0
    endIter = 1
    animation = Animation(hangFrames = hangFrames, fadeFrames = fadeFrames, soundFrames = soundFrames, soundThreshold = soundThreshold, backgroundColor = backgroundColor)
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

        animation.frames.append({
        'sides': sides,
        'colors': colors
        })
    animateSideGroups(animation)

###
# Modes
###    
def cycleThroughColorSequenceWithNonagonTriangles(sequence, hangFrames, fadeFrames):
    shiftColorSequenceOverNonagonGroups(triangles, sequence, hangFrames, fadeFrames)
    
def exMachinaMode(threshold=50):
    shiftColorSequenceOverNonagonGroups(everyNonagon, coldFour, 15, 10, [0,1,2,3], threshold)
    shiftColorSequenceOverNonagonGroups(everyNonagon, coldFour, 15, 10, [0,1,2,3], threshold)
    shiftColorSequenceOverNonagonGroups(topLeftToBottomRightSharpDiagonal, coldToWarmSixteen, 1, 5)
    shiftColorSequenceOverNonagonGroups(topLeftToBottomRightSharpDiagonal, coldToWarmSixteen, 1, 5)
    fillSidesAnimation(topLeftToBottomRightDiagonal, [RED]*len(topLeftToBottomRightDiagonal), 'top', 'bot', 10, 1, 1)
    fillSidesAnimation(topLeftToBottomRightSharpDiagonal, [RED]*len(topLeftToBottomRightDiagonal), 'top', 'bot', 10, 1, 1)
    fillSidesAnimation(topLeftToBottomRightDiagonal, [RED]*len(topLeftToBottomRightDiagonal), 'top', 'bot', 10, 1, 1)
    fillSidesAnimation(topLeftToBottomRightSharpDiagonal, [RED]*len(topLeftToBottomRightDiagonal), 'top', 'bot', 10, 1, 1)

def singleFrameSolidRandomColor(hangFrames=10, fadeFrames=10, threshold=0):
    global lastRandomColor
    uniqueRandomColor = randomColor(lastRandomColor)
    lastRandomColor = uniqueRandomColor
    animation = Animation(hangFrames = hangFrames, fadeFrames = fadeFrames, soundFrames = [0], soundThreshold = threshold)
    animation.frames = [{
        'groups': everyNonagon,
        'colors': [uniqueRandomColor]
    }]
    animateNonagonGroups(animation)

def singleFrameTrianglesRandomColor(hangFrames=10, fadeFrames=10, threshold=0):
    global lastRandomColor
    uniqueRandomColorOne = randomColor(lastRandomColor)
    uniqueRandomColorTwo = randomColor(uniqueRandomColorOne)
    lastRandomColor = uniqueRandomColorTwo
    animation = Animation(hangFrames = hangFrames, fadeFrames = fadeFrames, soundFrames = [0], soundThreshold = threshold)
    animation.frames = [{
        'groups': triangles,
        'colors': [uniqueRandomColorOne, uniqueRandomColorTwo]
    }]
    animateNonagonGroups(animation)

def randomMode(audioModes = True):
    print(math.rand(0,30))
