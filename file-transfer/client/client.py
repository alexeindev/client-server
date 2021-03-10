import zmq

context = zmq.Context()
#  Socket to talk to server
print("Connecting to the server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# Ask fot the action and filename
action = input("Do you want to upload or download [d/u] -> ")
filename = input("Filename -> ")


if action == 'd':
    # Download
    socket.send_multipart([b'd',
                           str(filename).encode('utf-8')])

    m = socket.recv_multipart()
    # Creates the file on the client folder and
    if m[0] == b'File exist':
        with open(filename, 'wb') as file:
            file.write(m[1])
            print('%s has been successfully downloaded ' % filename)
    else:
        print('The file %s does not exist on the server, try again' % filename)

elif action == 'u':
    # Upload
    try:
        with open(filename, 'rb') as file:
            filedata = file.read()
            socket.send_multipart(
                [b'u', str(filename).encode('utf-8'), filedata])
            m = socket.recv_multipart()
            if m[0] == b'File upload':
                print('File has been uploaded successfully! ')
    except IOError as e:
        print('The file %s does not exist on this host, try again' % filename)
else:
    print('invalid action, Try again')
