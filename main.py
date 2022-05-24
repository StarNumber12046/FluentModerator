import discord
from discord.ext import commands
from discord import app_commands
import json
import config.bot as botcfg
import config.db as dbcfg
import os
import versions

class Bot(commands.Bot):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.db = open(dbcfg.filename, "r")
    dump = self.db.read()
    self.db.close()
    self.db = open(dbcfg.filename, "w")
    self.db.write(dump)
    self.db.flush()
    self.json = json.loads(dump)

  async def on_ready(self):
      print("Ready, starting to load cogs!")
      print("Started bot v"+versions.__version__)
      for x in os.listdir("cogs"):
          try:
              if x.endswith(".py"):
                  await self.load_extension("cogs."+x[:-3])
          except:
              __import__("traceback").print_exc()
      await self.tree.sync()
      print("Synced tree")
      @self.tree.error
      async def on_app_command_error(
        interaction: discord.Interaction,
        error
      ):
        if isinstance(error, discord.app_commands.MissingPermissions):
          return await interaction.response.send_message(f"You don't have the permissions to do that! (You are missing {error.missing_permissions[0]})")
        await interaction.response.send_message(
          "Something went wrong, please try again later (note that my commands can't be used in DMS!)"
        )
    
bot = Bot(command_prefix="..", intents=discord.Intents.all())
bot.run(botcfg.token)
