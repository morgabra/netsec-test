from netifaces import AF_INET, AF_INET6, AF_LINK
import netifaces as ni

import json


class Interface(object):
    """
    #define AF_INET         2       /* Internet IP Protocol         */
    #define AF_INET6        10      /* IP version 6                 */
    #define AF_PACKET       17      /* Packet family                */
    NOTE: AF_LINK is an alias for AF_PACKET

    >>> ni.ifaddresses('eth0')
    {
        17: [
            {
                'broadcast': 'ff:ff:ff:ff:ff:ff',
                'addr': '00:02:55:7b:b2:f6'
            }
        ],
        2: [
            {
                'broadcast': '172.16.161.7',
                'netmask': '255.255.255.248',
                'addr': '172.16.161.6'
            }
        ],
        10: [
            {
                'netmask': 'ffff:ffff:ffff:ffff::',
                'addr': 'fe80::202:55ff:fe7b:b2f6%eth0'
            }
        ]
    }
    """

    def __init__(self, name, iface):
        self._name = name
        self._iface = json.loads(json.dumps(iface))

    @classmethod
    def from_interface_name(cls, name):
        iface = ni.ifaddresses(name)
        return cls(name, iface)

    @classmethod
    def from_interface_dict(cls, name, iface):
        return cls(name, iface)

    @property
    def name(self):
        return self._name

    @property
    def mac_address(self):
        return self._iface[str(AF_LINK)][0]['addr']

    @property
    def broadcast_mac_address(self):
        return self._iface[str(AF_LINK)][0].get(
            'broadcast', 'ff:ff:ff:ff:ff:ff')

    @property
    def ipv4_addresses(self):
        return [ip['addr'] for ip in self._iface[str(AF_INET)]]

    def _get_ipv4_address_info(self, ip_addr):
        for ip in self._iface[str(AF_INET)]:
            if ip['addr'] == ip_addr:
                return ip
        return {}

    def get_ipv4_netmask(self, ip_addr):
        ip_info = self._get_ipv4_address_info(ip_addr)
        return ip_info.get('netmask')

    def get_ipv4_broadcast(self, ip_addr):
        ip_info = self._get_ipv4_address_info(ip_addr)
        return ip_info.get('broadcast')

    def as_dict(self):
        return {'name': self._name, 'iface': self._iface}