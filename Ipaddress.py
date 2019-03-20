import socket


def getIP():
    x = str(socket.gethostbyname(socket.gethostname()))
    return x
