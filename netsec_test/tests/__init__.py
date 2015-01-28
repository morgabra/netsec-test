import ping
import grat_arp
import ipsg
import arp_request
import arp_reply
import arp_wrong_ip
import arp_wrong_mac

TESTS = {
    'ping': ping.PingTest,
    'grat_arp': grat_arp.GratArpTest,
    'arp_request': arp_request.ArpRequestTest,
    'arp_reply': arp_reply.ArpReplyTest,
    'arp_wrong_ip': arp_wrong_ip.ArpWrongIPTest,
    'arp_wrong_mac': arp_wrong_mac.ArpWrongMacTest,
    'ipsg': ipsg.IPSGTest
}


def get_test(test):
    return TESTS[test]()
