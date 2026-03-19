import discord
from src.helpers.bot_instance import tree
import src.channel_filter as channel_filter


@tree.command(name="initialize_channel", description="Initialize channel to accept commands")
async def initialize_channel(interaction: discord.Interaction):
    channel_id = str(interaction.channel_id)
    if channel_id in channel_filter.channels_list:
        await interaction.response.send_message(
            "Channel already initialized."
        )
    else:
        channel_filter.channels_list.append(channel_id)
        channel_filter.save_channel_list()
        await interaction.response.send_message(
            "Channel Initialized.\nAny messages sent here in the format `!<command> <params>` will be treated as a command"
        )