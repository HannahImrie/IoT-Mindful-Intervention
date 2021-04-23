from notification import *
import os
from time import time, sleep
import datetime
import json
from bson import ObjectId, json_util
from pymongo import MongoClient
import requests
import RPi.GPIO as GPIO

#(hue, sat, brightness, kelvin)


def mongo_setup(f):

    f.write(os.getcwd())

    secrets = open("home/pi/shared_files/secrets.json")
    secrets = json.load(secrets)
    token = secrets["Mongo_Key"]

    try:
        client = MongoClient(token)
        print("Connection Successful...")
        return client
    except:
        try:

            print("Could not connect to MongoDB...")
            print("Attempting again...")
            client = MongoClient(token)
            GPIO.output(27, GPIO.HIGH)
            return client
        except:
            GPIO.output(27, GPIO.LOW)
            print("Can't connect :(")
            f.write("\nmongodb issue")


def hue(value):  # 0-360
    return int(round(65535 * value) / 360)


def saturation(value):  # 0-1
    return int(round(65535 * value))


def brightness(value):  # 0-1
    return int(round(65535 * value))


def kelvin(value):
    return (hue(120), saturation(0), brightness(0.2), value)


def meditation(bulb, collection):
    start = datetime.datetime.now()
    bulb.set_waveform(0, (hue(60), saturation(
        0.01), brightness(0.3), 6000), 300, 2, 0, 1, rapid=True)
    sleep(5)
    bulb.set_color((hue(60), saturation(1), brightness(0.2), 6000), rapid=True)
    sleep(0.2)
    meditation_start = datetime.datetime.now()
    for x in list(range(6)):
        bulb.set_waveform(0, (hue(60+x*10), saturation(0.01),
                          brightness(0.4), 6000), 4000, 1, 0, 2, rapid=True)
        sleep(4)
        bulb.set_waveform(0, (hue(60+x*10), saturation(0.01),
                          brightness(0.5), 6000), 250, 1, 0, 1, rapid=True)
        sleep(0.3)
        bulb.set_waveform(0, (hue(60+x*10), saturation(1),
                          brightness(0.2), 6000), 4000, 1, 0, 2, rapid=True)
        sleep(4)
        bulb.set_color((hue(60+x*10), saturation(1),
                       brightness(0.01), 6000), 200, rapid=True)
        sleep(1)
        bulb.set_color((hue(60+x*10), saturation(1),
                       brightness(0.2), 6000), 200, rapid=True)
        sleep(0.2)
    bulb.set_waveform(0, (hue(60+x*10), saturation(0.01),
                      brightness(0.3), 6000), 250, 3, 0, 1, rapid=True)
    meditation_end = datetime.datetime.now()
    sleep(0.8)
    to_red()
    data = {
        "Break End": start.strftime("%F %H:%M:%S.%f"),
        "Meditation Start": meditation_start.strftime("%F %H:%M:%S.%f"),
        "Meditation End": meditation_end.strftime("%F %H:%M:%S.%f")
    }
    file_data = json.loads(json_util.dumps(data))
    print(file_data)
    collection.insert_one(file_data)    # insert data in collection


def breaktime(collection):
    start = datetime.datetime.now()
    data = {
        "Break Start": start.strftime("%F %H:%M:%S.%f"),
    }
    file_data = json.loads(json_util.dumps(data))
    print(file_data)
    collection.insert_one(file_data)    # insert data in collection


def get_sensor(chan0, chan1, chan2, chan3, chan4):

    bL = chan0.value
    bR = chan1.value
    b = chan2.value
    fR = chan3.value
    fL = chan4.value

    print(f"FR: {fR}, BR: {bR}, B: {b}, BL: {bL}, FL: {fL}")
    return fR, bR, b, bL, fL


def get_time():
    now = datetime.datetime.now()  # Current Time
    return now.strftime("%F %H:%M:%S.%f")


def set_values():

    # set up lists
    listtimestamp = [0]*30
    listback = [0]*30
    listfrontRight = [0]*30
    listfrontLeft = [0]*30
    listbackRight = [0]*30
    listbackLeft = [0]*30
    listtotal = [0]*30

    # set up values
    timestamp = None
    back = None
    frontRight = None
    frontLeft = None
    backRight = None
    backLeft = None
    total = None

    # set up array
    listoflists = [listtimestamp, listback, listfrontRight,
                   listfrontLeft, listbackRight, listbackLeft, listtotal]

    listofheaders = [timestamp, back, frontRight,
                     frontLeft, backRight, backLeft, total]

    return listoflists, listofheaders


def data_to_mongo(timestamp, fR, bR, b, bL, fL, collection):

    dict = {
        "Timestamp": timestamp,
        "FR": fR,
        "BR": bR,
        "B": b,
        "BL": bL,
        "FL": fL
    }
    # put the data in the correct form
    file_data = json.loads(json_util.dumps(dict))
    # print(file_data)
    collection.insert_one(file_data)    # insert data in collection
