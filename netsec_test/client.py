import socket
import traceback

import message
import tests
import utils
import time


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @classmethod
    def success(cls, msg):
        return cls.OKGREEN + msg + cls.ENDC

    @classmethod
    def failure(cls, msg):
        return cls.FAIL + msg + cls.ENDC

    @classmethod
    def warn(cls, msg):
        return cls.WARNING + msg + cls.ENDC


class NetsecTestClient(object):

    def __init__(self, parsed_args):
        self.debug = parsed_args.debug
        self.test_names = parsed_args.tests

        # passed in server: "./run.py --client 127.0.0.1"
        self.host = parsed_args.client
        self.port = int(parsed_args.port)

        if self.port == 0:
            raise "Must specify server port."

        self.interface = utils.Interface.from_interface_name(
            parsed_args.interface)
        self.server_interface = None

    def _send(self, msg):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Connect to server and send data
            sock.connect((self.host, self.port))
            sock.sendall(msg.serialize())

            received = sock.recv(1024)
            received = message.Message.deserialize(received)
        finally:
            sock.close()

        if self.debug:
            print "Sent:     {}".format(msg.serialize().strip())
            print "Received: {}".format(received.serialize().strip())
        return received

    def hello(self):
        msg = message.Message(command="hello", data=self.interface.as_dict())
        res = self._send(msg)
        self.server_interface = utils.Interface.from_interface_dict(
            res.data['name'], res.data['iface'])
        return res

    def _run_test(self, test_name):

        print "\n------------------------------"
        print "START TEST: {}".format(test_name)

        try:

            # Prepare Test
            test = tests.get_test(test=test_name)
            test.server_interface = self.server_interface
            test.client_interface = self.interface
            test.server_test_data = test.prepare_server()

            res = self._send(message.Message(
                command="prepare_test",
                data={"test_name": test_name,
                      "server_test_data": test.server_test_data}))

            test.client_test_data = res.data["client_test_data"]

            self._send(message.Message(
                command="run_test", data={"test_name": test_name}))
            # TODO(morgabra) Start the server test in a thread or something
            # so we can be sure it's listening when we are told to execute.
            time.sleep(2)

            # Excecute client-side test
            test.client()

            res = self._send(message.Message(
                command="get_test_results", data={"test_name": test_name}))

            msg = Colors.failure("FAILURE")
            if res.data["success"]:
                msg = Colors.success("SUCCESS")
            msg = "{} test: {} msg: {}".format(
                msg, test_name, res.data['msg'])

        except Exception as e:
            traceback.print_exc()
            msg = "{} test: {} msg: {}".format(
                Colors.failure("EXCEPTION"), test_name, str(e))

        print msg
        print "END TEST: {}".format(test_name)
        print "------------------------------"

        return msg

    def run_tests(self):

        if not self.test_names:
            self.test_names = tests.TESTS.keys()
            print Colors.warn("WARN: No tests to run, running all.")

        results = []

        for test_name in self.test_names:
            result = self._run_test(test_name)
            results.append(result)

        print "\nRESULTS"
        print "------------------------------"
        for result in results:
            print result
        print "------------------------------"
