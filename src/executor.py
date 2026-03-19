import shlex

from src.filesystem import get_user_dir

from src.helpers.executor import *


PASSTHROUGH = ["ls", "mkdir", "cat"]
HELP_TEXT = "Available commands: cd, ls, mkdir, nano, grep, cat, upload, get"


async def handle_command(raw: str, user_id: str, username: str, message) -> list:
    try:
        parts = shlex.split(raw)
    except Exception as e:
        return ["Send text", f"Error while parsing command: {e}"]

    if not parts:
        return ["Send text", ""]

    cmd = parts[0]
    user_dir = get_user_dir(user_id)

    if cmd == "help":
        return ["Send text", HELP_TEXT]
    elif cmd == "nano":
        return ["Send text", handle_nano(parts, user_dir, user_id)]
    elif cmd == "cd":
        return ["Send text", handle_cd(parts, user_id)]
    elif cmd == "grep":
        return ["Send text", await handle_grep(parts, user_id)]
    elif cmd == "upload":
        return ["Send text", await handle_upload(message, user_id)]
    elif cmd == "get":
        return ["Send attachment(s)", await handle_get(user_id, parts[1:])]
    elif cmd in PASSTHROUGH:
        return ["Send text", await run_subprocess(parts, user_id)]

    return ["Send text", f"bash: {cmd}: command not found"]