import discord
from discord.ext import commands

class EventsManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        data = self.bot.json
        if f"{message.channel.id}" in data[f'{message.guild.id}']['ignored_channels']:
            return
        if f"{message.guild.id}" in data:
            if message.author.id == self.bot.user.id:
                return
            if message.content.lower() in data[f"{message.guild.id}"]["bad_words"]:
                await message.delete()
                await message.author.send("You can't say that!")
                if data[f"{message.guild.id}"]["log_channel"] is not None:
                    embed = discord.Embed(title="Message deleted", description=f"Channel: {message.channel.mention}\nUser: {message.author.mention}\nMessage: {message.content}", color=discord.Color.red())
                    await self.bot.get_channel(int(data[f"{message.guild.id}"]["log_channel"])).send(embed=embed)
        
async def setup(bot):
    await bot.add_cog(EventsManager(bot))