from src.filesystem import get_cwd, get_user_dir
from src.helpers.executor.run_subprocess import run_subprocess

async def handle_grep(parts: list, user_id: str) -> str:
    if len(parts) < 2:
        return "grep: missing pattern"
    
    non_flags = [a for a in parts[1:] if not a.startswith("-")]
    
    if len(non_flags) < 2:
        parts = parts + [get_cwd(user_id)]
    
    print(f"DEBUG grep parts: {parts}")
    
    user_dir = get_user_dir(user_id)
    result = await run_subprocess(parts, user_id, skip_first_non_flag=True)
    result = result.replace(user_dir, "")
    
    return result