import os
import json

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "users")
users_current_dir = {}

CWD_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "cwds.json")

def load_cwds():
    global users_current_dir
    if os.path.exists(CWD_FILE):
        try:
            with open(CWD_FILE, "r") as f:
                users_current_dir = json.load(f)
        except Exception:
            users_current_dir = {}

def save_cwds():
    with open(CWD_FILE, "w") as f:
        json.dump(users_current_dir, f)

def get_user_dir(user_id: str) -> str:
    path = os.path.abspath(os.path.join(BASE_DIR, user_id))
    os.makedirs(path, exist_ok=True)
    return path
    
def get_cwd(user_id: str) -> str:
    user_dir = get_user_dir(user_id)
    current_dir = users_current_dir.get(user_id, user_dir) # have to use .get() method of dict cuz sometimes it just wont exist
    return current_dir
    
def set_user_dir(user_id: str, new_path: str) -> None:
    users_current_dir[user_id] = new_path
    save_cwds()