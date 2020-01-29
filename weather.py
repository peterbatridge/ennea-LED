import requests
import json
import credentials
currentWeather = None
# https://openweathermap.org/weather-conditions
current_weather_base = "http://api.openweathermap.org/data/2.5/weather?q=Chicago,us&APPID="
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


#currentWeather = getCurrentWeather()
#schedule.every(10).seconds.do(run_threaded, getTrains)
#schedule.every(30).minutes.do(run_threaded, getCurrentWeather)
# getModeFromWeather(currentWeather[0], currentWeather[1])