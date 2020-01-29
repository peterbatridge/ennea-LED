import threading
from datetime import datetime, timedelta
import schedule
import credentials
import requests
import json
CTA_DATETIME = '%Y-%m-%dT%H:%M:%S'
CTA_LOCK = threading.Semaphore(1)
mm_bound_timer = False
chi_bound_timer = False

###
# Train Functions
###
cta_train_line_base = "http://lapi.transitchicago.com/api/1.0/ttpositions.aspx?rt=brn,p&outputType=JSON&key="


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