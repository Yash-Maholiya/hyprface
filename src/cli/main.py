import src.utils.env
import sys
import cv2

from src.camera.manager import select_camera
from src.camera.capture import start_camera
from src.camera.doctor import doctor
from src.config.config import load_config

from src.recognition.database import (
    create_user,
    save_embedding,
    load_embeddings,
    list_users,
    remove_user,
    user_exists,
)
from src.recognition.embedder import get_embedding
from src.auth.authenticator import verify_user
from src.service.client import request_auth

SAMPLES_REQUIRED = 10


def _open_camera() -> cv2.VideoCapture:
    config = load_config()
    index = config.get("camera_index")
    if index is None:
        print("No camera configured. Run: python -m src.cli.main scan")
        sys.exit(1)
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print(f"Could not open camera {index}.")
        sys.exit(1)
    return cap


def cmd_add(username: str) -> None:
    if user_exists(username):
        print(f"User '{username}' already exists. Remove them first to re-enroll.")
        return

    create_user(username)
    print("\033[32mLook into the camera...\033[0m")

    cap = _open_camera()
    collected = 0

    try:
        while collected < SAMPLES_REQUIRED:
            ret, frame = cap.read()
            if not ret:
                print("Camera read failed.")
                break

            embedding = get_embedding(frame)

            if embedding is not None:
                save_embedding(username, embedding.tolist())
                collected += 1

            cv2.waitKey(200)
    except KeyboardInterrupt:
        cap.release()
        remove_user(username)
        print("\nCancelled.")
        return

    cap.release()

    if collected == SAMPLES_REQUIRED:
        print(f"User '{username}' enrolled successfully.")
    else:
        print("Enrollment failed. Please try again.")
        remove_user(username)


def cmd_verify() -> None:
    print("\033[32mLook into the camera...\033[0m")
    result = verify_user()
    if result.success:
        print(f"Authenticated: {result.username}")
    else:
        print("Authentication failed.")


def cmd_list() -> None:
    users = list_users()
    if not users:
        print("No enrolled users.")
        return
    print("Enrolled users:\n")
    for username in users:
        embeddings = load_embeddings(username)
        print(f"  {username}  ({len(embeddings)} samples)")


def cmd_remove(username: str) -> None:
    if not user_exists(username):
        print(f"User '{username}' not found.")
        return
    confirm = input(f"Remove '{username}'? This cannot be undone. [y/N] ").strip().lower()
    if confirm == "y":
        remove_user(username)
        print(f"User '{username}' removed.")
    else:
        print("Cancelled.")


def main() -> None:
    try:
        _main()
    except KeyboardInterrupt:
        print("\nCancelled.")


def _main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: python -m src.cli.main "
            "[scan|doctor|capture|add|verify|list|remove|start|auth]"
        )
        return

    command = sys.argv[1]

    if command == "scan":
        select_camera()
    elif command == "doctor":
        doctor()
    elif command == "capture":
        config = load_config()
        index = config.get("camera_index")
        if index is None:
            print("Run scan first.")
            return
        start_camera(index)
    elif command == "add":
        username = input("Username: ").strip()
        if not username:
            print("Username cannot be empty.")
            return
        cmd_add(username)
    elif command == "verify":
        cmd_verify()
    elif command == "list":
        cmd_list()
    elif command == "remove":
        username = input("Username: ").strip()
        if not username:
            print("Username cannot be empty.")
            return
        cmd_remove(username)
    elif command == "start":
        from src.service.daemon import run
        run()
    elif command == "auth":
        success = request_auth()
        if success:
            print("Authenticated.")
        else:
            print("Authentication failed.")
    else:
        print(f"Unknown command: '{command}'")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled.")