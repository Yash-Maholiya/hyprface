import numpy as np
from typing import Optional

THRESHOLD = 0.60


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    a = a / (np.linalg.norm(a) + 1e-6)
    b = b / (np.linalg.norm(b) + 1e-6)
    return float(np.dot(a, b))


def match_against_user(
    probe: np.ndarray,
    stored_embeddings: list[list[float]],
) -> float:
    if not stored_embeddings:
        return 0.0
    scores = [
        cosine_similarity(probe, np.array(e, dtype=np.float32))
        for e in stored_embeddings
    ]
    return max(scores)


def find_best_match(
    probe: np.ndarray,
    all_users: dict[str, list[list[float]]],
    threshold: float = THRESHOLD,
) -> tuple[Optional[str], float]:
    best_user: Optional[str] = None
    best_score: float = 0.0

    for username, embeddings in all_users.items():
        score = match_against_user(probe, embeddings)
        if score > best_score:
            best_score = score
            best_user = username

    if best_score >= threshold:
        return best_user, best_score

    return None, best_score