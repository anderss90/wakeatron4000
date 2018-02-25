import sys
import time
#sys.path.append("/storage/.kodi/addons/python.RPi.GPIO/lib")
n_repeats = 5
import RPi.GPIO as GPIO

class NexaSwitcher:
    def __init__(self, data_pin, transmitter_code, device_id):
        self._data_pin = data_pin
        self._device_id = device_id
        self._transmitter_code = transmitter_code
        self.n_bits = 0
        if device_id > 15 or device_id < 0:
            print "device id invalid"
        print "Created NexaSwitcher for data PIN #" + str(self._data_pin) + " and transmitter code: " +\
              str(self._transmitter_code)

    def sleep_T(self, T_num):
        time.sleep(T_num*250/1000000.0)

    def send_physical_bit(self, bit_value):
        if bit_value:
            GPIO.output(self._data_pin, True)
            self.sleep_T(1)
            GPIO.output(self._data_pin, False)
            self.sleep_T(1)
        else:
            GPIO.output(self._data_pin, True)
            self.sleep_T(1)
            GPIO.output(self._data_pin, False)
            self.sleep_T(5)

    def send_bit(self, bit_value):
        self.send_physical_bit(not bit_value)
        self.send_physical_bit(bit_value)
        self.n_bits = self.n_bits+1
#        print bit_value

    def send_sync(self):
        GPIO.output(self._data_pin, True)
        self.sleep_T(1)
        GPIO.output(self._data_pin, False)
        self.sleep_T(10)

    def send_pause(self):
        GPIO.output(self._data_pin, True)
        self.sleep_T(1)
        GPIO.output(self._data_pin, False)
        self.sleep_T(40)

    def send_on_off(self, on_off):
        self.send_sync()
        self.n_bits = 0

        #transmitter code
        binary_number_string = format(self._transmitter_code, '08b')
        #print binary_number_string
        for digit in binary_number_string:
            bit = digit == '1'
            self.send_bit(bit)

        #group code
        self.send_bit(False)

        #on/off bit, on = 1, off = 0
        self.send_bit(on_off)

        binary_device_id = format(self._device_id, '04b')
        #print binary_device_id
        for digit in binary_device_id:
            bit = digit == '1'
            self.send_bit(bit)

        self.send_pause()
    

    def switch(self, on_off):
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self._data_pin, GPIO.OUT)
            for x in range(0, n_repeats):
                self.send_on_off(on_off)
                time.sleep(0.1)

            GPIO.output(self._data_pin, False) # Make sure that we do not leave PIN in 'on' state
        except KeyboardInterrupt:
            GPIO.cleanup()
        finally:
            GPIO.cleanup()

