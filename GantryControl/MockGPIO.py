HIGH = 1
LOW = 0
BCM = 1
OUT = "OUT"
IN = "IN"

#all available GPIO pins on our RaspberryPi
pinout = {
    2: {"state": "OUT", "value": None},
    3: {"state": "OUT", "value": None},
    4: {"state": "OUT", "value": None},
    14: {"state": "OUT", "value": None},
    15: {"state": "OUT", "value": None},
    17: {"state": "OUT", "value": None},
    18: {"state": "OUT", "value": None},
    27: {"state": "OUT", "value": None},
    22: {"state": "OUT", "value": None},
    23: {"state": "OUT", "value": None},
    24: {"state": "OUT", "value": None},
    25: {"state": "OUT", "value": None},
    10: {"state": "OUT", "value": None},
    9: {"state": "OUT", "value": None},
    11: {"state": "OUT", "value": None},
    8: {"state": "OUT", "value": None},
    7: {"state": "OUT", "value": None}
   
}
def cleanup():
    pass

def setmode(val):
    pass

def setup(pin, state):
    pinout[pin]["state"] = state
    #pin corresponds to pin on RPI
    #state is either input or output
def output(pin, value):
    pinout[pin]["value"] = value
    #pin corresponds to pin on RPI
    #value is either HIGH  or LOW

def input(pin):
    if(pinout[pin]["state"] == "IN"):
        return pinout[pin]["value"]
    #pin corresponds to pin on RPI
    #check if that pin is and input pin and then return its state
    
