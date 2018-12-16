#!/usr/bin/python

import requests
import json
import subprocess
from presencedevice import PresenceDevice
from raumfeldconnect import RFSoapConnect

class SmartHomePresence(object):

    def __init__(self):

        self.devices = []

        try:

            f = open("smarthome-presence.json", "r")
            jconfig = json.loads(f.read())

            for device in jconfig["Devices"]:
                ndevice = PresenceDevice(device)
                self.devices.append(ndevice)

            # ping devices
            for device in self.devices:
                print(device.getDeviceName() + ":" + str(self.isDeviceOnline(device)))

            # connect to teufel streaming devices via SOAP
            rfconnect = RFSoapConnect(jconfig["TeufelHost"], jconfig["TeufelPort"])
            print(rfconnect.getDeviceStates()) 

        except IOError as e:
            print(e)

    def isMotionSensor(self):
        pass

    def getLastMotionTimestamp(self, sensor):
        pass

    def isDeviceOnline(self, device):

        is_online = False

        response = subprocess.Popen(["ping", device.getDeviceAddress(), "-c", "1", "-W", "2"], stdout=subprocess.PIPE)
        response.wait()

        if response.poll() == 0:
            is_online = True

        return is_online

    def hasPresence(self):
        pass

if __name__ == "__main__":
    presencewatcher = SmartHomePresence()
