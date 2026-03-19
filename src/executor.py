import shlex

from src.filesystem import get_user_dir

from src.helpers.executor.nano import handle_nano
from src.helpers.executor.cd import handle_cd
from src.helpers.executor.grep import handle_grep
from src.helpers.executor.upload import handle_upload
from src.helpers.executor.run_subprocess import run_subprocess


PASSTHROUGH = ["ls", "mkdir", "cat"]
HELP_TEXT = "Available commands: cd, ls, mkdir, nano, grep, cat, upload"


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
    elif cmd == "grep":
        return await handle_grep(parts, user_id)
    elif cmd == "upload":
        return await handle_upload(message, user_id)
    elif cmd in PASSTHROUGH:
        return await run_subprocess(parts, user_id)

    return f"bash: {cmd}: command not found"