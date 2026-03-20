import os
import discord
import io

from src.filesystem import get_cwd

pending_nano = {}  # user_id:absolute filepath

def handle_nano(parts: list,
    user_dir: str,
    user_id: str) -> list:
        
        if len(parts) < 2:
            return ["Send text", "nano: missing filename"]
            
        current_dir = get_cwd(user_id)
        filepath = os.path.join(current_dir, parts[1])
        parent = os.path.dirname(filepath)
        if not os.path.exists(parent):
            return ["Send text", f"nano: {os.path.dirname(parts[1])}: No such directory"]
        target = os.path.normpath(filepath)
        if not target.startswith(user_dir):
            return ["Send text", "nano: permission denied"]
        pending_nano[user_id] = filepath
        if os.path.isfile(target):
            try:
                with open(target, 'r') as f:
                    content = f.read()
                file_obj = discord.File(io.BytesIO(content.encode()), filename=parts[1])
                return ["nano-file", f"nano mode for `{parts[1]}`. Your next message wrapped in triple backticks will be used as file content. Use `.cancel` to abort. Current content:", file_obj]
            except Exception as e:
                return ["nano-text", f"nano mode for `{parts[1]}`. Your next message wrapped in triple backticks will be used as file content. Use `.cancel` to abort. Error reading file: {e}", None]
        else:
            return ["nano-text", f"nano mode for `{parts[1]}`. Your next message wrapped in triple backticks will be used as file content. Use `.cancel` to abort.", None]

def finish_nano(filepath: str, content: str) -> None:
    with open(filepath, "w") as f:
        f.write(content)