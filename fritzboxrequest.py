#!/usr/bin/python

from fritzconnection import FritzHosts

class FritzHostsWatch(object):

    def __init__(self, fritzpassword):
        self.fh = FritzHosts(password=fritzpassword)

    def getOnlineDevices(self):

        online_hosts = []

        for host in self.fh.get_hosts_info():
            if (host['status'] == '1'):
                online_hosts.append(host)

        return online_hosts

if __name__ == "__main__":
    pass
