import discord
from src.helpers.bot_instance import tree


@tree.command(name="example", description="An example slash command.")
async def example(interaction: discord.Interaction):
    await interaction.response.send_message("Hello World!")
