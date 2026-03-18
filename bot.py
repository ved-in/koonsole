import os
import sys

from dotenv import load_dotenv

from src.helpers.bot_instance import tree, bot
from src.executor import handle_command, pending_nano, finish_nano
from src.formatter import format_output

load_dotenv()



@bot.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {bot.user}")


@bot.event
async def on_message(message):
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
            filename = os.path.basename(filepath)
            await message.channel.send(f"Saved `/home/{username}/{filename}`.")
        return

    if not message.content.startswith("!"):
        return

    raw = message.content[1:].strip()
    if not raw:
        return

    result = await handle_command(raw, user_id, username, message)
    output = format_output(raw, username, result)

    await message.channel.send(output)


token: str = str(os.getenv("DISCORD_TOKEN")) #Zed keeps showing me warnings so had to do this buffonery
if token == "None":
    sys.exit("DISCORD_TOKEN not set")
bot.run(token)