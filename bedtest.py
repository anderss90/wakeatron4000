debug_mode = False
import time 
import os
import sys
import serial
import pygame
from pygame import mixer

#import subprocess
#from switch_nexa import NexaSwitcher
from config import Config
from datetime import datetime, timedelta


#heater = NexaSwitcher(Config.RASPBERRY_PI_DATA_PIN, Config.TRANSMITTER_CODE,Config.device_number['heater'])
#bedroom1 = NexaSwitcher(Config.RASPBERRY_PI_DATA_PIN, Config.TRANSMITTER_CODE,1)


ser = serial.Serial('/dev/ttyUSB0',38400,timeout=1)
time.sleep(1)


song_1 = os.path.join('/home/pi/workspace/autoHome2/music','gladiator.mp3')
song_2 = os.path.join('/home/pi/workspace/autoHome2/music','morgenstemning.mp3')
song_3 = os.path.join('/home/pi/workspace/autoHome2/music','Hopipolla.mp3')
song_4 = os.path.join('/home/pi/workspace/autoHome2/music','flutterby.mp3')
song_5 = os.path.join('/home/pi/workspace/autoHome2/music','get_up.mp3')

lights_on = False
mixer_on = False
debug_print = True
alarm_state = "idle"
if debug_mode:
    alarm_state = "song_1"

invert_bed = debug_mode
sleep_time = 1
bed_threshold = Config.bed_threshold_value
base_volume = 0.7

def printer(value):
    if debug_print:
        print value

def serialChecker():
    notComplete = True 
    number = 0
    while notComplete:
        number = number+1
        printer("SerialChecker sending")
        printer(number)
        ser.write(str(number))
        returned = ser.readline()
        if len(returned) <1:
            printer ("Nothing received, failed")
            continue
        if int(returned) is number:
            notComplete = False
            printer("SerialChecker complete")
        else:
            printer("Serialchecker failed")
            printer (returned)
        printer(" ")
        time.sleep(1)


def printSerial():
    printer(ser.readline())

def in_bed():
    printer("in_bed")
    ser.write("bed\n")
    time.sleep(0.1)
    bed_value_received = False
    counter = 5
    while not bed_value_received:
        bed_string = ser.readline()
        printer(bed_string)
        if "bed:" in bed_string:
            bed_value_received = True
            bed_string.find(":")
            substrings = bed_string.split(":")
            value = int(substrings[1])
            printer(value)
            if value is 0:
                printer(" BED IS 0, returning true")
                return not invert_bed

            if value > bed_threshold:
                printer(" = True")
                return not invert_bed
            else: 
                printer(" = False")
                return invert_bed
        else:
            counter = counter-1
            if counter <= 0:
                printer ("bed time out, returning True")
                return True

alarm_paused = False
def alarm_pause():
    global alarm_paused
    if alarm_paused is False:
        #mixer.music.fadeout(500)
        mixer.music.pause()
        alarm_paused = True

def alarm_unpause():
    global alarm_paused
    if alarm_paused is True:
        mixer.music.unpause()
        alarm_paused = False

def alarm_periodic():
    global mixer_on
    if not mixer_on:
        mixer.init()
        mixer_on = True
        mixer.music.set_volume(base_volume)

    printer("alarm periodic")
    global alarm_state
    if not in_bed():
        printer("i am not in bed lol")
        #debug alarm_pause()
        return

    else:
        alarm_unpause()

    if  mixer.music.get_busy():
        printer("mixer busy")
        return
    if alarm_state is "idle":
        printer("playing gladiator")
        mixer.music.load(song_1)
        mixer.music.set_volume(base_volume)
        mixer.music.play()
        alarm_state = "song_1"
    elif alarm_state is "song_1":

        #printer("opening roller blinds")
	printer("playing song_2")
        ser.write("1on\n")
        printSerial()
        time.sleep(1)
        mixer.music.set_volume(0.7)
        mixer.music.load(song_2)
        mixer.music.play()
        alarm_state = "song_2"
        
        #subprocess.call("sudo /home/pi/workspace/nexa_send_command 1on >testlog3 2>&1",shell=True)
        #os.system("sudo /home/pi/workspace/nexa_send_command 1on ")

    elif alarm_state is "song_2":
        #printer("turning on lights")
        ser.write("up\n")
        printSerial()
        time.sleep(1)
        printer("playing song_3")
        mixer.music.load(song_3)
        mixer.music.set_volume(base_volume+0.1)
        mixer.music.play()
        alarm_state = "song_3"
    elif alarm_state is "song_3":
        printer("playing song_4")
        mixer.music.set_volume(base_volume+0.2)
        mixer.music.load(song_4)
        mixer.music.play()
        alarm_state = "song_4"
    elif alarm_state is "song_4":
        printer("playing song_5")
        mixer.music.set_volume(base_volume+0.2)
        mixer.music.load(song_5)
        mixer.music.play()
        alarm_state = "song_5"


    elif alarm_state is "song_5":
        pass
    #debug     alarm_state = "song_4"
    else:
        printer("state is not idle")
        printer(" ")

# "main" loop
serialChecker()
heater_on = False
while True:
    in_bed()
    
