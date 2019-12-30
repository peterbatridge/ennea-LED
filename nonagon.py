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
# import board
# import adafruit_dotstar as dotstar

# Using hardware SPI. 436 = 12*31 leds + 2*32 leds
# strips = dotstar.DotStar(board.SCK, board.MOSI, 436, brightness=0.2)

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

currentWeather = getCurrentWeather()
schedule.every(10).seconds.do(run_threaded, getTrains)
schedule.every(10).minutes.do(run_threaded, getCurrentWeather)
# getModeFromWeather(currentWeather[0], currentWeather[1])

try:
    while True:
        schedule.run_pending()

except KeyboardInterrupt:
    print("Exiting due to keyboard interrupt.")
except Exception as e:
    print("Error:", e)