#!/usr/bin/python

import requests
import json
from xml.etree import ElementTree

class RFSoapConnect(object):

    def __init__(self, ip, port):

        # define the raumfeld/teufel streaming host
        self.ip = ip
        self.port = port

    # Requests host for all upnp devices and returns a list of rendering devices
    def getRenderingDevices(self):

        renderers = []

        try:

            xml_response = requests.post("http://" + self.ip + ":" + str(self.port) + "/listDevices")
            devices = ElementTree.fromstring(xml_response.content)

            for device in devices.iter("device"):

                if device.attrib["type"].find("MediaRenderer") > 0:
                    renderers.append(device.attrib["location"])

        except requests.exceptions.ConnectionError as e:
            print(e)

        except IOError as e:
            print(e)

        return renderers

    # requests a single rendering device fpr its state
    def getTransportState(self, deviceURL):

        transport_state = {}

        soap_request = """
            <?xml version="1.0" encoding="utf-8"?>
                <s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
                    <s:Body>
                        <u:GetTransportInfo xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
                            <InstanceID>0</InstanceID>
                        </u:GetTransportInfo>
                    </s:Body>
                </s:Envelope>'
            """

        # seperate the <ip:port> info from full url
        url = deviceURL.split("/")[2]

        # build a valid soap header
        headers = {
            'Content-Type': 'application/soap+xml; charset="utf-8"',
            'Host': url,
            'SOAPAction': 'urn:schemas-upnp-org:service:AVTransport:1#GetTransportInfo',
            'Content-Length': str(len(soap_request))
        }

        # request the service url with via soap
        try:
            response = requests.post(
                "http://" + url + "/AVTransport/ctrl",
                headers=headers,
                data=soap_request
            )

            # check for a valid answer. if given, return the trasport state from the answer
            if response.status_code == 200:
                xml_response = ElementTree.fromstring(response.content)
                transport_state = json.dumps({'device': url.split(":")[0], 'state': xml_response[0][0][0].text, 'status': xml_response[0][0][1].text}, separators=(',', ':'))

        except requests.exceptions.ConnectionError as e:
            print(e)

        return transport_state

    # returns a complete list of states of all rendering devices in json
    def getDeviceStates(self):

        devicelist = []

        devices = self.getRenderingDevices()

        for device in devices:
            state = self.getTransportState(device)
            devicelist.append(state)

        return json.dumps(devicelist, separators=(',', ':'))


if __name__ == "__main__":

    rfconnect = RFSoapConnect('192.168.178.48', 47365)
    devices = rfconnect.getRenderingDevices()
    for device in devices:
        state = rfconnect.getTransportState(device)
        print(state)
