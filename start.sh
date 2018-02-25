#!/bin/sh

#sudo killall python
#sleep 1
python /home/pi/workspace/autoHome2/loop.py >/home/pi/workspace/autoHome2/logloop 2>&1 &
