import asyncio
import os
import shlex

from src.filesystem import get_user_dir

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
    elif cmd in PASSTHROUGH:
        return await run_subprocess(parts, user_dir)

    return f"bash: {cmd}: command not found"


def handle_nano(parts: list,
    user_dir: str,
    user_id: str) -> str:
        
        if len(parts) < 2:
            return "nano: missing filename"
        filepath = os.path.join(user_dir, parts[1])
        pending_nano[user_id] = filepath
        return f"nano mode for `{parts[1]}`. Send your next message wrapped in triple backticks will be used as file content. Use `.cancel` to abort."


async def run_subprocess(parts: list, user_dir: str) -> str:
    try:
        proc = await asyncio.create_subprocess_exec(
            *parts,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=user_dir,
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