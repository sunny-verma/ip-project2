import time
import os
import json
from socket import *
import collections

UDP_IP = "127.0.0.1"
UDP_PORT = 12000
CLIENT_TIMEOUT = 5
MSS = 1024
number_of_server = 1
file_name = "test.txt"

sequence_number = 0
data_type = '0101010101010101'
data_packet = collections.namedtuple('data_packet', 'sequence_number checksum data_type data')

zero_field = '0000000000000000'
ack_type = '1010101010101010'
ack_packet = collections.namedtuple('ack_packet', 'sequence_number zero_field ack_type')

class Client(object):
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT

    def create_packet(self, data):
        global sequence_number, data_type
        return data_packet(sequence_number, self.calculate_checksum(data), data_type, data)

    def calculate_data_checksum(self, data):
        pass

    def send_the_file_to_server(self, file_chunk):
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        clientSocket.settimeout(CLIENT_TIMEOUT)
        addr = (self.IP, self.PORT)
        start = time.time()
        clientSocket.sendto(self.encode_json(file_chunk), addr)
        try:
            data, server = clientSocket.recvfrom(2 * MSS)
            end = time.time()
            elapsed = end - start
            print '%s %d' % (self.decode_json(data), elapsed)
        except timeout:
            print 'REQUEST TIMED OUT'
            print 'Retrying'
            clientSocket.close()
            self.send_the_file_to_server(file_chunk)

    def encode_json(self, data):
        return json.dumps(data)

    def decode_json(self, data):
        return json.loads(data)

    def calc_checksum(self, s ):
        return '%2X' % (-(sum(ord(c) for c in s) % 256) & 0xFF)

    def open_file(self):
        global  file_name
        current_dir = os.getcwd()
        abs_path = os.path.join(os.path.join(current_dir, 'file_to_read'), file_name)
        exists = os.path.exists(abs_path)
        if not exists:
            print "File doesn't exists"

        f = open(abs_path, 'rb')
        file_chunk = f.read(MSS)
        while(file_chunk):
            self.send_the_file_to_server(file_chunk)
            file_chunk = f.read(MSS)
        f.close()
        print('Done sending!!')



def main():
    global UDP_IP, UDP_PORT
    Client(UDP_IP, UDP_PORT).open_file()

if __name__ == "__main__":
    main()

