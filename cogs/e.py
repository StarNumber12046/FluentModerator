import discord
from discord import app_commands
from discord.ext import commands
class Automod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="e", description="Say E pinging someone (beta)")
    async def e(self, interaction, user:discord.User):
        await interaction.response.send_message("E! " + user.mention)

async def setup(bot):
    await bot.add_cog(Automod(bot))
