import os

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "users")


def get_user_dir(user_id: str) -> str:
    path = os.path.abspath(os.path.join(BASE_DIR, user_id))
    os.makedirs(path, exist_ok=True)
    return path