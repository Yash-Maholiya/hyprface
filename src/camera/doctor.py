import cv2
from src.config.config import load_config

def doctor ():

    config = load_config()

    index = config.get("camera_index")

    if index is None:
        print("No configured camera found .")
        return

    print("HyperFace Diagnostic\n")

    cap = cv2.VideoCapture(index)

    if not cap.isOpened():
        print("✖ Camera Open Failed")
        return

    print("✔ Camera Opened")

    ret,frame = cap.read()

    if not ret:
        print("✖ No frames Received")
        return

    print("✔ Frames Received")

    height, width = frame.shape[:2]

    print(f"✔ Resolution: {width}*{height}")

    print("\nStatus: Healthy")

    cap.release()