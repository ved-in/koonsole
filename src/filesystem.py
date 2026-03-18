import os

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "users")
users_current_dir = {}

def get_user_dir(user_id: str) -> str:
    path = os.path.abspath(os.path.join(BASE_DIR, user_id))
    os.makedirs(path, exist_ok=True)
    return path
    
def get_user_current_dir(user_id: str) -> str:
    user_dir = get_user_dir(user_id)
    current_dir = users_current_dir.get(user_id, user_dir) # have to use .get() method of dict cuz sometimes it just wont exist
    return current_dir
    
def set_user_dir(user_id: str, new_path: str) -> None:
    users_current_dir[user_id] = new_path