
import os
#if os.environ.get("TESTMODE"):
if False:
	import MockGPIO as GPIO
else:
	import RPi.GPIO as GPIO
	
from flask import Flask, render_template, request, jsonify
from flask_mqtt import Mqtt
from motor_control import *
import yaml
import json


configData, Gantry_Pins = Data_From_config()
def interruptTriggered(channel):
    GPIO.cleanup()
    print("Limit Switch Triggered. You went too far! reset GPIO pins")

def interrupt():

##This is defined seperately because event detection can only be done once
# or it will break things
# the other GPIO setup things can be called multiple time without breaking things
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(configData["Limit_Switch"]["HMSwtichEnd"], GPIO.IN)
    GPIO.setup(configData["Limit_Switch"]["VMSwtichEnd"], GPIO.IN)
    GPIO.add_event_detect(configData["Limit_Switch"]["HMSwtichEnd"], GPIO.FALLING, callback=interruptTriggered)
    GPIO.add_event_detect(configData["Limit_Switch"]["VMSwtichEnd"], GPIO.FALLING, callback=interruptTriggered)

interrupt()

app = Flask(__name__)

print(configData["Variables"]["Broker_IP"])
app.config['MQTT_BROKER_URL'] = configData["Variables"]["Broker_IP"]
app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes
app.config['MQTT_CLEAN_SESSION'] = True
mqtt = Mqtt(app)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
	Setup(configData, Gantry_Pins)
	print(configData["Variables"]["Topic"])
	mqtt.subscribe(configData["Variables"]["Topic"])
	mqtt.subscribe(configData["Variables"]["Actuator_Topic"])

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
	global configData
	global Gantry_Pins
	msg = message.payload.decode()
	if(msg == "Actuator1"):
		Move_Actuator(configData,msg)
	elif(msg == "Actuator2"):
		Move_Actuator(configData, msg)
	elif(msg in configData["Item_Names"]):
        	find_home(configData, Gantry_Pins)
        	Find_Item(msg, configData, Gantry_Pins)
	else:
		print("Nothing happens")

@app.route('/')
@app.route('/home')
def home():
	return render_template("index.html")
@app.route('/Actuate')
def Actuate():
	global configData
	global Gantry_Pins
	Setup(configData, Gantry_Pins)
	Move_Actuator(configData, "Actuator1")
	return render_template("index.html")

@app.route('/PinClear')
def PinClear():
	GPIO.cleanup()
	interrupt()
	return render_template("index.html")


@app.route('/Find_Home', methods=["GET"])
def Find_Home():
	global configData
	global Gantry_Pins
	config, Pins = Data_From_config()
	configData = config
	Gantry_Pins = Pins
	Setup(configData, Gantry_Pins)
	print("route call")
	find_home(configData, Gantry_Pins)
	return render_template("index.html")


@app.route('/SetPins', methods=["POST"])
def SetPins():
	global configData
	global Gantry_Pins
	VM = eval(json.dumps(request.form['VerticalMotor']))
	HM = eval(json.dumps(request.form['HorizontalMotor']))
	Position = request.form['Position']
	set_Position(configData,VM,HM,Position)
	configData, Gantry_Pins = Data_From_config()
	find_home(configData, Gantry_Pins)
	return render_template("UpdatePositions.html", configData=configData,Gantry_Pins=Gantry_Pins )

@app.route('/MoveUp', methods=["POST"])
def MoveUp():
	pins = json.loads(request.data)
	print(pins)
	print(type(pins))
	if(pins == 0):
		return "nothing"
	Move_Up(pins)
	return "nothing"

@app.route('/MoveDown', methods=["POST"])
def MoveDown():
	pins = json.loads(request.data)
	print(pins)
	if(pins == 0):
		return "nothing"
	Move_Down(pins)
	return "nothing"

@app.route('/MoveRight', methods=["POST"])
def MoveRight():
	pins = json.loads(request.data)
	print(pins)
	if(pins == 0):
		return "nothing"
	Move_Right(pins)
	return "nothing"

@app.route('/MoveLeft', methods=["POST"])
def MoveLeft():
	pins = json.loads(request.data)
	print(pins)
	if(pins == 0):
		return "nothing"
	Move_Left(pins)
	return "nothing"

@app.route('/Move_To_Position', methods=['POST'])
def Move_To_Position():
	global configData
	global Gantry_Pins
	Setup(configData,Gantry_Pins)
	find_home(configData, Gantry_Pins)
	Item = request.form['ItemName']
	Find_Item(Item, configData, Gantry_Pins)
	return render_template("index.html")

@app.route('/Update_Positions', methods=['POST'])
def Update_Positions():
	global configData
	global Gantry_Pins
	Setup(configData, Gantry_Pins)
	#find_home(configData, Gantry_Pins)
	return render_template("UpdatePositions.html", configData=configData,Gantry_Pins=Gantry_Pins )

#if __name__ == '__main__':
#	app.run(debug=True, port=80, host='0.0.0.0')
