import discord
from discord.ext import commands
from discord import app_commands
import json


class Settings(commands.GroupCog, name="settings"):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.checks.has_permissions(manage_guild=True)
    @app_commands.command(name="logchannel", description="Set a new log channel or leave blank to remove it")
    async def log(self, interaction, channel: discord.TextChannel = None):
        data = self.bot.json
        if channel is None:
            data[f"{interaction.guild.id}"]["log_channel"] = None
        else:
            data[f"{interaction.guild.id}"]["log_channel"] = channel.id
        self.bot.db.seek(0)
        self.bot.db.truncate()
        self.bot.db.flush()
        self.bot.db.write(json.dumps(self.bot.json))
        self.bot.db.flush()
        await interaction.response.send_message("Succesfully set the log channel to `" + str(channel) + "`")
        self.bot.json = data
async def setup(bot):
    await bot.add_cog(Settings(bot))