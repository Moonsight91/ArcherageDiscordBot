import discord
from discord.ext import commands
from discord import app_commands,ui


class MyModal(ui.Modal, title="Verification Request"):
    name = ui.TextInput(label="Enter Ingame Name",
                        placeholder="John Doe",
                        custom_id="nameField",
                        style=discord.TextStyle.short)
    age = ui.TextInput(label="Enter Ingame Guild",
                       placeholder="<Playground>",
                       custom_id="ageField",
                       style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        # Acknowledge the interaction with an ephemeral message
        await interaction.response.send_message("Processing your request...", ephemeral=True)

        # Replace with your desired channel ID
        target_channel_id = 1210487753196707921

        # Try to get the channel from the guild
        target_channel = interaction.guild.get_channel(target_channel_id)

        if target_channel:
            # Send the message to the specified channel
            await target_channel.send(
                f"**{interaction.user.mention}**! Is Waiting for Verification Guild: **{self.age.value}**")
        else:
            print("Target channel not found.")


class ModalTest(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Slash Cogs Loaded")

    @app_commands.command(name="verify", description="sends verification message")
    @commands.cooldown(1, 30, commands.BucketType.guild)  # 1 use per 30 seconds per guild
    async def modal(self, interaction: discord.Interaction):
        await interaction.response.send_modal(MyModal())


async def setup(client):
    client.remove_command("help")
    await client.add_cog(ModalTest(client), guilds=[discord.Object(id="1210432912525099028")])
