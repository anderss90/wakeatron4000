import time 
import os
import sys
from switch_nexa import NexaSwitcher
from config import Config

if len(sys.argv) != 2:
    sys.exit('Usage: %s device' % sys.argv[0])
    print sys.argv
switcher = NexaSwitcher(Config.RASPBERRY_PI_DATA_PIN, Config.TRANSMITTER_CODE,int(sys.argv[1]))

switcher.switch(True)
switcher.switch(True)
switcher.switch(True)
switcher.switch(True)
switcher.switch(True)

