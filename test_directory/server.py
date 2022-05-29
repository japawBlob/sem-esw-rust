#!/usr/bin/env python3

import asyncio
import gzip
import struct

import esw_server_pb2

words = {}


def send_message(writer, message):
    data = message.SerializeToString()
    data_size = struct.pack("!I", len(data))
    writer.write(data_size + data)


async def receive_message(reader, message_type):
    try:
        buffer = await reader.readexactly(4)
    except asyncio.IncompleteReadError as irerr:
        if len(irerr.partial) > 0:
            raise ValueError("Message length transmission incomplete")
        return None
    data_size, = struct.unpack("!I", buffer)
    try:
        data = await reader.readexactly(data_size)
    except asyncio.IncompleteReadError:
        raise ValueError("Data transmission incomplete")

    message = message_type()
    message.ParseFromString(data)
    return message


async def handle_connection(reader, writer):
    global words
    global loop

    # Client may ask multiple requests
    while True:
        request = await receive_message(reader, esw_server_pb2.Request)
        if request is None:
            break
        response = esw_server_pb2.Response()

        if request.HasField("getCount"):
            response.status = esw_server_pb2.Response.OK
            response.counter = len(words)
            words = {}
            send_message(writer, response)
        elif request.HasField("postWords"):
            text = gzip.decompress(request.postWords.data).decode("utf-8")
            for word in text.split():
                words[word] = 1
            response.status = esw_server_pb2.Response.OK
            send_message(writer, response)
        else:
            raise Exception("Request broken")


loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_connection, '', 8080, loop=loop)
server = loop.run_until_complete(coro)

print('Serving on {}'.format(server.sockets[0].getsockname()))
loop.run_forever()