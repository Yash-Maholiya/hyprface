import cv2

def start_camera(index):

    cap = cv2.VideoCapture(index)

    if not cap.isOpened():
        raise RuntimeError(f"Could not open {index}")

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        cv2.imshow(f"HyprFace Camera {index}", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()