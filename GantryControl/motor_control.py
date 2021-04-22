import os
import sys

if os.environ.get("MOCK_RPI")=='True':
	import MockGPIO as GPIO
else:
	import RPi.GPIO as GPIO

from time import sleep
import yaml
#CW = 1 #clockWise; Horizontal goes left; Vertical goes Down
#CCW = 0 #CounterClockwise; Horizontal goes Right ; Vertical goes up
#Down Left is home
Left = GPIO.HIGH
Down = GPIO.LOW
Right = GPIO.LOW
Up = GPIO.HIGH

def Data_From_config():
#This function is used to load data in from the config file, it returns two dictionaries
	configData = yaml.load(open('config.yaml'), Loader=yaml.FullLoader)
	GantryPins = configData["Gantry_Control_Pins"]

	return configData, GantryPins


def set_Position(configData, xCord, yCord,Pos):
#this function is used to update the position coordinates
	configData["Gantry_Positions"][Pos]["VerticalMotor_SFH"] = xCord
	configData["Gantry_Positions"][Pos]["HorizontalMotor_SFH"] = yCord
	with open(r'config.yaml','w') as file:
		yaml.dump(configData,file)

def enable(GantryPins):
#This sets the ENA pins that are connected to the motor driver HIGH
	GPIO.output(GantryPins["VerticalMotor"]["ENA_Pin"], GPIO.HIGH)
	GPIO.output(GantryPins["HorizontalMotor"]["ENA_Pin"], GPIO.HIGH)


def disable(GantryPins):
#This sets the ENA pins that are connected to the motor driver LOW
	GPIO.output(GantryPins["VerticalMotor"]["ENA_Pin"], GPIO.LOW)
	GPIO.output(GantryPins["HorizontalMotor"]["ENA_Pin"], GPIO.LOW)

def Actuate(P1, P2, PWM, Standby):
#Actuates the actuators based on the pin values recieved
	GPIO.output(P1, GPIO.LOW)
	GPIO.output(P2, GPIO.LOW)
	GPIO.output(P1, GPIO.HIGH)
	GPIO.output(PWM, GPIO.HIGH)
	GPIO.output(Standby, GPIO.HIGH)
	sleep(7)
	GPIO.output(P1, GPIO.LOW)
	GPIO.output(P2, GPIO.LOW)
	GPIO.output(P2, GPIO.HIGH)
	GPIO.output(PWM, GPIO.HIGH)
    	GPIO.output(Standby, GPIO.HIGH)
	sleep(7)
	#for pin in configData["Actuator_Pins"].values():
        #        GPIO.output(pin, GPIO.LOW)

def Move_Actuator(configData, Actuator):
#This function is used to determine which actuator was called to move
	print("Actuator: "+ str(Actuator))
	print(configData["Actuator_Pins"])
	if(Actuator == "Actuator1"):
		Actuate(configData["Actuator_Pins"]["Act1_P1"],configData["Actuator_Pins"]["Act1_P2"],configData["Actuator_Pins"]["PWM1_Pin"],configData["Actuator_Pins"]["Standby"])
	else:
		Actuate(configData["Actuator_Pins"]["Act2_P1"],configData["Actuator_Pins"]["Act2_P2"],configData["Actuator_Pins"]["PWM2_Pin"],configData["Actuator_Pins"]["Standby"])

def Move(stepPin, GantryPins):
#This function is used to define the distance traveled each time its called
	#MicroStep = 32
	#SPR = 200 * MicroStep #Steps per revolution : 360 / step angle 1.8 for 1/32 step
	#6400 steps will rotate the motor shaft 1 full circle.
	SPR = 5080 # will move gantry 1/4 inch 
	delay = 0.1 / SPR  ## should finish loop in half a second
	enable(GantryPins)
	for x in range(SPR):
		GPIO.output(stepPin,GPIO.HIGH)
		sleep(delay)
		GPIO.output(stepPin, GPIO.LOW)
		sleep(delay)
	disable(GantryPins)


def Move_Up(GantryPins):
	print("Move up")
	GPIO.output(GantryPins["VerticalMotor"]["Dir_Pin"], Up) #clockwise
	Move((GantryPins["VerticalMotor"]["PUL_Pin"]), GantryPins)


def Move_Down(GantryPins):
	print("Move Down")
	GPIO.output(GantryPins["VerticalMotor"]["Dir_Pin"], Down) #counter-clockwise
	Move(GantryPins["VerticalMotor"]["PUL_Pin"], GantryPins)


def Move_Left(GantryPins):
	print("Move Left")
	GPIO.output(GantryPins["HorizontalMotor"]["Dir_Pin"], Left) #counter-clockwise
	Move(GantryPins["HorizontalMotor"]["PUL_Pin"], GantryPins)


def Move_Right(GantryPins):
	print("Move Right")
	GPIO.output(GantryPins["HorizontalMotor"]["Dir_Pin"], Right) #Clockwise
	Move(GantryPins["HorizontalMotor"]["PUL_Pin"], GantryPins)


def find_home(configData, GantryPins):
#This function will move the motor until the home limit switch is triggered
	SPR = 200 * 32 #Steps per revolution : 360 / step angle 1.8
	#this will rotate the motor shaft 1 full circle. 
	delay = .1 / SPR
	GPIO.output(GantryPins["HorizontalMotor"]["Dir_Pin"], Left) #counter-clockwise
	enable(GantryPins)
	while(GPIO.input(configData["Limit_Switch"]["HMSwitchHome"])):
		GPIO.output(GantryPins["HorizontalMotor"]["PUL_Pin"], GPIO.HIGH)
		sleep(delay)
		GPIO.output(GantryPins["HorizontalMotor"]["PUL_Pin"], GPIO.LOW)
		sleep(delay)
	# Down Left is home
	GPIO.output(GantryPins["VerticalMotor"]["Dir_Pin"], Down) #counterClockwise
	while(GPIO.input(configData["Limit_Switch"]["VMSwitchHome"])):
		GPIO.output(GantryPins["VerticalMotor"]["PUL_Pin"], GPIO.HIGH)
		sleep(delay)
		GPIO.output(GantryPins["VerticalMotor"]["PUL_Pin"], GPIO.LOW)
		sleep(delay)
## this call is to keep the motors at least 1 Move() away from the limit switches
# that will be the defined home position
	Move_Up(GantryPins)
	Move_Right(GantryPins)
	disable(GantryPins)
	print("I am Home")
	return

def Setup(configData, GantryPins):
	 #Sets up all gpio pins and creates configDataionary from config file 
	GPIO.setmode(GPIO.BCM)
	for pin in configData["Limit_Switch"].values():
		GPIO.setup(pin, GPIO.IN)
		print("limit switch pin on RaspberryPi: " + str(pin))
	for pin in configData["Actuator_Pins"].values():
                GPIO.setup(pin, GPIO.OUT)
                print("actuator pin on RaspberryPi: " + str(pin))
	#set up PUL pins
	print("Vertical Motor: " +str(GantryPins["VerticalMotor"]))
	print("Horizontal Motor: " +str(GantryPins["HorizontalMotor"]))
	GPIO.setup(GantryPins["VerticalMotor"]["PUL_Pin"], GPIO.OUT)
	GPIO.setup(GantryPins["HorizontalMotor"]["PUL_Pin"], GPIO.OUT)
	#set up direction pins
	GPIO.setup(GantryPins["VerticalMotor"]["Dir_Pin"], GPIO.OUT)
	GPIO.setup(GantryPins["HorizontalMotor"]["Dir_Pin"], GPIO.OUT)
	#set up ENA pins
	GPIO.setup(GantryPins["VerticalMotor"]["ENA_Pin"], GPIO.OUT)
	GPIO.setup(GantryPins["HorizontalMotor"]["ENA_Pin"], GPIO.OUT)
	print("Pins Set up")


def Stepper(configData, StepsFromHome, GantryPins):
	#this function will move to the location of the Item in the gantry system
	# Steps from home are the coordinates that were defined in Set_Position
	Y_cord = StepsFromHome["VerticalMotor_SFH"]
	Z_cord = StepsFromHome["HorizontalMotor_SFH"]
	step_count_VM = Y_cord
	step_count_HM = Z_cord
	enable(GantryPins)
	GPIO.output(GantryPins["VerticalMotor"]["Dir_Pin"], Up)
	GPIO.output(GantryPins["HorizontalMotor"]["Dir_Pin"], Right)
	print("Move vertical motor")
	for x in range(int(step_count_VM)):
		Move(GantryPins["VerticalMotor"]["PUL_Pin"],GantryPins)
	print("Move horizontal motor")
	for x in range(int(step_count_HM)):
		Move(GantryPins["HorizontalMotor"]["PUL_Pin"],GantryPins)
	disable(GantryPins)
	return


def Find_Item(Item, configData, GantryPins):
	#This function will check if the Item exists inside of the dictionary, and if it does, call
	# stepper with the positions defined in the dictionary
	if Item in configData["Item_Names"]:
		print(Item + " exists and is located at " + configData["Item_Names"][Item])
		print(configData["Item_Names"][Item] + " is located at " + str(configData["Gantry_Positions"][configData["Item_Names"][Item]]))
		StepsFromHome = configData["Gantry_Positions"][configData["Item_Names"][Item]]
		Stepper(configData, StepsFromHome, GantryPins)
	else:
		print("Item doesnt exist")
