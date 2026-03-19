import os
import discord
from src.filesystem import get_cwd


async def handle_get(user_id: str, file_names):
    base_path = get_cwd(user_id)
    files = []
    for file_name in file_names:
        print(f"DEBUG: {file_name}")
        file_path = os.path.join(base_path, file_name)
        files.append(discord.File(file_path))
        print(f"DEBUG: got file {file_name}")
    print("DEBUG: returning files")
    return files