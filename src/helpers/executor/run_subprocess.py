import asyncio
import os
from src.filesystem import get_user_dir, get_cwd

FILE_ARG_COMMANDS = [
    "cat", "ls", "mkdir", "rm", "cp", "mv", "chmod", "ln", "touch", "head", "tail", "grep", "find", "du", "stat", "tree", "wc", "file", "diff", "cd", "nano"
]

async def run_subprocess(parts: list, user_id: str, username: str, skip_first_non_flag=False) -> str:
    user_dir = get_user_dir(user_id)
    cwd = get_cwd(user_id)
    sanitized = [parts[0]]
    skipped = False
    
    if parts[0] not in FILE_ARG_COMMANDS:
        sanitized = parts
    else:
        for part in parts[1:]:
            if part.startswith("-"):
                sanitized.append(part)
                continue
            if skip_first_non_flag and not skipped:
                sanitized.append(part)  # pass pattern through untouched
                skipped = True
                continue
            resolved = os.path.abspath(os.path.join(cwd, part))
            if not resolved.startswith(user_dir):
                return f"{parts[0]}: permission denied"
            sanitized.append(resolved)

    print(f"DEBUG sanitized: {sanitized}")
        
    try:
        proc = await asyncio.create_subprocess_exec(
            *sanitized,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=get_cwd(user_id),
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=5.0)
        out = stdout.decode(errors="replace").strip()
        err = stderr.decode(errors="replace").strip()
        result = out or err or ""
        
        result = result.replace(get_user_dir(user_id), f"/home/{username}")
        result = result.replace(os.getlogin(), username)
        
        return result
    except asyncio.TimeoutError:
        return "Timeout: command took too long"
    except FileNotFoundError:
        return f"bash: {parts[0]}: command not found"
    except PermissionError:
        return f"{parts[0]}: Permission denied"
    except Exception as e:
        return f"error: {e}"