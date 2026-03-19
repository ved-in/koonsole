import discord
from src.helpers.bot_instance import tree
import src.channel_filter as channel_filter


@tree.command(name="uninitialize_channel", description="Forget previously initialized channels")
async def uninitialize_channel(interaction: discord.Interaction):
    channel_id = str(interaction.channel_id)
    if channel_id not in channel_filter.channels_list:
        await interaction.response.send_message(
            """Channel was not initialized... No changes were done"""
        )
    else:
        channel_filter.channels_list.remove(channel_id)
        channel_filter.save_channel_list()
        await interaction.response.send_message(
            """Channel Uninitialized.
Any messages sent here now onwards will be ignored by the bot"""
        )