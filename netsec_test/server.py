import SocketServer

import message
import utils
import tests


class MyTCPHandler(SocketServer.StreamRequestHandler):

    def _reply(self, message):

        reply = message.serialize()

        if self.server.debug:
            print "Sent:     {}".format(reply.strip())

        self.wfile.write(reply)

    def handle(self):

        # parse client message
        data = self.rfile.readline()

        if self.server.debug:
            print "Received: {}".format(data.strip())
        msg = message.Message.deserialize(data)

        if msg.command == "hello":

            # save client default interface data
            client_iface = utils.Interface.from_interface_dict(
                msg.data['name'], msg.data['iface'])
            self.server.client_interface = client_iface

            # reply with our own interface data
            self._reply(message.Message(
                command="hello", data=self.server.interface.as_dict()))

        # TODO(morgabra) keep all the test data on the client side and
        # pickle and send the whole thing each time to the server, keeping
        # the server stateless.
        if msg.command == "prepare_test":

            test_name = msg.data["test_name"]

            # set up test class instance
            test = tests.get_test(test=test_name)
            test.server_interface = self.server.interface
            test.client_interface = self.server.client_interface
            test.client_test_data = test.prepare_client()
            test.server_test_data = msg.data['server_test_data']
            self.server.test = test

            # reply with test data for client
            self._reply(message.Message(
                command="prepare_test",
                data={"test_name": test_name,
                      "client_test_data": self.server.test.client_test_data}))

        if msg.command == "run_test":

            test_name = msg.data["test_name"]

            self._reply(message.Message(
                command="run_test",
                data={"test_name": test_name}))

            # listen for packets
            self.server.test.server()

        if msg.command == "get_test_results":

            test_name = msg.data["test_name"]

            self._reply(message.Message(
                command="get_test_results",
                data=self.server.test.results))


class NetsecTestServer(SocketServer.TCPServer):

    def __init__(self, parsed_args):

        self.debug = parsed_args.debug

        self.interface = utils.Interface.from_interface_name(
            parsed_args.interface)
        self.client_interface = None

        self.test = None

        SocketServer.TCPServer.__init__(
            # TODO(morgabra) Configurable server listen host/port
            self, ("", 0), MyTCPHandler)
