  
import time
import random
import board
import adafruit_dotstar as dotstar

# Using a DotStar Digital LED Strip with 30 LEDs connected to hardware SPI
#dots = dotstar.DotStar(board.SCK, board.MOSI, 144, brightness=0.2)

# Using a DotStar Digital LED Strip with 30 LEDs connected to digital pins
dots = dotstar.DotStar(board.D3, board.D2, 144, brightness=0.2)

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
        
def getTomorrowsWeather():
    print("TODO")

def getTrain():
    print("TODO")

n_dots = len(dots)
i = 0
while True:
    dots.fill(wheel(i))
    i = (i+20) % 384
