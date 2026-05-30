import numpy as np
from insightface.app import FaceAnalysis
from typing import Optional
from src.utils.env import suppress_stdout

_app: Optional[FaceAnalysis] = None


def _get_app() -> FaceAnalysis:
    global _app
    if _app is None:
        with suppress_stdout():
            _app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
            _app.prepare(ctx_id=0, det_size=(640, 640))
    return _app


def detect_face(frame: np.ndarray) -> Optional[object]:
    app = _get_app()
    faces = app.get(frame)
    if not faces:
        return None
    return max(faces, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]))


def get_embedding(frame: np.ndarray) -> Optional[np.ndarray]:
    face = detect_face(frame)
    if face is None:
        return None
    return face.embedding.astype(np.float32)