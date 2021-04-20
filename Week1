from time import time, sleep
import os
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import threading
import random
import datetime
import sys
from masterFunctions import *
from lifxlan import LifxLAN
import requests
from bson import ObjectId, json_util
from pymongo import MongoClient


# Find light on network
print("Discovering lights...")
lifx = LifxLAN(None)
devices = lifx.get_lights()
bulb = devices[0]
print("Selected {}".format(bulb.get_label()))

# set up sensors
# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)
# create the mcp object
mcp = MCP.MCP3008(spi, cs)
# create an analog input channel on pin 0
chan0 = AnalogIn(mcp, MCP.P0)
chan1 = AnalogIn(mcp, MCP.P1)
chan2 = AnalogIn(mcp, MCP.P2)
chan3 = AnalogIn(mcp, MCP.P3)
chan4 = AnalogIn(mcp, MCP.P4)

client = mongo_setup()
db = client.mastersProject
collection = db.datalog1        # Pi 1
# collection = db.datalog2        # Pi 2
collection1 = db.activitylog1   # Pi 1
# collection1 = db.activitylog2   # Pi 2


def main():

    count30 = 0
    count = 0
    onabreak = False
    med = 90

    listoflists, listofheaders = set_values()
    listtimestamp, listback, listfrontRight, listfrontLeft, listbackRight, listbackLeft, listtotal = listoflists
    timestamp, back, frontRight, frontLeft, backRight, backLeft, total = listofheaders

    for ever in range(70):

        count += 1
        count30 += 1
        med += 1

        start = time()

        timestamp = get_time()
        frontRight, backRight, back, backLeft, frontLeft = get_sensor(
            chan0, chan1, chan2, chan3, chan4)
        total = back + frontRight + frontLeft + backRight + backLeft

        listofheaders = [timestamp, back, frontRight,
                         frontLeft, backRight, backLeft, total]

        for num in range(len(listofheaders)):
            listoflists[num].append(listofheaders[num])
            listoflists[num].pop(0)

        if count30 == 30:
            count30 = 0
            # send to mongo
            t1 = threading.Thread(target=data_to_mongo, args=[listtimestamp, listfrontRight, listbackRight,
                                                              listback, listbackLeft, listfrontLeft, collection])
            t1.start()

        # TODO fix for higher values
        # if all(number > 20 for number in listtotal) and onabreak == True:
        if listtotal.count(0) == 0 and onabreak == True:
            print("Meditation time")
            onabreak = False
            med = 0
            t2 = threading.Thread(target=meditation, args=[bulb, collection1])
            t2.start()

        # TODO fix for higher resting value
        # if all(number < 20 for number in listtotal) and onabreak == False:
        if listtotal.count(0) == 30 and onabreak == False and med > 70:
            print("Break time")
            breaktime(collection1)
            onabreak = True
            bulb.set_color((hue(260), saturation(1), brightness(0.2), 6000))

        # TODO test for breaktime during meditation
        if count > 1800 and count % 300 == 0:
            flash = (count-1800)//300
            bulb.set_waveform(0, (hue(0), saturation(
                1), brightness(0.4), 6000), 300, flash, 0, 1)

        end = time()
        duration = end - start
        #print("sleep for", 1-duration)
        sleep(1-duration)


main()
