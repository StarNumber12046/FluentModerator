import discord
from discord.ext import commands
from discord import app_commands
import json

class Channels(commands.GroupCog, name="ignored"):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="add", description="Add a new ignored channel")
    async def add(self, interaction, channel: discord.TextChannel):
        data = self.bot.json
        print(data)
        if f"{interaction.guild.id}" in data:
            try:
                data[f"{interaction.guild.id}"]["ignored_channels"].append(f"{channel.id}")
            except:
                data[f"{interaction.guild.id}"]["ignored_channels"] = [f"{channel.id}"]
        else:
            data[f"{interaction.guild.id}"] = {
                "ignored_channels": [f"{channel.id}"]}

        self.bot.db.seek(0)
        self.bot.db.truncate()
        self.bot.db.flush()
        self.bot.db.write(json.dumps(data))
        self.bot.db.flush()

        await interaction.response.send_message("Succesfully added " + channel.mention)

        self.bot.json = data
        embed = discord.Embed(title="**New ignored channel**", description="Now " +
                              channel.mention + " is ignored", color=discord.Color.green())
        try:
            ch = self.bot.get_channel(
                int(data[f"{interaction.guild.id}"]["log_channel"]))
            await ch.send(embed=embed)
        except Exception as e:
            print(e.__traceback__)

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="remove", description="Remove an ignored channel")
    async def remove(self, interaction, channel: discord.TextChannel):
        data = self.bot.json

        if not f"{interaction.guild.id}" in data:
            return await interaction.response.send_message("This guild has no ignored channels")

        if data[f"{interaction.guild.id}"]["ignored_channels"].count(f"{channel.id}") == 0:
            return await interaction.response.send_message("This channel is not ignored")
        if data[f"{interaction.guild.id}"]["ignored_channels"] == []:
            return await interaction.response.send_message("This guild has no ignored channels")

        #remove channel id from list of ignored channels
        try:
            data[f"{interaction.guild.id}"]["ignored_channels"].remove(f"{channel.id}")
        except:
            return await interaction.response.send_message("Hm..")

        self.bot.db.seek(0)
        self.bot.db.truncate()
        self.bot.db.flush()
        self.bot.db.write(json.dumps(data))
        self.bot.db.flush()
        embed = discord.Embed(title="**Ignored channel removed**",
                              description="Now "+channel.mention + " not ignored", color=discord.Color.green())
        await interaction.response.send_message("Succesfully removed `" + channel.mention + "`")
        try:
            ch:discord.TextChannel = self.bot.get_channel(int(data[f"{interaction.guild.id}"]["log_channel"]))
            await ch.send(embed=embed)
        except Exception as e:
            print(e.__traceback__)

        self.bot.json = data

async def setup(bot):
    await bot.add_cog(Channels(bot))
