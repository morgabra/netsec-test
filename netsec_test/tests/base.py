from scapy.all import *

import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


class NetSecTest(object):

    def __init__(self):

        self.server_test_data = None
        self.client_test_data = None

        self.client_interface = None
        self.server_interface = None

        self.results = {}

    def make_arp(self, eth_hwsrc=None, eth_hwdst=None,
                 arp_hwsrc=None, arp_psrc=None,
                 arp_hwdst=None, arp_pdst=None,
                 op=None):
        """
        By default, this will craft a gratuitous arp packet
        for the client interface.

        eth_hwsrc Ethernet MAC SRC
        eth_hwdst Ethernet MAC DST

        arp_hwsrc ARP MAC SRC
        arp_hwdst ARP MAC DST

        arp_pdst  ARP IP DST
        arp_psrc  ARP IP SRC

        op        ARP Operation ['is-at', 'who-has']
        """

        # Ethernet
        if not eth_hwsrc:
            eth_hwsrc = self.client_interface.mac_address

        if not eth_hwdst:
            eth_hwdst = self.client_interface.broadcast_mac_address

        # ARP
        if not arp_hwsrc:
            arp_hwsrc = self.client_interface.mac_address

        if not arp_hwdst:
            arp_hwdst = self.client_interface.broadcast_mac_address

        if not arp_pdst:
            arp_pdst = self.client_interface.ipv4_addresses[0]

        if not arp_psrc:
            arp_psrc = self.client_interface.ipv4_addresses[0]

        if not op:
            op = 'is-at'

        p = (Ether(dst=eth_hwdst, src=eth_hwsrc)/ARP(psrc=arp_psrc,
                                                     pdst=arp_pdst,
                                                     op=op,
                                                     hwsrc=arp_hwsrc,
                                                     hwdst=arp_hwdst))

        return p

    def prepare_server(self):
        """
        Prepare any data to send from the client to the server
        that it needs to run the server-side tests test.

        :returns: a dict that is passed to the server-side test
        """
        return {}

    def client(self):
        """
        Run the client-side test (emit packets).
        """
        pass

    def prepare_client(self):
        """
        Prepare any data to send from the server to the client that
        the client needs to run the client-side test.

        :returns: a dict that is passed to the client-side test
        """
        return {}

    def server(self):
        """
        Run the server-side test. (listen for packets)

        :returns: A dict with test reporting informaiton
        """
        pass