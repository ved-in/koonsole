import os
import sys

from dotenv import load_dotenv

from src.helpers.bot_instance import tree, bot
from src.executor import handle_command
from src.helpers.executor.nano import pending_nano, finish_nano
from src.formatter import format_output
from src.filesystem import get_user_dir, load_cwds
import src.channel_filter as channel_filter


# This will show unused imports, but its needed. Discord.py handles the commands through decorators
import src.slash_commands.set_channel
import src.slash_commands.forget_channel

load_dotenv()


@bot.event
async def on_ready():
    await tree.sync()
    load_cwds()
    channel_filter.load_channel_list()
    print(f"Logged in as {bot.user}")


@bot.event
async def on_message(message):
    if str(message.channel.id) in channel_filter.channels_list:        
        if message.author.bot:
            return
    
        user_id = str(message.author.id)
        username = message.author.name
    
        if user_id in pending_nano:
            if message.content.strip() == ".cancel":
                del pending_nano[user_id]
                await message.channel.send("Cancelled.")
                return
            if message.content.strip().startswith("```"):
                filepath = pending_nano[user_id]
                finish_nano(filepath, message.content.strip().strip("```"))
                del pending_nano[user_id]
                relative = os.path.relpath(filepath, get_user_dir(user_id))
                path = f"{relative}"
                await message.channel.send(f"Saved `/home/{username}/{path}`.")
            return
    
        if not message.content.startswith("!"):
            return
    
        raw = message.content[1:].strip()
        if not raw:
            return
    
        result = await handle_command(raw, user_id, username, message)
        if result[0] == "Send text":
            output = format_output(raw, username, result[1])
            await message.channel.send(output)
        elif result[0] == "Send attachment(s)":
            files = result[1]
            print("DEBUG: sending files")
            await message.channel.send(content="", files=files)


token: str = str(os.getenv("DISCORD_TOKEN")) #Zed keeps showing me warnings so had to do this buffoonery
if token == "None":
    sys.exit("DISCORD_TOKEN not set")
bot.run(token)