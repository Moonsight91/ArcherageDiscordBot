import pytz
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Embed

class Red_Dragon_Notification(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone('US/Eastern'))

        # Define cron triggers for each notification time
        notification_times = [
            "20 7 * * mon,tue,wed,thu,fri,sat,sun",  # 7:20 AM every day of the week
            "50 10 * * mon,tue,wed,thu,fri,sat,sun",  # 10:50 AM every day of the week
            "50 19 * * mon,tue,wed,thu,fri,sat,sun",  # 7:50 PM every day of the week
        ]

        for time in notification_times:
            self.scheduler.add_job(self.send_message, CronTrigger.from_crontab(time))

    async def send_message(self):
        channel = self.client.get_channel(1210835743358984203)  # replace with your channel ID
        if channel:
            embed = Embed(
                title="Red Dragon",
                description="**Spawns in 10 Minutes**",
                color=0xff0000
            )
            embed.set_image(url="https://archeage-download1.sea.archeage.com/web/What3.PNG")
            embed.set_thumbnail(url="https://1000logos.net/wp-content/uploads/2020/09/ArcheAge-logo.png")
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Red_Dragon_Notification")
        self.scheduler.start()

    def cog_unload(self):
        self.scheduler.shutdown()

async def setup(client):
    await client.add_cog(Red_Dragon_Notification(client))
