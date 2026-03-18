import asyncio
import os
import shlex

from src.filesystem import get_user_dir, get_user_current_dir, set_user_dir

pending_nano = {}  # user_id:absolute filepath


def finish_nano(filepath: str, content: str) -> None:
    with open(filepath, "w") as f:
        f.write(content)


PASSTHROUGH = ["cd", "ls", "mkdir"]
HELP_TEXT = "Available commands: cd, ls, mkdir, nano"


async def handle_command(raw: str, user_id: str, username: str, message) -> str:
    try:
        parts = shlex.split(raw)
    except Exception as e:
        return f"Error while parsing command: {e}"

    if not parts:
        return ""

    cmd = parts[0]
    user_dir = get_user_dir(user_id)

    if cmd == "help":
        return HELP_TEXT
    elif cmd == "nano":
        return handle_nano(parts, user_dir, user_id)
    elif cmd == "cd":
        return handle_cd(parts, user_id)
    elif cmd in PASSTHROUGH:
        return await run_subprocess(parts, user_id)

    return f"bash: {cmd}: command not found"


def handle_nano(parts: list,
    user_dir: str,
    user_id: str) -> str:
        
        if len(parts) < 2:
            return "nano: missing filename"
            
        current_dir = get_user_current_dir(user_id)
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


async def run_subprocess(parts: list, user_id: str) -> str:
    try:
        proc = await asyncio.create_subprocess_exec(
            *parts,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=get_user_current_dir(user_id),
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=5.0)
        out = stdout.decode(errors="replace").strip()
        err = stderr.decode(errors="replace").strip()
        return out or err or "(no output)"
    except asyncio.TimeoutError:
        return "Timeout: command took too long"
    except FileNotFoundError:
        return f"bash: {parts[0]}: command not found"
    except PermissionError:
        return f"{parts[0]}: Permission denied"
    except Exception as e:
        return f"error: {e}"
        
def handle_cd(parts: list, user_id: str) -> str:
    user_dir = get_user_dir(user_id)
    current = get_user_current_dir(user_id)

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