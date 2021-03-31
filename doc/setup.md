# Setup
The recommended prequisites:
* Tentacle runs on a Raspberry Pi, it is recommended to use the latest official [Raspbian distribution](https://www.raspberrypi.org/downloads/raspbian/).
* At least one supported sensor, i.e. the famous temperature sensor BME280.
* It is also recommended to use `avahi` for hostname resolution within the LAN so your webinterface will not only be availible on i.e. `192.168.178.123:8000` but on `raspberrypi.local:8000`.

Now you need to install tentacle, clone it with git:
```bash
git clone https://github.com/tentacle-project/tentacle <path you like to clone it to>
```
Tentacle needs some python modules which themselfes need more python modules which gets confusing pretty fast. To keep it simple it is recommended to use a virtual environment such as `pipenv`: `sudo apt install pipenv`

The necessary python modules are listed in <a href="https://github.com/tentacle-project/tentacle/src/branch/master/Pipfile" target="_blank">Pipfile</a>. You can install them by running `pipenv install` within the repository.

On the satellite you need to install `mosquitto-clients`:
```
sudo apt install -y mosquitto-clients
```

On the system running the MQTT-host you need to install both, the clients and the broker:
```
sudo apt install -y mosquitto mosquitto-clients
```
The installation of `mosquitto` will automatically start and enable the mosquitto broker via the service `mosquitto.service`. Next you need to copy the mosquitto config file for tentacle to the mosquitto configuration. On linux you can symlink it: `sudo ln /path/to/tentacle/conf/tentacle.conf /etc/mosquitto/conf.d/tentacle.conf`

And don't forget to restart mosquitto: `sudo systemctl restart mosquitto`

Now you have to install the modules for the sensors and you need for tentacle.
Go into the tentacle folder:
`pipenv install [-d]`

Now the software is installed you need to enable the bus on your Pi corresponding to your sensor. You can see which bus is used by which sensor in the [list of supported sensors](sensors.md)

# Activate buses
To activate specific buses start raspi-config
`raspi-config`
Select Interfacing Options->[I2C, 1-Wire, SPI, Serial]
