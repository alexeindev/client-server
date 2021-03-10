import os
import zmq

#  Assigning the socket
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:

    m = socket.recv_multipart()
    if m[0] == b'd':
        # Download
        try:
            with open(str("./songs/" + str(m[1].decode("utf-8"))), 'rb') as file:
                filedata = file.read()
                # Send positive response and the file
                socket.send_multipart([b'File exist', filedata])
        except IOError as e:
            # Send negative response
            socket.send_multipart([b'File not found'])

    elif m[0] == b'u':
        # Upload
        with open(m[1], 'wb') as file:
            file.write(m[2])
            # Send response
            socket.send_multipart([b'File upload'])

    elif m[0] == b'l':
        listOfFile = os.listdir(path='./songs')
        listOfFile = str(listOfFile)
        socket.send(listOfFile.encode('utf-8'))
