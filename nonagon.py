import time
import random
import requests
import json
import credentials
# import board
# import adafruit_dotstar as dotstar

# Using a DotStar Digital LED Strip with 30 LEDs connected to hardware SPI
#dots = dotstar.DotStar(board.SCK, board.MOSI, 144, brightness=0.2)

# Using a DotStar Digital LED Strip with 30 LEDs connected to digital pins
#dots = dotstar.DotStar(board.D3, board.D2, 144, brightness=0.2)

# https://openweathermap.org/weather-conditions

current_weather_base = "http://api.openweathermap.org/data/2.5/weather?q=Chicago,us&APPID="

cta_train_line_base = "http://lapi.transitchicago.com/api/1.0/ttpositions.aspx?rt=brn&outputType=JSON&key="


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
    responseRaw = requests.get(current_weather_base+credentials.owm_api_key)
    response = json.loads(responseRaw.content)
    weatherCode = response['weather'][0]['id']
    temp = response['main']['temp']
    return weatherCode, temp
    
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

#Train Timings
#29:20 at chicago -> 29:59 probably audible -> 30:20 probably fading -> 31:25 stopped at merch Mart  => About a minute and a half before arrival at merch mart
#43:20 at merch mart -> 43:30 stopped -> 44: 00 leaving -> 45:00 probably audible -> 45:20 right nextdoor -> 45:40 at Chicago => About 40 seconds until arrival at merch mart
def getTrain():
    data = ''''''
    responseRaw = requests.post(cta_train_line_base + credentials.cta_api_key, data=data)
    response = json.loads(responseRaw.content)
    print(response)
    for train in response['ctatt']['route'][0]['train']:
        #trDr = 1 for northbound and 5 for southbound
        if (train['trDr'] == '5' and train['nextStaNm']=="Merchandise Mart"):
            print("On the way to merch mart!")
            #time_to_arrival_at_merchmart = train['arrT'] - train['prdt'] 
        if (train['trDr'] == '1' and train['nextStaNm']=="Chicago"):
            print("On the way to Chicago!")

# n_dots = len(dots)
# i = 0
# while True:
#     dots.fill(wheel(i))
#     i = (i+20) % 384

# currentWeather = getCurrentWeather()
# getModeFromWeather(currentWeather[0], currentWeather[1])
while True:
    getTrain()
    time.sleep(10)