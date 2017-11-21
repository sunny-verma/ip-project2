import random
import json
from socket import *
import collections

UDP_IP = "127.0.0.1"
UDP_PORT = 7735
MSS = 1024

sequence_number = 0
data_type = '0101010101010101'
data_packet = collections.namedtuple('data_packet', 'sequence_number checksum data_type data')
#data_packet(sequence_number, calculate_checksum(data), DATA_TYPE, data)
ack_type = '1010101010101010'
zero_filed = '0000000000000000'
ack_packet = collections.namedtuple('ack_packet', 'sequence_number zero_field data_type')



class Server():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def rand_probability(self):
        rand = random.randint(0, 10)
        if rand >= 4:
            return True
        else:
            return False

    def create_packet(self, data):
        global  sequence_number, ack_type, zero_filed
        return ack_packet(sequence_number, zero_filed, ack_type)

    def something(self):
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind((self.ip, self.port))
        print "server1"
        while True:

            message, address = serverSocket.recvfrom(2 * MSS)
            message = self.decode_json(message)
            print message

            if self.rand_probability():
                serverSocket.sendto(self.encode_json(message), address)
            else:
                print "Not sending this one"

    def encode_json(self, data):
        return json.dumps(data)

    def decode_json(self, data):
        return json.loads(data)

def main():
    global UDP_IP, UDP_PORT
    Server(UDP_IP, UDP_PORT).something()

if __name__ == "__main__":
    main()

