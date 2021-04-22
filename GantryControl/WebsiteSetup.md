#

-------------------
Before doing these things be sure to read and complete DataConfiguration and WireSetup
-------------------

To install docker:
--

sudo apt-get update

sudo apt-get upgrade

curl -sSL https://get.docker.com | sh

To build a docker container:
--

docker build -t gantry .

To run the docker container:

docker run --privileged -d --rm -it -p 5000:5000 -v `pwd`:/app gantry



Using the Website:
--

find IP of raspberryPi, or IP of Broker and update the IP in BrokerIP in the config file

connect the website via port 5000 of whatever the IP is of the device hosting the website

Update the config file following the consistient style of the rest of the document
define all of the Items that are in the gantry system
define what posistion those Items are located at

Once connected, the posistion of the Items that are defined in the configuration file need to be defined in the system before use. Click "update posistion coordinates" button. 
This will take you to a new page that will show you what Items, and posisitons are defined in the system. 
The system is completely moldabale to however it is defined in the config file. 

To define the coordinates of a Item in the gantry system, click the directional buttons the move the 
gantry to a positions that places the actuators in front of the Item. Once satisfied with the location,
click the drop down and select which posistion you are setting coordinates for. Once you click the Set Posistion New Coordinates button, the gantry system will go home, and then updates the coordinates
of that posistion in the config file. 

To test if those coordinates are what you want, click Return to Homepage button

Type in the name of the Item that was specified in the config file, and once Submit is hit,
The gantry system will move to the position that the Item is defined.  
