import os
from src.filesystem import get_user_dir, get_cwd, set_user_dir

def handle_cd(parts: list, user_id: str) -> str:
    user_dir = get_user_dir(user_id)
    current = get_cwd(user_id)

    if len(parts) < 2 or parts[1] == "~":
        set_user_dir(user_id, user_dir)
        return ""

    target = os.path.normpath(os.path.join(current, parts[1]))

    if not target.startswith(user_dir):
        return "cd: permission denied"
    if not os.path.exists(target):
        return f"cd: {parts[1]}: No such file or directory"
    if not os.path.isdir(target):
        return f"cd: {parts[1]}: Not a directory"

    set_user_dir(user_id, target)
    return ""