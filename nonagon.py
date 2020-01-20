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

# n_dots = len(dots)
# i = 0
# while True:
#     dots.fill(wheel(i))
#     i = (i+20) % 384

def run_threaded(func):
    threading.Thread(target=func).start()

#currentWeather = getCurrentWeather()
#schedule.every(10).seconds.do(run_threaded, getTrains)
#schedule.every(10).minutes.do(run_threaded, getCurrentWeather)
# getModeFromWeather(currentWeather[0], currentWeather[1])

def color_fill(color, wait):
    strips.fill(color)
    strips.show()
    time.sleep(wait)
 
def blankStrip():
    strips[0:434] = [BLANK]*434
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
 
 
def rainbow_cycle(wait):
    for j in range(384):
        for i in range(num_pixels):
            rc_index = (i * 384 // num_pixels) + j
            strips[i] = wheel(rc_index % 384)
        strips.show()
        #time.sleep(wait) 
def bounce():
    for frame in range(0,60):
        for i in range(num_pixels//3):
            if frame > 30:
                frame = 29 - (frame % 31)
            if frame == i: # or frame+15 == i or frame-15==i:
                strips[i] = RED
                #strips[(i+31)%61] = PURPLE
                #strips[(i+62)%93] = PURPLE
            else:
                strips[i] = BLUE           
                #strips[i+31] = BLUE
                #strips[i+62] = BLUE
        strips[31:62] = strips[0:31]
        strips[62:93] = strips[0:31]
        strips[93:124] = strips[0:31]
        strips[124:155]= strips[0:31]
        strips[155:186] = strips[0:31]
        strips[186:217] = strips[0:31]
        strips[217:248] = strips[0:31]
        strips[248:279] = strips[0:31]
        strips[279:310] = strips[0:31]
        strips[310:341] = strips[0:31]
        strips[341:372] = strips[0:31]
        strips[372:403] = strips[0:31]
        strips[403:434] = strips[0:31]
        strips.show()


def random_color():
    return colors[randrange(9)]
def random_solid_colors():
        strips[0:31] = [random_color()]*31
        strips[31:62] = [random_color()]*31
        strips[62:93] =  [random_color()]*31

        strips[93:124] =  [random_color()]*31
        strips[124:155]=  [random_color()]*31

        strips[155:186] = [random_color()]*31

        strips[186:217] = [random_color()]*31

        strips[217:248] = [random_color()]*31

        strips[248:279] = [random_color()]*31

        strips[279:310] = [random_color()]*31

        strips[310:341] = [random_color()]*31

        strips[341:372] = [random_color()]*31

        strips[372:403] = [random_color()]*31

        strips[403:434] = [random_color()]*31

        strips.show() 
        time.sleep(0.2)
def solid_color_cycle():
    for i in range(0,14):
        strips[0:31]    = [colors[i % 9]]*31
        strips[31:62]   = [colors[(i+1)%9]]*31
        strips[62:93]  =  [colors[(i+2)%9]]*31
        strips[93:124] =  [colors[(i+3)%9]]*31
        strips[124:155] = [colors[(i+4)%9]]*31
        strips[155:186] = [colors[(i+5)%9]]*31
        strips[186:217] = [colors[(i+6)%9]]*31
        strips[217:248] = [colors[(i+7)%9]]*31
        strips[248:279] = [colors[(i+8)%9]]*31
        strips[279:310] = [colors[(i)%9]]*31
        strips[310:341] = [colors[(i+1)%9]]*31
        strips[341:372] = [colors[(i+2)%9]]*31
        strips[372:403] = [colors[(i+3)%9]]*31
        strips[403:434] = [colors[(i+4)%9]]*31

        strips.show() 
        time.sleep(0.2)
def solid_color_every_other():
    for i in range(0,2):
        strips[0:434] =[(0,0,0)]*434
        for q in range(0,14, 2):
            strips[(q+i)*31:(q+i+1)*31] = [random_color()]*31
        strips.show()
        time.sleep(1)

def five_random_solid_colors():
    strips[0:434] = [(0,0,0)] *434
    for i in range(0,5):
        x = randrange(0,14)
        strips[x*31:(x+1)*31] = [random_color()]*31
    strips.show()
    time.sleep(1)
def pinwheel(sleep):
    for i in range(0,434):
        strips[0:434] = [(0,0,0)] * 434
        for q in range(0,62):
            strips[(i+(7*q))%434] = wheel(i)
            strips[(i+(7*q)+1)%434] = wheel(i+15)
            strips[(i+(7*q)+2)%434] = wheel(i+30)
        strips.show()
        time.sleep(sleep)
def trail(length):
    for i in range(0,434):
        strips[0:434] = [(0,0,0)] *434
        for l in range(0, length):
            strips[(i+l)% 434] = wheel((i+l)%434)
        strips.show()

def rain():
    rain_color = RED
    path1 = [(0,0,0)]*434
    for i in range(0,238):
        path1[0:434] = [(0,0,0)] * 434
        path1[i] = rain_color
        path1[(i+1)%238]
        path1[(i+2)%238]
        path1[(i+3)%238]

        strips[0:16]    = path1[0:16]
        strips[31:47]   = path1[18:34]
        strips[62:78]   = path1[36:52]
        strips[93:109]  = path1[54:70]
        strips[124:140] = path1[72:88]
        strips[155:171] = path1[90:106]
        strips[186:202] = path1[108:124]
        #strips[217:]
        strips.show()
def setNonagonColor(n, color):
    strips[n*31:n*31+31] = [color]*31


color_seq = [RED, RED, ORANGE, ORANGE, CYAN, BLUE, MAGENTA, MAGENTA]

color_seq2 = [RED, ORANGE, YELLOW, GREEN, TEAL, CYAN, BLUE, PURPLE, MAGENTA]
horizontalRows = [[0],[1,13],[2,12],[3,11],[4,10],[5,9],[6,8],[7]]
def groupCycleThroughSequence(group, color_seq, wait):
    length = len(color_seq)
    for i in range(0,length):
        for q, row in enumerate(group):
            color = color_seq[(i+q)%length]
            for nonagon in row:
                setNonagonColor(nonagon, color)
        strips.show()
        time.sleep(wait)

def stepBetweenColors(startColor, endColor, stepCount, currentStep):
    r = ((endColor[0]-startColor[0]) * currentStep /stepCount)+startColor[0]
    g = ((endColor[1]-startColor[1]) * currentStep /stepCount)+startColor[1]
    b = ((endColor[2]-startColor[2]) * currentStep /stepCount)+startColor[2]
    return (int(r),int(g),int(b))
def groupCycleThroughSequenceFade(groups, color_seq, hang_frames, fade_frames, wait=0):
    length = len(color_seq)
    for i in range(0, length):
        for f in range(0, hang_frames+fade_frames):
            for q, group in enumerate(groups):
                if f < hang_frames:
                    color = color_seq[(i+q)%length]
                else:
                    fade_frame = f - hang_frames
                    start_color = color_seq[(i+q)%length]     
                    end_color = color_seq[(i+q+1)%length]
                    color = stepBetweenColors(start_color, end_color, fade_frames, fade_frame)
                for nonagon in group:
                    setNonagonColor(nonagon, color)
            strips.show()
            time.sleep(wait)
               
nonagonsWithLightsStartingBottomCenter = [0,2,4,6,8,10,12]
nonagonsWIthLightsStartingBottomLeft = [1,3,5,7,9,11,13]
def fillNonagonSide(n, side, color):
    nonagonStart = n*31
    sideStart = int(math.ceil(side*3.647))
    sideEnd = (sideStart+4)%31
    if sideStart+4 > 31:
        strips[nonagonStart+sideStart] = color
        strips[nonagonStart:nonagonStart+3] = [color] * 3
    else:
        strips[nonagonStart+sideStart:nonagonStart+sideStart+4] = [RED]*4

def setLightOnSide(n, side, pos, color):
    nonagonStart = n*31
    sideStart= int(math.ceil(side*3.647))
    positionWithinNonagon = (sideStart+pos) % 31
    strips[nonagonStart+positionWithinNonagon] = color

redFour = [CYAN,CYAN, BLUE, BLUE]

HtL = [3,2,1,0]
LtH = [0,1,2,3]
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
def sidesWithSequences(sidesWithSequences, hangFrame, wait_between_nonagons=0):
    lastNonagon = -1
    for sequence in sidesWithSequences:
        for i, pos in enumerate(sequence[2]):
            for h in range(0, hangFrame):
                blankStrip()
                setLightOnSide(sequence[0], sequence[1], pos, sequence[3][i])
                if lastNonagon!=sequence[0]:
                    if lastNonagon!=-1:
                        time.sleep(0)
                    lastNonagon=sequence[0]
                strips.show()
columnsRightToLeft = [[3,4],[1,2,5,6],[7,10, 11, 0],[8, 9, 12, 13]]
columnsLeftToRight = [[8,9,12,13],[7,10,11,0],[1,2,5,6],[3,4]]
def columnsCycleThroughSequence(color_seq, wait):
    setCycleThroughSequence(columnsLeftToRight, color_seq, wait)
 
def rowCycleThroughSequence(color_seq, wait):
    setCycleThroughSequence(horizontalRows, color_seq, wait)
def cycleThroughSides():
    for s in range(0,9):
        strips[0:434] = [(0,0,0)] *434
        for n in range(0,14):
            fillNonagonSide(n, s, RED)
        strips.show()
        time.sleep(0.5)




try:        
    i = 0

    while True:
        #path() 
        #pinwheel(0)
        #columnsCycleThroughSequence(color_seq)
        #rowCycleThroughSequence(color_seq, 0.3)
        
        #setCycleThroughSequenceFade(horizontalRows, color_seq, 10, 10, 0) 
        #cycleThroughSides()
        sidesWithSequences(sideList, 2, 0)
        
        #trail(217)
        # Increase or decrease this to speed up or slow down the animation.
        #slice_alternating(0.1)
     
        #rain()
        #color_fill(WHITE, 0.5)
     
        # Increase or decrease this to speed up or slow down the animation.
        #slice_rainbow(0.1)
     
        #time.sleep(0.5)
     
        # Increase this number to slow down the rainbow animation.
       # rainbow_cycle(0)
        #bounce()
        #random_solid_colors()
        #solid_color_cycle()
        #single_snake()
        #solid_color_every_other()
#        rain()

#five_random_solid_colors()
            #schedule.run_pending()
            #rainbow_cycle(i)
except KeyboardInterrupt:
    print("Exiting due to keyboard interrupt.")
    strips.deinit()
#except Exception as e:
#    print("Error:", e)
