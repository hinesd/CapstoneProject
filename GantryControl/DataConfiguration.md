Complete this After the Gantry has be assembled
--

Once the Gantry is assembled and the locks are in place, we need to update the config file. 

The config file is a yaml file that is converted to python dictionaries. it is important you keep the exact styling and spacing when updating the config file.

To get a clean blank template of the config file, you can use the yamlCreate script. 

Before setting up the website we must make sure that everything in the system is defined properly. 

Varibles
--
here is where the topics and the Broker IP is defined. 

Those topics can be changed to whatever you need. 

The BrokerIP needs to be updated to the IP address of device the broker lives on. If the broker is living on the RaspberryPi controlling the gantry system, put that RaspberryPi's IP.

Control Pins
-

Make sure that the value of the pins defined are BCM pin numbering, not the actual pin number.

Actuator_Pins, Gantry_Control_Pins, and Limit_Switch can be defined to whatever pins you want. The current values that are there are just the pins our team chose. 

Lock_Names
-
Lock names are the locks that are in the assembled system. Each lock in the system needs a unique identifier that is to be defined in Lock_Names. 
Once the name is defined, define what posistion that lock is in. the orientation of the "posistions" are completely up to the user and only necessary to understand during setup. Once the system is set up, a seperate machine will publish a message to the broker under the topic defined in variables, containing the unique indetifier located in Lock_Names. 

Gantry_Positions
-
The default config file uses 4 posistions, one posistion per lock defined in Lock_Names.
If more than default 4 posistions are used, more posistions will need to be defined using the same syntax as used in posistions 1-4. 

HorizontalMotor_SFH and VerticalMotor_SFH are the identifiers used to define the SFH, StepsFromHome. the value defined here is the number of times the Move Function is called, which executes 5080 steps each time, moving the gantry system 1/4 inch each call. These values are the "coordinates" of each posistion in the gantry system. These values will be updated by moving the gantry manually with the website. 


