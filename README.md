netsec-test
===========

Quick and dirty tool for testing network stuff in an semi-automated fashion.

The idea is you have two hosts that traverse some network gear, and you want to automate emitting some packets and listening for them on the other side and assert some things about them.

The client and server will share their network interface info as well as anything returned from the prepare_server/client() methods, and then proceed to run each side of the test.

There's a few terrible examples in /test.

Install Requirements
--------------------

 * scapy
 * netifaces

Example
-------

```
# start server
python base.py -s -i 'eth1'
Netsec test server listening on 0.0.0.0:36181

# run tests from client
python base.py -c <server_ip> -i 'eth1' -p 36181
```

TODO
----

* The server could be threaded and changed to be stateless as long as the client pickles and sends the test instance each time.
* The existing tests are terrible: Copy/pasted everywhere and not particularly thorough.
* You only have access to packets before/after the kernel 802.1q tags them, this is fixable so you can test the tagging.
* Tests should be refactored to automate generating packets more. (ARP poisoning is a good example, there's many permutations of invalid arp requests that could ideally be tested)
 
