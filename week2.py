from pymongo import MongoClient
from bson import ObjectId, json_util
import requests
from lifxlan import LifxLAN
from masterFunctions import *
import sys
import datetime
import random
import threading
from adafruit_mcp3xxx.analog_in import AnalogIn
import adafruit_mcp3xxx.mcp3008 as MCP
import board
import digitalio
import busio
import os
from time import time, sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(27, GPIO.OUT)
GPIO.output(27, GPIO.LOW)

f = open("/home/pi/shared_files/demofile2.txt", "a")

# Find light on network
print("Discovering lights...")
lifx = LifxLAN(None)
for _ in range(5):

    try:
        devices = lifx.get_lights()
        bulb = devices[0]
        print("LED on")
        GPIO.output(27, GPIO.HIGH)
        break
    except:

        sleep(15)
        continue

print("Selected {}".format(bulb.get_label()))

# set up sensors
# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)
# create the mcp object
mcp = MCP.MCP3008(spi, cs)
# create an analog input channel on pin 0
chan0 = AnalogIn(mcp, MCP.P0)
chan1 = AnalogIn(mcp, MCP.P1)
chan2 = AnalogIn(mcp, MCP.P2)
chan3 = AnalogIn(mcp, MCP.P3)
chan4 = AnalogIn(mcp, MCP.P4)

client = mongo_setup(f)
db = client.mastersProject
# collection = db.datalog1        # Pi 1
collection = db.datalog2        # Pi 2
# collection1 = db.activitylog1   # Pi 1
collection1 = db.activitylog2   # Pi 2


def main():

    count30 = 0
    count = 0
    onabreak = False
    med = 90

    listoflists, listofheaders = set_values()
    listtimestamp, listback, listfrontRight, listfrontLeft, listbackRight, listbackLeft, listtotal = listoflists
    timestamp, back, frontRight, frontLeft, backRight, backLeft, total = listofheaders

    #f.write("\nMade it to main")

    while True:
        # for _ in range(60):

        count += 1
        count30 += 1
        med += 1

        #f.write("\nMade it to while"+str(count30))

        start = time()

        timestamp = get_time()
        frontRight, backRight, back, backLeft, frontLeft = get_sensor(
            chan0, chan1, chan2, chan3, chan4)
        total = back + frontRight + frontLeft + backRight + backLeft

        listofheaders = [timestamp, back, frontRight,
                         frontLeft, backRight, backLeft, total]

        #f.write("\nGot sensor data")

        for num in range(len(listofheaders)):
            listoflists[num].append(listofheaders[num])
            listoflists[num].pop(0)

        #f.write("\nadded to list")

        if count30 == 30:
            count30 = 0
            # send to mongo
            t1 = threading.Thread(target=data_to_mongo, args=[listtimestamp, listfrontRight, listbackRight,
                                                              listback, listbackLeft, listfrontLeft, collection])
            #f.write("Sending 30 data")
            t1.start()
            # f.write("sent")

        # TODO fix for higher values
        if all(number > 650 for number in listtotal) and onabreak == True:
            # if listtotal.count(0) == 0 and onabreak == True:
            f.write("\nMeditation Time")
            print("Meditation time")
            count = 0
            onabreak = False
            med = 0
            t2 = threading.Thread(target=meditation, args=[bulb, collection1])
            t2.start()

        # TODO fix for higher resting value
        if all(number < 650 for number in listtotal) and onabreak == False and med > 70:
            # if listtotal.count(0) == 30 and onabreak == False and med > 70:
            print("Break time")
            f.write("\nbreaktime send")
            breaktime(collection1)
            #f.write("\nafter breaktime send")
            onabreak = True
            bulb.set_color((hue(260), saturation(1), brightness(0.2), 6000))

        # TODO test for breaktime during meditation
        if count > 3200 and count % 300 == 0 and onabreak == False:
            flash = (count-3200)//300
            bulb.set_waveform(0, (hue(0), saturation(
                1), brightness(0.4), 6000), 300, flash, 0, 1)
        #f.write("\nalmost at end")
        end = time()
        duration = end - start
        #f.write("\nbefore sleep" + str(duration))
        #print("sleep for", 1-duration)
        if duration < 1:
            sleep(1-duration)
        #f.write("\nafter sleep")


main()
