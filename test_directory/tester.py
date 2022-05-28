#!/usr/bin/env python3

import gzip
import struct
import socket
import sys

import esw_server_pb2


class Client:
    def __init__(self, host, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((host, port))

    def send_message(self, pb_message):
        data = pb_message.SerializeToString()
        data_size = struct.pack("!I", len(data))
        self.connection.sendall(data_size + data)

    def receive_message(self, messageType):
        data_size, = struct.unpack("!I", self.connection.recv(4))
        data = b''
        while data_size:
            buffer = self.connection.recv(data_size)
            if not buffer:
                raise ValueError("Data transmission incomplete")
            data += buffer
            data_size -= len(buffer)
        message = messageType()
        message.ParseFromString(data)
        return message

    def get_count(self):
        request = esw_server_pb2.Request()
        request.getCount.CopyFrom(esw_server_pb2.Request.GetCount())
        self.send_message(request)
        response = self.receive_message(esw_server_pb2.Response)
        if response.status == esw_server_pb2.Response.OK:
            return response.counter
        else:
            raise ValueError("Status not OK: " + response.errMsg)

    def post_words(self, text):
        request = esw_server_pb2.Request()
        request.postWords.CopyFrom(esw_server_pb2.Request.PostWords())
        request.postWords.data = gzip.compress(text.encode("utf-8"))
        self.send_message(request)
        response = self.receive_message(esw_server_pb2.Response)
        if response.status != esw_server_pb2.Response.OK:
            raise ValueError("Status not OK: " + response.errMsg)


host = "0.0.0.0"
port = 8123
client = Client(host, port)

print(client.get_count())
client.post_words("two words")
client.post_words("three words words")
print(client.get_count())