#!/usr/bin/python

import requests
import json
import subprocess
from presencedevice import PresenceDevice
from raumfeldconnect import RFSoapConnect
from huesensors import HueMotionWatch
from fritzboxrequest import FritzHostsWatch

class SmartHomePresence(object):

    def __init__(self, configfile):

        self.devices = []

        try:

            # try to open the configuration file
            f = open(configfile, "r")
            jconfig = json.loads(f.read())

            # read all devices from config file
            for device in jconfig["Devices"]:
                ndevice = PresenceDevice(device)
                self.devices.append(ndevice)

            # create a list of online devices, compare to device list from
            # config file
            if "FritzBox" in jconfig.keys():
                fh = FritzHostsWatch(jconfig["FritzBox"]["FritzPassword"])
                online_hosts = fh.getOnlineDevices()

                for device in self.devices:

                    is_online = True

                    try:
                        if next(host for host in online_hosts if host['ip'] == device.getDeviceAddress()):
                            print(device.getDeviceName())
                    except StopIteration as e:
                        is_online = False

                    if is_online:
                        print("add to database")

            # check if there is an entry for TeufelStreaming in configfile
            # if so, request streaming data
            if "TeufelStreaming" in jconfig.keys():

                # check whether the Teufel host is online or not
                teufel_host = jconfig["TeufelStreaming"]["Hostname"]
                if next(host for host in online_hosts if host['ip'] == teufel_host):

                    # connect to teufel streaming devices via SOAP
                    rfconnect = RFSoapConnect(
                        jconfig["TeufelStreaming"]["Hostname"],
                        jconfig["TeufelStreaming"]["Port"]
                    )

                    # TODO: Make something useful with the data
                    print(rfconnect.getDeviceStates())

            # check if there is an entry for a Philips Hue HueBridge
            if "HueBridge" in jconfig.keys():

                # if a hue bridge is online, it should be found by its hostname
                # in the fritzbox request
                hue_host = jconfig["HueBridge"]["Hostname"]

                if next(host for host in online_hosts if host['name'] == hue_host):

                    # if so, request sensor data. Only motion sensors will be returned
                    huewatch = HueMotionWatch(
                        jconfig["HueBridge"]["Hostname"],
                        jconfig["HueBridge"]["HueUser"]
                    )

                    # TODO: Make something useful with the data
                    print(huewatch.getMotionSensorData())

        except IOError as e:
            print(e)

        except ValueError as e:
            print(e)

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
    presencewatcher = SmartHomePresence("/home/fabian/Programmierung/Python/presence-watch/smarthome-presence.json")
