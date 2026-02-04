import socket

def is_online():
    try:
        # connect to a reliable host
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        pass
    return False
