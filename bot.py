import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# LOAD TOKEN DARI .env
load_dotenv()

TOKEN = os.getenv("TOKEN")

# INTENTS
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# BOT READY
@bot.event
async def on_ready():
    print(f"Bot login sebagai {bot.user}")

# MEMBER JOIN
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="welcome")
    if channel is None:
        return

    embed = discord.Embed(
        title="👋 Selamat Datang!",
        description=f"Welcome {member.mention} ke **{member.guild.name}**!",
        color=discord.Color.green()
    )
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.set_footer(text=f"Member ke-{member.guild.member_count}")

    await channel.send(embed=embed)

# MEMBER LEAVE
@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name="welcome")
    if channel is None:
        return

    embed = discord.Embed(
        title="😭 NOOOO",
        description=f"**{member.name}** keluar dari server.",
        color=discord.Color.red()
    )

    await channel.send(embed=embed)

# JALANKAN BOT (PALING BAWAH)
bot.run(TOKEN)


bot.run("MTQ2NzQ1MDQzMjg5NjEwNjU1OA.GfKtEZ.kXw3h5FoJ3Zu6rDlz7YWd0luy4z6mDSKtFTzq0")

