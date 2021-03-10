import zmq
import os

#  Assigning the socket
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:

    m = socket.recv_multipart()
    if m[0] == b'd':
        print('Entro a descargar')
        # Download
        try:
            with open(m[1], 'rb') as file:
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
        listOfFile = os.listdir(path='.')
        print(listOfFile)
        socket.send_multipart([str(listOfFile).encode('utf-8')])
