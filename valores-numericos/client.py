import zmq


context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

socket.send_multipart([b'suma', b'4', b'3'])
m = socket.recv_multipart()
print(m)
