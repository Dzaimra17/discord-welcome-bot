import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

# =====================
# LOAD TOKEN
# =====================
load_dotenv()
TOKEN = os.getenv("TOKEN")

# =====================
# INTENTS
# =====================
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot online sebagai {bot.user}")

# =====================
# WELCOME (JOIN)
# =====================
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="welcome")
    if not channel:
        return

    # BACKGROUND JPG
    background = Image.open("background.jpg").convert("RGBA")

    # AVATAR
    avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
    avatar_bytes = requests.get(avatar_url).content
    avatar = Image.open(BytesIO(avatar_bytes)).convert("RGBA")
    avatar = avatar.resize((200, 200))

    # MASK BULAT
    mask = Image.new("L", (200, 200), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0, 200, 200), fill=255)

    # TEMPEL AVATAR (TENGAH)
    background.paste(avatar, (412, 120), mask)

    # TULIS NAMA
    draw = ImageDraw.Draw(background)
    try:
        font = ImageFont.truetype("arial.ttf", 42)
    except:
        font = ImageFont.load_default()

    name = member.name
    text_width = draw.textlength(name, font=font)

    draw.text(
        ((1024 - text_width) / 2, 350),
        name,
        font=font,
        fill=(255, 255, 255)
    )

    # SAVE KE MEMORY
    buffer = BytesIO()
    background.save(buffer, format="PNG")
    buffer.seek(0)

    file = discord.File(buffer, filename="welcome.png")

    embed = discord.Embed(
        title="🎉 Welcome!",
        description=f"Selamat datang {member.mention} di **{member.guild.name}**",
        color=discord.Color.green()
    )
    embed.set_image(url="attachment://welcome.png")

    await channel.send(embed=embed, file=file)

# =====================
# LEAVE
# =====================
@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name="welcome")
    if not channel:
        return

    embed = discord.Embed(
        title="👋 Goodbye",
        description=f"**{member.name}** keluar dari server.",
        color=discord.Color.red()
    )

    await channel.send(embed=embed)

# =====================
# RUN BOT
# =====================
bot.run(TOKEN)
