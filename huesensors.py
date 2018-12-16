#!/usr/bin/python

import requests
import json
import time

class HueMotionWatch(object):

    def __init__(self, huebridge, hueuser):
        self.huebridge = huebridge
        self.hueuser = hueuser


    def getMotionSensorData(self):

        motion_data = {}

        try:
            response = requests.get("http://" + self.huebridge + "/api/" + self.hueuser + "/sensors")

            if response.status_code == 200:
                json_data = json.loads(response.content)

                for sensor in json_data:
                    if json_data[sensor]['type'] == "ZLLPresence":

                        try:
                            last_updated =      time.mktime(
                                                    time.strptime(
                                                        json_data[sensor]['state']['lastupdated'], "%Y-%m-%dT%H:%M:%S"
                                                    )
                                                )

                            if (time.mktime(time.gmtime()) - last_updated) <= 600:
                                motion_data[json_data[sensor]['uniqueid']] = True

                        except ValueError as e:
                            print(e)

        except requests.ConnectionError as e:
            print(e)

        except requests.HTTPError as e:
            print(e)

        return motion_data

if __name__ == "__main__":
    motionwatch = HueMotionWatch('192.168.178.44', 'D567Sx3i5gjhWpX9pDge4MYPRYrFFaq7Dfo1SnaF')
    print(motionwatch.getMotionSensorData())
