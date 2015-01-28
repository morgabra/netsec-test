from scapy.all import *
import pcapy as pcap
conf.use_pcap = True

import base


class ArpRequestTest(base.NetSecTest):
    """
    Test that a valid ARP request is forwarded.
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

        print "sending arp request packet for {} to {} on iface {}".format(
            dst_ip, dst_mac, self.client_interface.name)

        try:
            p = self.make_arp(arp_psrc=src_ip, arp_pdst=dst_ip, op='who-has')
            p.show()
            sendp(p, iface=self.client_interface.name)
        except OSError as e:
            pass

    def prepare_client(self):
        return {}

    def server(self):

        ips = self.client_interface.ipv4_addresses
        src_ip = ips[0]

        print "listening for arp request from {} on iface {}".format(
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
        if len(res) == 1:
            success = True

        if success:
            self.results = {
                "success": True,
                "msg": "received arp request from host {}".format(src_ip)}
        else:
            self.results = {
                "success": False,
                "msg": "expected 1 arp request, got {}".format(len(res))}