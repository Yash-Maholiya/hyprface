from pathlib import Path
import json
import shutil
from datetime import datetime


DATA_DIR = Path("data/users")


def create_user(username: str) -> Path:
    """
    Create a user directory and profile.
    """

    user_dir = DATA_DIR / username

    if user_dir.exists():
        raise ValueError(
            f"User '{username}' already exists."
        )

    user_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    profile = {
        "username": username,
        "created_at": datetime.utcnow().isoformat(),
        "samples": 0,
        "model": "buffalo_l"
    }

    with open(
        user_dir / "profile.json",
        "w"
    ) as file:
        json.dump(
            profile,
            file,
            indent=4
        )

    with open(
        user_dir / "embeddings.json",
        "w"
    ) as file:
        json.dump(
            {"embeddings": []},
            file,
            indent=4
        )

    return user_dir


def save_embedding(
    username: str,
    embedding: list[float]
):
    """
    Append a new embedding.
    """

    user_dir = DATA_DIR / username

    if not user_dir.exists():
        raise ValueError(
            f"User '{username}' not found."
        )

    embeddings_file = (
        user_dir / "embeddings.json"
    )

    with open(
        embeddings_file,
        "r"
    ) as file:
        data = json.load(file)

    data["embeddings"].append(
        embedding
    )

    with open(
        embeddings_file,
        "w"
    ) as file:
        json.dump(
            data,
            file,
            indent=4
        )

    profile_file = (
        user_dir / "profile.json"
    )

    with open(
        profile_file,
        "r"
    ) as file:
        profile = json.load(file)

    profile["samples"] = len(
        data["embeddings"]
    )

    with open(
        profile_file,
        "w"
    ) as file:
        json.dump(
            profile,
            file,
            indent=4
        )


def load_embeddings(
    username: str
) -> list:
    """
    Load all embeddings for a user.
    """

    user_dir = DATA_DIR / username

    embeddings_file = (
        user_dir / "embeddings.json"
    )

    if not embeddings_file.exists():
        return []

    with open(
        embeddings_file,
        "r"
    ) as file:
        data = json.load(file)

    return data.get(
        "embeddings",
        []
    )


def list_users() -> list[str]:
    """
    Return all enrolled users.
    """

    if not DATA_DIR.exists():
        return []

    return sorted(
        [
            d.name
            for d in DATA_DIR.iterdir()
            if d.is_dir()
        ]
    )


def remove_user(
    username: str
):
    """
    Delete user directory.
    """

    user_dir = DATA_DIR / username

    if not user_dir.exists():
        raise ValueError(
            f"User '{username}' not found."
        )

    shutil.rmtree(user_dir)


def user_exists(
    username: str
) -> bool:
    return (
        DATA_DIR / username
    ).exists()