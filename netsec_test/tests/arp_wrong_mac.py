from scapy.all import *
import pcapy as pcap
conf.use_pcap = True

import base


class ArpWrongMacTest(base.NetSecTest):
    """
    Test that arp replies with the wrong mac are blocked.
    """

    def prepare_server(self):
        return {}

    def client(self):

        ips = self.server_interface.ipv4_addresses
        dst_ip = ips[0]

        ips = self.client_interface.ipv4_addresses
        src_ip = ips[0]

        dst_mac = self.server_interface.mac_address
        src_mac = self.client_interface.mac_address

        src_mac = src_mac.split(':')
        last = src_mac.pop()
        if last == "00":
            last = "01"
        else:
            last = "00"
        src_mac.append(last)
        src_mac = ":".join(src_mac)

        print "sending grat arp packet on iface {}".format(
            self.client_interface.name)

        try:
            p = self.make_arp(arp_hwsrc=src_mac)
            p.show()
            sendp(p, iface=self.client_interface.name)
        except OSError as e:
            pass

        print "sending arp reply packet on iface {}".format(
            self.client_interface.name)

        try:
            p = self.make_arp(eth_hwdst=dst_mac, arp_hwdst=dst_mac,
                              arp_hwsrc=src_mac, arp_psrc=src_ip,
                              arp_pdst=dst_ip, op='is-at')
            p.show()
            sendp(p, iface=self.client_interface.name)
        except OSError as e:
            pass

    def prepare_client(self):
        return {}

    def server(self):

        ips = self.client_interface.ipv4_addresses
        src_ip = ips[0]

        print "listening for grat arp from {} on iface {}".format(
            src_ip, self.server_interface.name)

        def lfilter(pkt):
            if not pkt.haslayer(ARP):
                return False
            if not pkt[ARP].psrc == src_ip:
                return False
            return True

        def callback(pkt):
            pkt.show()

        res = sniff(lfilter=lfilter, prn=callback,
                    iface=self.server_interface.name, timeout=5)

        success = False
        if len(res) == 0:
            success = True

        if success:
            self.results = {
                "success": True,
                "msg": "received no invalid arp from host {}".format(src_ip)
            }
        else:
            self.results = {
                "success": False,
                "msg": "received invalid arp from host {}".format(src_ip)
            }