import os
from src.filesystem import get_cwd

pending_nano = {}  # user_id:absolute filepath

def handle_nano(parts: list,
    user_dir: str,
    user_id: str) -> str:
        
        if len(parts) < 2:
            return "nano: missing filename"
            
        current_dir = get_cwd(user_id)
        filepath = os.path.join(current_dir, parts[1])
        parent = os.path.dirname(filepath)
        if not os.path.exists(parent):
            return f"nano: {os.path.dirname(parts[1])}: No such directory"
        target = os.path.normpath(filepath)
        if not target.startswith(user_dir):
            return "nano: permission denied"
        pending_nano[user_id] = filepath
        if os.path.isfile(target):
            try:
                with open(target, 'r') as f:
                    content = f.read()
                return f"nano mode for `{parts[1]}`. Your next message wrapped in triple backticks will be used as file content. Use `.cancel` to abort. Current content in file is:``` ```{content}"
            except Exception as e:
                return f"nano mode for `{parts[1]}`. Your next message wrapped in triple backticks will be used as file content. Use `.cancel` to abort. Error reading file:``` ```{e}"
        elif os.path.isdir(target):
            return f"{parts[1]} is not a file"
        else:
            return f"nano mode for `{parts[1]}`. Your next message wrapped in triple backticks will be used as file content. Use `.cancel` to abort."

def finish_nano(filepath: str, content: str) -> None:
    with open(filepath, "w") as f:
        f.write(content)