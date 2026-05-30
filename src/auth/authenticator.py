import cv2
import numpy as np

from src.config.config import load_config
from src.recognition.embedder import get_embedding
from src.recognition.database import load_embeddings, list_users
from src.recognition.matcher import find_best_match
from src.auth.result import AuthResult


def _open_camera() -> cv2.VideoCapture:
    config = load_config()
    index = config.get("camera_index")
    if index is None:
        raise RuntimeError("No camera configured.")
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera {index}.")
    return cap


def verify_user() -> AuthResult:
    users = list_users()
    if not users:
        return AuthResult(success=False)

    all_embeddings = {u: load_embeddings(u) for u in users}
    cap = _open_camera()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                return AuthResult(success=False)

            embedding = get_embedding(frame)

            if embedding is not None:
                matched_user, _ = find_best_match(
                    np.array(embedding, dtype=np.float32),
                    all_embeddings,
                )
                return AuthResult(
                    success=matched_user is not None,
                    username=matched_user,
                )

            cv2.waitKey(1)
    finally:
        cap.release()