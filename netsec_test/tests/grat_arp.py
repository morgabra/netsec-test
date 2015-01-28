from scapy.all import *
import pcapy as pcap
conf.use_pcap = True

import base


class GratArpTest(base.NetSecTest):
    """
    Test that a valid gratuitus ARP is forwarded.
    """

    def prepare_server(self):
        return {}

    def client(self):

        ips = self.server_interface.ipv4_addresses
        ip = ips[0]

        print "sending grat arp packet to {} on iface {}".format(
            ip, self.client_interface.name)

        try:
            p = self.make_arp()
            p.show()
            sendp(p, iface=self.client_interface.name)
        except OSError as e:
            pass

    def prepare_client(self):
        return {}

    def server(self):

        ips = self.client_interface.ipv4_addresses
        ip = ips[0]

        print "listening for grat arp from {} on iface {}".format(
            ip, self.server_interface.name)

        def lfilter(pkt):
            if not pkt.haslayer(ARP):
                return False
            if not pkt[ARP].psrc == ip:
                return False
            if not pkt[ARP].pdst == ip:
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
            self.results = {"success": True,
                            "msg": "received grat arp from host %s" % ip}
        else:
            self.results = {"success": False,
                            "msg": "expected 1 grat arp, got %s" % len(res)}