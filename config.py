from datetime import datetime, time
class Config:
    RASPBERRY_PI_DATA_PIN = 25
    bed_threshold_value = 80

    weekend = False

    # You can choose your own transmitter code randomly
    TRANSMITTER_CODE = 44356010
    device_number = dict([('bedroom1',0),('bedroom2',1),('bedroom_roof',2),('heater',3)])
    on = True
    off = False
    heater_on_time = time(5,0,0,0,None)
    heater_off_time = time(8,30,0,0,None)
    wakeup_time_start = time(7,45,0,0,None)
    wakeup_time_end = time(9,0,0,0,None)
#    wakeup_time_start = time(13,52,0,0,None)
#    wakeup_time_end = time(20,0,0,0,None)
    if weekend:
        wakeup_time_start = time(8,45,0,0,None)
        wakeup_time_end   = time(12,00,0,0,None)



