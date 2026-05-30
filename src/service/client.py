import src.utils.env

import socket
import sys

SOCKET_PATH = "/tmp/hyprface.sock"


def request_auth() -> bool:
    try:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(SOCKET_PATH)
        client.sendall(b"AUTH\n")
        response = client.recv(64).decode().strip()
        client.close()
        return response == "OK"
    except Exception:
        return False


if __name__ == "__main__":
    success = request_auth()
    if success:
        sys.exit(0)
    sys.exit(1)