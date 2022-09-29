import traceback
import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import versions
import pymongo
import dotenv

dotenv.load_dotenv(".env")

class Bot(commands.Bot):

    def __init__(self, *args, **kwargs):
        """
        This function is used to connect to the MongoDB database
        """
        super().__init__(*args, **kwargs)
        self.mongo = pymongo.MongoClient(os.environ.get("MONGO_CONNECTION_STRING"))
        self.db = self.mongo.get_database("FluentModerator")

    async def on_ready(self):
        """
        It loads all the cogs in the cogs folder, and then syncs the tree.
        :return: The error message
        """
        print("Ready, starting to load cogs!")
        print("Started bot v" + versions.__version__)
        for x in os.listdir("cogs"):
            try:
                if x.endswith(".py"):
                    await self.load_extension("cogs." + x[:-3])
            except:
                __import__("traceback").print_exc()
        await self.tree.sync()
        print("Synced tree")

        @self.tree.error
        async def on_app_command_error(interaction: discord.Interaction, error):
            """
            If the error is a missing permission error, send a message saying the user is missing a
            permission. If the error is anything else, send a message saying something went wrong.
            
            :param interaction: discord.Interaction
            :type interaction: discord.Interaction
            :param error: The error that was raised
            :return: The error message that is being returned is the one that is being returned by the
            on_app_command_error event.
            """
            if isinstance(error, discord.app_commands.MissingPermissions):
                return await interaction.response.send_message(
                    f"You don't have the permissions to do that! (You are missing {error.missing_permissions[0]})"
                )
            await interaction.response.send_message(
                "Something went wrong, please try again later (note that my commands can't be used in DMS!)"
            )
            traceback.print_exc()


bot = Bot(command_prefix="..", intents=discord.Intents.all())
bot.run(os.environ.get("TOKEN"))
