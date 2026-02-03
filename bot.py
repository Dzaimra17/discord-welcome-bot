import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

CHANNEL_ID = 1467477719766794260
welcome_channel = None

@bot.event
async def on_ready():
    global welcome_channel
    try:
        welcome_channel = await bot.fetch_channel(CHANNEL_ID)
        print(f"Bot online sebagai {bot.user}")
        print("Channel welcome ditemukan")
    except Exception as e:
        print("Gagal mengambil channel:", e)

@bot.event
async def on_member_join(member):
    global welcome_channel

    if welcome_channel is None:
        try:
            welcome_channel = await bot.fetch_channel(CHANNEL_ID)
        except:
            print("Channel masih tidak ditemukan")
            return

    if not welcome_channel.permissions_for(member.guild.me).send_messages:
        print("Bot tidak punya izin kirim pesan")
        return

    embed = discord.Embed(
        title="👋 Selamat Datang!",
        description=f"Selamat datang {member.mention} di **{member.guild.name}**!",
        color=discord.Color.green()
    )

    embed.set_thumbnail(
        url=member.avatar.url if member.avatar else member.default_avatar.url
    )

    embed.add_field(
        name="📌 Member ke-",
        value=str(member.guild.member_count),
        inline=True
    )

    embed.set_footer(text="Selamat bergabung!")

    await welcome_channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    global welcome_channel

    if welcome_channel is None:
        try:
            welcome_channel = await bot.fetch_channel(CHANNEL_ID)
        except:
            return

    embed = discord.Embed(
        title="😢 Member Keluar",
        description=f"**{member.name}** telah keluar dari server.",
        color=discord.Color.red()
    )

    embed.set_thumbnail(
        url=member.avatar.url if member.avatar else member.default_avatar.url
    )

    embed.set_footer(text="NOOOOO 😭")

    await welcome_channel.send(embed=embed)

bot.run(os.getenv("TOKEN"))



