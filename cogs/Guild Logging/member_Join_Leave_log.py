import discord
from discord.ext import commands
import sqlite3
from datetime import datetime, timedelta

class MemberLogger(commands.Cog):
    def __init__(self, client, db_file):
        self.bot = client
        self.db_file = db_file

        # Connect to SQLite database
        self.conn = sqlite3.connect(self.db_file)
        self.c = self.conn.cursor()

        # Create tables if not exists
        self.c.execute('''CREATE TABLE IF NOT EXISTS JoinLeaveLog (
                         guild_id TEXT PRIMARY KEY,
                         log_channel_id TEXT
                         )''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS JoinLeaveEvents (
                         guild_id TEXT,
                         event_type TEXT,
                         user_id TEXT,
                         timestamp TEXT
                         )''')
        self.conn.commit()

    def save_log_channel_id(self, guild_id, log_channel_id):
        self.c.execute("INSERT OR REPLACE INTO JoinLeaveLog (guild_id, log_channel_id) VALUES (?, ?)", (guild_id, log_channel_id))
        self.conn.commit()

    def get_log_channel_id(self, guild_id):
        self.c.execute("SELECT log_channel_id FROM JoinLeaveLog WHERE guild_id = ?", (guild_id,))
        row = self.c.fetchone()
        return row[0] if row else None

    async def send_embed(self, channel, title, description, footer_text, color):
        embed = discord.Embed(
            title=title,
            description=description,
            color=color
        )
        embed.set_footer(text=footer_text)
        await channel.send(embed=embed)

    @commands.command(name="set-log-channel", description="Sets the log channel for member join and leave events")
    @commands.has_permissions(administrator=True)
    async def set_log_channel(self, ctx, channel: discord.TextChannel):
        guild_id = str(ctx.guild.id)
        self.save_log_channel_id(guild_id, str(channel.id))
        await ctx.send(f"Log channel set to {channel.mention} for member join and leave events.")

    @commands.command(name="reset-log-channel", description="Resets the log channel for member join and leave events")
    @commands.has_permissions(administrator=True)
    async def reset_log_channel(self, ctx):
        guild_id = str(ctx.guild.id)
        self.save_log_channel_id(guild_id, None)
        await ctx.send("Log channel for member join and leave events has been reset.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        log_channel_id = self.get_log_channel_id(str(member.guild.id))
        if log_channel_id:
            log_channel = self.bot.get_channel(int(log_channel_id))
            if log_channel:
                join_date = member.joined_at.strftime('%Y-%m-%d %H:%M:%S')
                footer_text = f"Joined: {join_date} UTC"
                await self.send_embed(log_channel, "Member Joined", f"{member.mention} has joined the server.", footer_text, discord.Color.green())

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        log_channel_id = self.get_log_channel_id(str(member.guild.id))
        if log_channel_id:
            log_channel = self.bot.get_channel(int(log_channel_id))
            if log_channel:
                leave_date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                footer_text = f"Left: {leave_date} UTC"
                await self.send_embed(log_channel, "Member Left", f"{member.mention} has left the server.", footer_text, discord.Color.red())


async def setup(client):
    db_file = 'discord_bot.db'
    await client.add_cog(MemberLogger(client, db_file))
