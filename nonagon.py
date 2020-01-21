import time
import random
import requests
import json
import credentials
import threading
from datetime import datetime, timedelta
#import schedule
CTA_DATETIME = '%Y-%m-%dT%H:%M:%S'
CTA_LOCK = threading.Semaphore(1)
mm_bound_timer = False
chi_bound_timer = False
currentWeather = None
import board
import adafruit_dotstar as dotstar
from random import randrange
import math
# Using hardware SPI. 436 = 12*31 leds + 2*32 leds
num_pixels = 465
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

def blankStrip():
    strips[0:434] = [BLANK]*434
 
def setNonagonColor(n, color):
    strips[n*31:n*31+31] = [color]*31

def setPatternOnEachNonagon(pattern):
    for n in range(0,14):
        strips[n*31:(n*31)+31] = pattern

def setSide(n, side, color):
    nonagonStart = n*31
    sideStart = int(math.ceil(side*3.647))
    if sideStart+4 > 31:
        strips[nonagonStart+sideStart] = color
        strips[nonagonStart:nonagonStart+3] = [color] * 3
    else:
        strips[nonagonStart+sideStart:nonagonStart+sideStart+4] = [RED]*4

def setPositionOnSide(n, side, pos, color):
    nonagonStart = n*31
    sideStart= int(math.ceil(side*3.647))
    positionWithinNonagon = (sideStart+pos) % 31
    strips[nonagonStart+positionWithinNonagon] = color

def wheel(num):
    r =0
    g =0
    b = 0
    c = int(num/128)
    if c == 0:
        r = 127 - (num%128)
        g = num % 128
        b = 0
    elif c == 1:
        g = 127 - (num%128)
        b = num % 128
        r = 0
    else:
        b = 127 - (num%128)
        r = num % 128
        g = 0
    return (r,g,b)

###
# Pattern Functions
###

def slice_alternating(wait):
    strips[::2] = [RED] * ((num_pixels // 2)+1)
    strips.show()
    time.sleep(wait)
    strips[1::2] = [ORANGE] * (num_pixels // 2)
    strips.show()
    time.sleep(wait)
    strips[::2] = [YELLOW] * ((num_pixels // 2)+1)
    strips.show()
    time.sleep(wait)
    strips[1::2] = [GREEN] * (num_pixels // 2)
    strips.show()
    time.sleep(wait)
    strips[::2] = [TEAL] * ((num_pixels // 2)+1)
    strips.show()
    time.sleep(wait)
    strips[1::2] = [CYAN] * (num_pixels // 2)
    strips.show()
    time.sleep(wait)
    strips[::2] = [BLUE] * ((num_pixels // 2)+1)
    strips.show()
    time.sleep(wait)
    strips[1::2] = [PURPLE] * (num_pixels // 2)
    strips.show()
    time.sleep(wait)
    strips[::2] = [MAGENTA] * ((num_pixels // 2)+1)
    strips.show()
    time.sleep(wait)
    strips[1::2] = [WHITE] * (num_pixels // 2)
    strips.show()
    time.sleep(wait)
 
 
def slice_rainbow(wait):
    strips[::6] = [RED] * 78 
    strips.show()
    time.sleep(wait)
    strips[1::6] = [ORANGE] *78
    strips.show()
    time.sleep(wait)
    strips[2::6] = [YELLOW] * 78
    strips.show()
    time.sleep(wait)
    strips[3::6] = [GREEN] * 77
    strips.show()
    time.sleep(wait)
    strips[4::6] = [BLUE] * 77
    strips.show()
    time.sleep(wait)
    strips[5::6] = [PURPLE] * 77
    strips.show()
    time.sleep(wait)
 
 
def rainbowCycle(wait):
    for j in range(384):
        for i in range(num_pixels):
            rc_index = (i * 384 // num_pixels) + j
            strips[i] = wheel(rc_index % 384)
        strips.show()
        time.sleep(wait) 
def bounce():
    pattern = [BLANK] * 31
    for frame in range(0,60):
        for i in range(num_pixels//3):
            if frame > 30:
                frame = 29 - (frame % 31)
            if frame == i: # or frame+15 == i or frame-15==i:
                pattern[i] = RED
                #strips[(i+31)%61] = PURPLE
                #strips[(i+62)%93] = PURPLE
            else:
                pattern[i] = BLUE           
                #strips[i+31] = BLUE
                #strips[i+62] = BLUE
        setPatternOnEachNonagon(pattern)
        strips.show()


def randomColor():
    return colors[randrange(9)]
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
    
def groupCycleThroughSequenceFade(groups, colorSeq, hang_frames, fade_frames, wait=0):
    length = len(colorSeq)
    for i in range(0, length):
        for f in range(0, hang_frames+fade_frames):
            for q, group in enumerate(groups):
                if f < hang_frames:
                    color = colorSeq[(i+q)%length]
                else:
                    fade_frame = f - hang_frames
                    start_color = colorSeq[(i+q)%length]     
                    end_color = colorSeq[(i+q+1)%length]
                    color = stepBetweenColors(start_color, end_color, fade_frames, fade_frame)
                for nonagon in group:
                    setNonagonColor(nonagon, color)
            strips.show()
            time.sleep(wait)
 
def getNonagonColorFromFrame(frame, n):
    for g, group in enumerate(frame['groups']):
        for nonagon in group:
            if n == nonagon:
                return frame['colors'][g]

def getLastFrameColors(animation):
    lastFrameColors = [0]*14
    frame = animation[len(animation)-1]
    for g, group in enumerate(frame['groups']):
        for nonagon in group:
            lastFrameColors[nonagon] = frame['colors'][g]
    return lastFrameColors
def groupAnimateFade(animation, hang_frames, fade_frames, wait=0):
    lastFrameColors = getLastFrameColors(animation)
    for n, frame in enumerate(animation):
        for f in range(0, hang_frames+fade_frames):
            for g, group in enumerate(frame['groups']):
                color = frame['colors'][g]
                for nonagon in group:
                    if f < fade_frames:
                        endColor = lastFrameColors[nonagon]
                        stepColor = stepBetweenColors(endColor, color, fade_frames, f)
                        setNonagonColor(nonagon, stepColor)
                    else:
                        lastFrameColors[nonagon] = color
                        setNonagonColor(nonagon, color)
            strips.show()
               
def sidesWithSequences(sidesWithSequences, hangFrame, wait_between_nonagons=0):
    lastNonagon = -1
    for sequence in sidesWithSequences:
        for i, pos in enumerate(sequence[2]):
            for h in range(0, hangFrame):
                blankStrip()
                setPositionOnSide(sequence[0], sequence[1], pos, sequence[3][i])
                if lastNonagon!=sequence[0]:
                    if lastNonagon!=-1:
                        time.sleep(0)
                    lastNonagon=sequence[0]
                strips.show()
            
def cycleThroughSides(wait=0.5):
    for s in range(0,9):
        blankStrip()
        for n in range(0,14):
            setSide(n, s, RED)
            strips.show()
            time.sleep(wait)
 
###
#Groups Of Nonagons
###
columnsRightToLeft = [[3,4],[1,2,5,6],[7,10, 11, 0],[8, 9, 12, 13]]
columnsLeftToRight = columnsRightToLeft[::-1]
rowsTopToBottom = [[0],[1,13],[2,12],[3,11],[4,10],[5,9],[6,8],[7]]
rowsBottomToTop = rowsTopToBottom[::-1]
bottomLeftToTopRightDiagonal = [[0,1],[2,3,13],[4,11,12],[5,10],[6,9],[7,8]]
topRightToBottomLeft = bottomLeftToTopRightDiagonal[::-1]
bottomRightToTopLeftDiagonal = [[0,13],[1,12],[2,11],[3,9,10],[4,5,8],[6,7]]
topLeftToBottomRightDiagonal = bottomRightToTopLeftDiagonal[::-1]

###
# Color Sequences
###
redToBlueSeq8 = [RED, RED, ORANGE, ORANGE, CYAN, BLUE, MAGENTA, MAGENTA, GREEN]
colorSeq2 = [RED, ORANGE, YELLOW, GREEN, TEAL, CYAN, BLUE, PURPLE, MAGENTA]
redFour = [CYAN,CYAN, BLUE, BLUE]

###
# Pixel Sequences on Sides
###
HtL = [3,2,1,0]
LtH = [0,1,2,3]

###
# Side Animations
###

def shiftLeft(colors, step):
    if step == 0:
        return colors
    return colors[step:] + colors[:step]

def shiftColorSequenceOverNonagonGroups(groups, sequence):
    animation = []
    for i in range(0, len(sequence)):
        animation.append({
            'groups': groups,
            'colors': shiftLeft(sequence, i)
            })
    groupAnimateFade(animation, 10, 10, 0)

animationFrames = [
        {
            'groups': rowsTopToBottom,
            'colors': redToBlueSeq8
        },
        {
            'groups':rowsTopToBottom,
            'colors': shiftLeft(redToBlueSeq8,1)
        },
        {
            'groups': rowsTopToBottom,
            'colors': shiftLeft(redToBlueSeq8,2)
        },
        {
            'groups':rowsTopToBottom,
            'colors': shiftLeft(redToBlueSeq8,3)
        },
        {
            'groups': rowsTopToBottom,
            'colors': shiftLeft(redToBlueSeq8,4)
        },
        {
            'groups':rowsTopToBottom,
            'colors': shiftLeft(redToBlueSeq8,5)
        },
        {
            'groups': rowsTopToBottom,
            'colors': shiftLeft(redToBlueSeq8,6)
        },
        {
            'groups':rowsTopToBottom,
            'colors': shiftLeft(redToBlueSeq8,7)
        }
        ]

sideList  = [
            (7,4, HtL, redFour),
            (7,3, HtL, redFour),
            (7,2, HtL, redFour),
            (8,7, LtH, redFour),
            (8,8, LtH, redFour),
            (9,5,  LtH, redFour),
            (9,6,  LtH, redFour),
            (10,2, HtL, redFour),
            (10,1, HtL, redFour),
            (11,3, HtL, redFour),
            (11,2, HtL, redFour),
            (12,7, LtH, redFour),
            (12,8, LtH, redFour),
            (13,5, LtH, redFour),
            (13,6, LtH, redFour),
            (0,2, HtL, redFour),
            (0,1, HtL, redFour)
            ]

try:        
    i = 0

    while True:
        #path() 
        #pinwheel(0)
        #columnsCycleThroughSequence(colorSeq)
        #rowCycleThroughSequence(colorSeq, 0.3)
        
        #groupAnimateFade(animationFrames, 10, 10, 0)
        shiftColorSequenceOverNonagonGroups(rowsTopToBottom, redToBlueSeq8)
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
       # rainbowCycle
       #(0)
        #bounce()
        #s
        #()
        #solidColorCycle
        #()
        #single_snake()
        #solidRandomColorEveryOther()
#        rain()

#five_random_solid_colors()
            #schedule.run_pending()
            #rainbowCycle
            #(i)
except KeyboardInterrupt:
    print("Exiting due to keyboard interrupt.")
    strips.deinit()
#except Exception as e:
#    print("Error:", e)
