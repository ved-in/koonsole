import os
from dotenv import load_dotenv

load_dotenv()

from src.helpers.bot_instance import tree, bot
import src.commands


@bot.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {bot.user}")


token = os.getenv("DISCORD_TOKEN")
bot.run(token)
