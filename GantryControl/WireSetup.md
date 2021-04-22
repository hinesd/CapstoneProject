All of the wires that are used in the gantry system are defined in the config.yaml file. 


  ---------------------------------------------
  WHEN WIRING TO THE RASPBERRYPI, THE PIN DIAGRAM THAT IS USED IS BCM, NOT THE LITERAL PIN NUMBERS.
  ---------------------------------------------

  to find the BCM pinout for your raspberryPi, in the terminal on the RaspberryPi, type pinout. the numbering scheme used will look like GPIO2 (3).
  2 is the BCM pin definition, 3 is the actual pin on the RaspberryPi


Motor Drivers:
--
  Each Motor requires a motor driver. Follow the Datasheet to determine which wires get plugged into the A and B slots on the driver.
  https://openbuildspartstore.com/nema-23-stepper-motor-high-torque-series/
  
  VCC and ground goes to Power Supply.  
  
  ENA+, DIR+, and PUL+ all need 3.3v of power. 
  ENA-, DIR-, and PUL- all will be attatched to the RaspberryPi. 
  When looking in the config.yaml file under Gantry_Control_Pins, HorizontalMotor and VerticalMotor have their defined PUL, ENA, and DIR pins. 
  
 Limit Switches:
 --
  The limit switches used all have 3 wires, Power( we used 3.3v), Ground, and Signal. 
  https://openbuildspartstore.com/xtension-limit-switch-kit/
  
  There are two types of limit Switches. Home Limit Switches, and End limit Switches. The home limit switches are used for positioning because encoders weren't       used. The End switches are used to account for failure, they are attached to interrupts that clear the GPIO pins once reached. 
  
  HM stands for Horizontal Motor, VM stands for Vertical Motor. 
  
  The Signal pin on the limit switch is attached to the GPIO pin defined in the config file. 
  
  Actuators:
  --
  
  SparkFun Motor Driver - Dual TB6612FNG (with Headers) https://www.sparkfun.com/products/14450
  
  this Motor Driver can be used to control 2 Actuators.
  
  VM and VCC were both given 5V.
  
  The Motor Driver to control the two actuators require 7 pins on the RaspberryPi.
  
  When looking at the datasheet for the motor driver, the A pins can be used for Actuator 1 and the B pins can be used for Actuator 2, and vice versa. 
  The A0 and B0 pins are the output pins that will be attached to the Actuators. A01 and B01 will be the Positive, and A02 and B02 will be the negative. 
  (AI,PWMA) and (BI,PWMB) are the input pins that recieve signals from the RaspberryPi. 
  
  The pins used are defined under Actuator_Pins in the config file. 

  Act1_P1, Act1_P2, and PWMA can be used for the AI pins. Act2_P1, Act2_P2, and PWMB can be used for the BI pins. Or vice versa. 
  There is only one Standby Pin. 
  
  
  
  
