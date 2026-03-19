import os
from src.filesystem import get_cwd



async def handle_upload(message, user_id: str) -> str:
    if not message.attachments:
        return "No attachments found in message. Try again"
    
    path = get_cwd(user_id)
    status = ""
    for attachment in message.attachments:
        try:
            file_path = os.path.join(path, attachment.filename)
            await attachment.save(fp=file_path)
            status += f"Successfully uploaded {attachment.filename}\n"
        except Exception as _:
            status += f"Failed to upload {attachment.filename}\n"
    return status