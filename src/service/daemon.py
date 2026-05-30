import src.utils.env

import os
import sys
import socket
import signal
import threading
import cv2
import numpy as np

from src.recognition.embedder import get_embedding
from src.recognition.database import load_embeddings, list_users
from src.recognition.matcher import find_best_match
from src.config.config import load_config

SOCKET_PATH = "/tmp/hyprface.sock"
TIMEOUT = 7


def _open_camera():
    config = load_config()
    index = config.get("camera_index")
    if index is None:
        return None
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        return None
    return cap


def _attempt_auth() -> bool:
    users = list_users()
    if not users:
        return False

    all_embeddings = {u: load_embeddings(u) for u in users}
    cap = _open_camera()
    if cap is None:
        return False

    result = [False]
    done = threading.Event()

    def run():
        try:
            while not done.is_set():
                ret, frame = cap.read()
                if not ret:
                    break
                embedding = get_embedding(frame)
                if embedding is not None:
                    matched_user, _ = find_best_match(
                        np.array(embedding, dtype=np.float32),
                        all_embeddings,
                    )
                    if matched_user:
                        result[0] = True
                    done.set()
                    return
                cv2.waitKey(1)
        finally:
            cap.release()

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    thread.join(timeout=TIMEOUT)
    done.set()

    return result[0]


def _handle_client(conn: socket.socket) -> None:
    try:
        data = conn.recv(64).decode().strip()
        if data == "AUTH":
            success = _attempt_auth()
            conn.sendall(b"OK\n" if success else b"FAIL\n")
        else:
            conn.sendall(b"UNKNOWN\n")
    finally:
        conn.close()


def _cleanup(signum, frame):
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)
    sys.exit(0)


def run():
    signal.signal(signal.SIGTERM, _cleanup)
    signal.signal(signal.SIGINT, _cleanup)

    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_PATH)
    os.chmod(SOCKET_PATH, 0o600)
    server.listen(1)

    while True:
        conn, _ = server.accept()
        thread = threading.Thread(target=_handle_client, args=(conn,), daemon=True)
        thread.start()


if __name__ == "__main__":
    run()