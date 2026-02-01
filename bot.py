import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

CHANNEL_ID = 1467477719766794260  # GANTI DENGAN ID CHANNEL WELCOME

@bot.event
async def on_ready():
    print(f"Bot online sebagai {bot.user}")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(CHANNEL_ID)

    embed = discord.Embed(
        title="👋 Selamat Datang!",
        description=f"Selamat datang {member.mention} di **{member.guild.name}**!",
        color=discord.Color.green()
    )
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.add_field(name="📌 Member ke-", value=f"{member.guild.member_count}", inline=True)
    embed.set_footer(text="Selamat bergabung!")

    await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1467477719766794260)

    embed = discord.Embed(
        title="😢 Member Keluar",
        description=f"**{member.name}** telah keluar dari server.",
        color=discord.Color.red()
    )
    embed.set_footer(text="Semoga bertemu lagi!")

    await channel.send(embed=embed)

bot.run("MTQ2NzQ1MDQzMjg5NjEwNjU1OA.GfKtEZ.kXw3h5FoJ3Zu6rDlz7YWd0luy4z6mDSKtFTzq0")
