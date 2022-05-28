import socket
target_host = "0.0.0.0"
target_port = 8080
# create a socket connection
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# let the client connect
client.connect((target_host, target_port))
# send some data
while True:
    blob = input()
    if blob == "exit()":
        break
    client.send(bytes(blob, "UTF-8"))
    # get some data
    response = client.recv(4096)
    print(response)
