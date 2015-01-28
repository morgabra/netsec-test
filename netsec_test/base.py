import argparse

import server
import client


class NetsecTest(object):
    """Small wrapper around argparse for shared script options."""

    def __init__(self):

        self._parser = argparse.ArgumentParser('Utility for testing network '
                                               'security features.')

        self._parsed_args = None

        mode = self._parser.add_mutually_exclusive_group(required=True)
        mode.add_argument('--client', '-c',
                          help='Run tests as client')
        mode.add_argument('--server', '-s', action='store_true',
                          help='Start a test server')

        self._parser.add_argument('--interface', '-i',
                                  help='Interface to run tests on.',
                                  required=True)

        self._parser.add_argument('--debug', '-d', action='store_true',
                                  help='Debug logging.', default=False)

        self._parser.add_argument('--port', '-p',
                                  help='Server listen port.', default=0)

        self._parser.add_argument('tests', nargs='*',
                                  help='Test names to run.')

    def run_server(self):
        serv = server.NetsecTestServer(self._parsed_args)
        print "Netsec test server listening on {}:{}".format(
            *serv.server_address)
        serv.serve_forever()

    def run_client(self):
        c = client.NetsecTestClient(self._parsed_args)
        c.hello()
        c.run_tests()

    def run(self):
        self._parsed_args = self._parser.parse_args()
        if self._parsed_args.server:
            self.run_server()
        else:
            self.run_client()

if __name__ == '__main__':
    c = NetsecTest()
    c.run()
