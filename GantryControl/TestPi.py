import RPi.GPIO as GPIO
from motor_control import *
from time import sleep
import pdb
#configData, Gantry_Pins = Data_From_config()
Left = GPIO.HIGH
Down = GPIO.HIGH
Right = GPIO.LOW
Up = GPIO.LOW
#Setup(configData, Gantry_Pins)
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT) #     Dir_Pin: 2
GPIO.setup(24, GPIO.OUT) #    ENA_Pin: 24
GPIO.setup(3, GPIO.OUT) #     PUL_Pin: 3
print("simulating 3 up button presses")
#pdb.set_trace()
delay = .01
for i in range(100):
    GPIO.output(2, Up)
    GPIO.output(24, GPIO.HIGH )
    #input("Check if enable pin is High, then press enter to continue")
    print("watch the PUL pin toggle")
    for x in range(10):
        GPIO.output(3,GPIO.HIGH)
        sleep(delay)
        GPIO.output(3, GPIO.LOW)
        sleep(delay)
    GPIO.output(24, GPIO.LOW )

print("simulating 3 down button presses")
for i in range(3):
    GPIO.output(2, Down)
    GPIO.output(24, GPIO.HIGH )
    print("watch the PUL pin toggle")
    for x in range(10):
        GPIO.output(3,GPIO.HIGH)
        sleep(delay)
        GPIO.output(3, GPIO.LOW)
        sleep(delay)
    GPIO.output(24, GPIO.LOW )

GPIO.cleanup()



