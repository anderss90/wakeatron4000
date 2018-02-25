import time 
import os
import sys
from switch_nexa import NexaSwitcher
from config import Config

if len(sys.argv) != 3:
    sys.exit('Usage: %s device on/off' % sys.argv[0])
    print sys.argv
switcher = NexaSwitcher(Config.RASPBERRY_PI_DATA_PIN, Config.TRANSMITTER_CODE,int(sys.argv[1]))
if sys.argv[2] == "off":
    switcher.switch(False)
elif sys.argv[2] == "on":
    switcher.switch(True)
else: 
    switcher.switch(int(sys.argv[2]))


