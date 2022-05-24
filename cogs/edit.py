import discord
from discord.ext import commands
from discord import app_commands
import json

class ModEditor(commands.GroupCog, name="filter"):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    super().__init__()
  @app_commands.checks.has_permissions(manage_messages=True)
  @app_commands.command(name="add", description="Add a new bad word")
  async def add(self, interaction, word:str):
    data = self.bot.json
    print(data)
    if f"{interaction.guild.id}" in data:
      data[f"{interaction.guild.id}"]["bad_words"].append(word)
    else:
      data[f"{interaction.guild.id}"] = {"bad_words": [word]}
      
    self.bot.db.seek(0)
    self.bot.db.truncate()
    self.bot.db.flush()
    self.bot.db.write(json.dumps(data))
    self.bot.db.flush()
   
    await interaction.response.send_message("Succesfully added `" + word + "`")
    self.bot.json = data
    try:
      embed = discord.Embed(title="**New bad word**", description="Now `" + word + "` is a bad word", color=discord.Color.green())
      ch: discord.TextChannel = self.bot.get_channel(
      int(data[f"{interaction.guild.id}"]["log_channel"]))
      await ch.send(embed=embed)
    except Exception as e:
      print(e.__traceback__)

  @app_commands.checks.has_permissions(manage_messages=True)
  @app_commands.command(name="remove", description="Remove a bad word")
  async def remove(self, interaction, word:str):
    data = self.bot.json
    if f"{interaction.guild.id}" in data:
      pass
    else:
      return await interaction.response.send_message("This guild has no bad words")
    
    self.bot.db.seek(0)
    data[f"{interaction.guild.id}"]["bad_words"].remove(word)
    self.bot.db.truncate()
    self.bot.db.flush()
    self.bot.db.write(json.dumps(data))
    
    await interaction.response.send_message("Succesfully removed `" + word + "`")
    self.bot.db.flush()
    print(data)
    self.bot.json = data
    try:
      embed = discord.Embed(title="**Removed bad word**", description="Now `" + word + "` is not a bad word", color=discord.Color.green())
      ch: discord.TextChannel = self.bot.get_channel(
      int(data[f"{interaction.guild.id}"]["log_channel"]))
      await ch.send(embed=embed)
    except Exception as e:
      print(e.__traceback__)


async def setup(bot):
  await bot.add_cog(ModEditor(bot))
