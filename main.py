import asyncio
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv


from cogs.PersistentButtonViews.Set_Events_Notification import ArcheRage_Event_Notification

load_dotenv()

intents = discord.Intents.all()


class Client(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or("!"),
            owner_id=787565560677662720,
            intents=intents,
            case_insensitive=False,
            help_command=None
        )

    async def on_ready(self):
        print(f"{self.user} Has Logged In")

        # Print the number of guilds the bot is in
        guild_count = len(self.guilds)
        print(f"Connected to {guild_count} guilds:")

        # Print information for each guild
        for guild in self.guilds:
            print(f" - {guild.name} (ID: {guild.id}) - {len(guild.members)} members")

        # Print the total number of users
        user_count = sum(len(guild.members) for guild in self.guilds)
        print(f"Total users across all guilds: {user_count}")

        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.playing, name="/verify to gain access"),
            status=discord.Status.online
        )

        try:
            synced = await self.tree.sync(guild=discord.Object(id=1210432912525099028))
            print(f"{len(synced)} command(s)")
        except Exception as e:
            print(e)

    async def setup_hook(self):
        self.add_view(ArcheRage_Event_Notification())

    async def load_cogs(self, path="cogs"):
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if os.path.isdir(file_path):
                await self.load_cogs(file_path)
            elif filename.endswith(".py"):
                cog_name = file_path.replace(os.path.sep, '.')[:-3]
                await self.load_extension(cog_name)


if __name__ == "__main__":
    async def main():
        bot = Client()
        await bot.load_cogs()
        await bot.start('DISCORD_TOKEN')


    asyncio.run(main())
