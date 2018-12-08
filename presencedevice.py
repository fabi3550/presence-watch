#!/usr/bin/python

class PresenceDevice(object):

    def __init__(self, device):

        if "Address" in device.keys():
            self.deviceaddress = device["Address"]

        if "Name" in device.keys():
            self.devicename = device["Name"]

        if "Owner" in device.keys():
            self.deviceowner = device["Owner"]

        if "Type" in device.keys():
            self.devicetype = device["Type"]

    def getOwner(self):
        return self.deviceowner

    def getDeviceType(self):
        return self.devicetype

    def getDeviceName(self):
        return self.devicename

    def getDeviceAddress(self):
        return self.deviceaddress
