#Import all neccessary features to code.
import RPi.GPIO as GPIO
from time import sleep

#If code is stopped during active it will stay active
#This may produce a warning if restarted, this
#line prevents that.
GPIO.setwarnings(False)
#This means we will refer to the GPIO
#by the number after GPIO.
GPIO.setmode(GPIO.BCM)
#This sets up the GPIO 18 pin as an output pin
GPIO.setup(18, GPIO.OUT)

while (True):    
    
    #This Turns Relay Off. Brings Voltage to Max GPIO can output ~3.3V
    GPIO.output(18, 1)
    #Wait 1 Seconds
    sleep(1)
    #Turns Relay On. Brings Voltage to Min GPIO can output ~0V.
    GPIO.output(18, 0)
    #Wait 1 Seconds
    sleep(1)
    
