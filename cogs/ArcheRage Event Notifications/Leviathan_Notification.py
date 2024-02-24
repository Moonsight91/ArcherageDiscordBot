import pytz
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Embed

class Leviathan_Notification(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone('US/Eastern'))

        # Define cron triggers for each notification time
        notification_times = [
            "50 19 * * mon",  # 7:50 PM on Monday
            "50 19 * * wed",  # 7:50 PM on Wednesday
            "50 19 * * fri",  # 7:50 PM on Friday
        ]

        for time in notification_times:
            self.scheduler.add_job(self.send_message, CronTrigger.from_crontab(time))

    async def send_message(self):
        channel = self.client.get_channel(1210709248011669594)  # replace with your channel ID
        if channel:
            embed = Embed(
                title="Leviathan",
                description="**Spawns in 10 Minutes**",
                color=0xff0000
            )
            embed.set_image(url="https://archeage-download1.sea.archeage.com/web/What3.PNG")
            embed.set_thumbnail(url="https://1000logos.net/wp-content/uploads/2020/09/ArcheAge-logo.png")
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Leviathan_Notification")
        self.scheduler.start()

    def cog_unload(self):
        self.scheduler.shutdown()

async def setup(client):
    await client.add_cog(Leviathan_Notification(client))
