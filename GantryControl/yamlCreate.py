#This file is used to create the config file for each new system to reset all of the data in the config file
#!/usr/bin/env python3
import yaml
d = {
	"Item_Names": {
		"Item1": "position1",
		"Item2": "position2",
		"Item3": "position3",
                "Item4": "position4"
		},
	"Gantry_Positions": {
		#SFH = Steps From Home
		"position1": {"VerticalMotor_SFH": 0, "HorizontalMotor_SFH": 0},
		"position2": {"VerticalMotor_SFH": 0, "HorizontalMotor_SFH": 0},
		"position3": {"VerticalMotor_SFH": 0, "HorizontalMotor_SFH": 0},
		"position4": {"VerticalMotor_SFH": 0, "HorizontalMotor_SFH": 0}
		},
	"Limit_Switch":{
		"VMSwitchHome": 20,
		"VMSwtichEnd": 12,
		"HMSwitchHome": 21,
		"HMSwtichEnd": 16,

	},
	"Actuator_Pins":{
		"Act1_P1" : 0,
 		"Act1_P2": 5,
		"Act2_P1" : 13,
                "Act2_P2": 19,
 		"PWM1_Pin": 6,
		"PWM2_Pin": 26,
 		"Standby": 11
	},
	"Gantry_Control_Pins":{
		"VerticalMotor":{"PUL_Pin": 2, "Dir_Pin": 3, "ENA_Pin": 4}, 
		"HorizontalMotor":{"PUL_Pin": 17, "Dir_Pin": 27, "ENA_Pin": 22}
	},
	"Variables":{
		"Broker_IP": "10.40.97.105",
		"Topic": "test/message",
		"Actuator_Topic" : "test/actuator"
	}

}

with open(r'config.yaml','w') as file:
	yaml.dump(d,file)
