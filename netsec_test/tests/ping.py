from scapy.all import *

import base


class PingTest(base.NetSecTest):
    """
    Test that a valid ICMP echo request is forwarded.
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

        print "sending ping packet from {} to {} on iface {}".format(
            src_ip, dst_ip, self.client_interface.name)

        try:
            p = (Ether(dst=dst_mac, src=src_mac) /
                 IP(dst=dst_ip, src=src_ip) /
                 ICMP())
            p.show()
            sendp(p, iface=self.client_interface.name)
        except OSError as e:
            pass

    def prepare_client(self):
        return {}

    def server(self):

        ips = self.server_interface.ipv4_addresses
        dst_ip = ips[0]

        ips = self.client_interface.ipv4_addresses
        src_ip = ips[0]

        dst_mac = self.server_interface.mac_address
        src_mac = self.client_interface.mac_address

        print "listening for ping packet from {} on iface {}".format(
            src_ip, self.server_interface.name)

        lfilter = lambda x: x.haslayer(ICMP) and x[IP].src == src_ip

        def callback(pkt):
            pkt.show()

        res = sniff(lfilter=lfilter, prn=callback, timeout=5, count=1,
                    iface=self.server_interface.name)

        success = True
        msg = "Received ping packet from host: {}".format(src_ip)

        if len(res) != 1:
            success = False
            msg = "Received no ping packet.".format(len(res))

        self.results = {"success": success,
                        "msg": msg}