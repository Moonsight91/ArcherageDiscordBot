import discord
from discord.ext import commands
from discord import app_commands, ui


class MyModal(ui.Modal, title="Verification Request"):
    name = ui.TextInput(label="Enter Ingame Name",
                        placeholder="John Doe",
                        custom_id="nameField",
                        style=discord.TextStyle.short)
    guild = ui.TextInput(label="Enter Ingame Guild",
                         placeholder="Guild Name",
                         custom_id="ageField",
                         style=discord.TextStyle.short)
    image_url = ui.TextInput(label="Enter Image URL for Verification",
                             placeholder="https://imgur.com/a/eMQtjcy",
                             custom_id="imageUrlField",
                             style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        # Acknowledge the interaction with an ephemeral message
        await interaction.response.send_message("Processing your request...", ephemeral=True)

        # Replace with your desired channel ID
        target_channel_id = 1210487753196707921

        # Try to get the channel from the guild
        target_channel = interaction.guild.get_channel(target_channel_id)

        if target_channel:
            # Construct the embed
            embed = discord.Embed(title="✅ Verification Request",
                                  description=f"{interaction.user.mention}",
                                  color=discord.Color.blurple())
            embed.add_field(name="Guild:", value=f"`<{self.guild.value}>`", inline=True)
            embed.add_field(name="Ingame Name:", value=f"{self.name.value}", inline=True)

            # Send the embed message to the specified channel
            embed_message = await target_channel.send(embed=embed)

            # Send the image URL as a regular message
            await target_channel.send(f"**Verification Image Url: ** ||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|||||||||||| {self.image_url.value}")

        else:
            print("Target channel not found.")


class ModalTest(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Verification_Cog_Loaded")

    @app_commands.command(name="verify", description="Sends verification message")
    @commands.cooldown(1, 30, commands.BucketType.guild)  # 1 use per 30 seconds per guild
    async def modal(self, interaction: discord.Interaction):
        await interaction.response.send_modal(MyModal())


async def setup(client):
    client.remove_command("help")
    await client.add_cog(ModalTest(client), guilds=[discord.Object(id="1210432912525099028")])
