import discord
from discord.ext import commands
import time
import json
import os
from discord import app_commands
from datetime import datetime
from discord.utils import utcnow
from datetime import timedelta, datetime


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
    @app_commands.command(description="kisk someone")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction:discord.Interaction, user: discord.Member, *, reason: str = None):
        data = self.bot.json
        await user.kick(reason=reason)
        try:
            await user.send(
                f"😢 | You have been kicked by {interaction.user}. \nReason: {reason}"
            )
        except:
            pass
        await interaction.response.send_message(f"{user} has been kicked by {interaction.user}. \nReason: {reason}")
        embed = discord.Embed(title="**User kicked**", description=user.mention + " has been kiced", color=discord.Color.red())
        try:
            ch = self.bot.get_channel(
                int(data[f"{interaction.guild.id}"]["log_channel"]))
            await ch.send(embed=embed)
        except Exception as e:
            print(e.__traceback__)

    @app_commands.command(description="mute someone")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def mute(self, interaction:discord.Interaction, user: discord.Member, *, args:str):
        reason = "Muted by " + interaction.user.name
        data = args.split(" ")
        print(args)
        minutes = 0
        seconds = 0
        hours = 0
        days = 0

        print(data)
        for a in data:

            if a.endswith("m"):
                minutes = int(a[:-1])
            if a.endswith("s"):
                seconds = int(a[:-1])
            if a.endswith("d"):
                days = int(a[:-1])
            if a.endswith("h"):
                hours = int(a[:-1])

        timeout_until = utcnow() + timedelta(
            minutes=minutes, seconds=seconds, days=days, hours=hours
        )
        await user.edit(timed_out_until=timeout_until)
        await user.send(
            f"You are muted for {days} days {hours} hours {minutes} minutes {seconds} seconds"
        )
        await interaction.response.send_message(f"{user.mention} muted!")
        embed = discord.Embed(title="**User muted**", description=user.mention +
                              " has been muted", color=discord.Color.red())
        try:
            ch = self.bot.get_channel(
                int(self.bot.json[f"{interaction.guild.id}"]["log_channel"]))
            await ch.send(embed=embed)
        except Exception as e:
            print(e.__traceback__)


    
    @app_commands.command(description="unmute someone")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def unmute(self, interaction:discord.Interaction, user: discord.Member):
        data = self.bot.json
        await user.edit(timeout_until=None)
        await interaction.response.send_message(f"{user} is no longer muted.")
        embed = discord.Embed(title="**User unmuted**", description=user.mention +
                              " has been unmuted", color=discord.Color.green())
        try:
            ch = self.bot.get_channel(
                int(data[f"{interaction.guild.id}"]["log_channel"]))
            await ch.send(embed=embed)
        except Exception as e:
            print(e.__traceback__)


    
    @app_commands.command(description="ban someone")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction:discord.Interaction, user: discord.Member, *, reason:str=None):
        data = self.bot.json
        await user.ban(reason=reason)
        await interaction.response.send_message("You banned "+user.mention)
        try:
            await user.send(
                f"😢 | You have been banned by {interaction.user}. \nReason: {reason}"
            )
        except:
            pass
        embed = discord.Embed(title="**User banned**", description=user.mention +
                              " has been baned", color=discord.Color.green())
        try:
            ch = self.bot.get_channel(
                int(data[f"{interaction.guild.id}"]["log_channel"]))
            await ch.send(embed=embed)
        except Exception as e:
            print(e.__traceback__)

    
    @app_commands.command(description="delete some messages")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge(self, interaction:discord.Interaction, limit: int = 2):
        data = self.bot.json

        await interaction.channel.purge(limit=limit + 1)
        time.sleep(1)
        await interaction.response.send_message(f"Removed {limit} messages", delete_after=2)
        embed = discord.Embed(title="**Messages deleted**", description=f"{limit} messages hve been deleted", color=discord.Color.green())
        try:
            ch = self.bot.get_channel(
                int(data[f"{interaction.guild.id}"]["log_channel"]))
            await ch.send(embed=embed)
        except Exception as e:
            print(e.__traceback__)
    

async def setup(bot) -> None:
    await bot.add_cog(Moderation(bot))
