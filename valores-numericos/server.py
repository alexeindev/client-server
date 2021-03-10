import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    m = socket.recv_multipart()
    print(m)
    res = 0

    # Arithmetic Operations
    if m[0] == b'suma':
        res = int(m[1]) + int(m[2])

    elif m[0] == b'resta':
        res = int(m[1]) - int(m[2])

    elif m[0] == b'multiplicacion':
        res = int(m[1]) * int(m[2])

    elif m[0] == b'division':
        res = int(m[1]) / int(m[2])

    elif m[0] == b'modulo':
        res = int(m[1]) % int(m[2])

    elif m[0] == b'exponenciacion':
        res = int(m[1]) ** int(m[2])

    elif m[0] == b'cociente':
        res = int(m[1]) // int(m[2])

    elif m[0] == b'maximo':
        res = max(int(m[1]), int(m[2]))

    elif m[0] == b'minimo':
        res = min(int(m[1]), int(m[2]))
    else:
        res = b'Operacion invalida'
    #  Send reply back to client

    socket.send_multipart([b'resultado', str(res).encode('utf-8')])
