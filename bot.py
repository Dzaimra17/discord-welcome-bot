import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

CHANNEL_NAME = "welcome"

def make_image(member, mode="welcome"):
    bg = Image.open("background.jpg").convert("RGBA")
    draw = ImageDraw.Draw(bg)

    response = requests.get(member.display_avatar.url)
    avatar = Image.open(BytesIO(response.content)).convert("RGBA")
    avatar = avatar.resize((200, 200))

    mask = Image.new("L", avatar.size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0, 200, 200), fill=255)
    avatar.putalpha(mask)

    bg.paste(avatar, (bg.width//2 - 100, 180), avatar)

    font_big = ImageFont.truetype("font.ttf", 48)
    font_small = ImageFont.truetype("font.ttf", 32)

    name = member.name
    title = "WELCOME" if mode == "welcome" else "GOODBYE"
    subtitle = f"{member.guild.name}"

    title_width = draw.textlength(title, font=font_big)
    name_width = draw.textlength(name, font=font_big)

    draw.text(
        ((bg.width - title_width)//2, 420),
        title,
        font=font_big,
        fill="#00ff99" if mode == "welcome" else "#ff5555"
    )

    draw.text(
        ((bg.width - name_width)//2, 480),
        name,
        font=font_big,
        fill="white"
    )

    draw.text(
        (bg.width//2 - 120, 550),
        subtitle,
        font=font_small,
        fill="#cccccc"
    )

    filename = "welcome.png" if mode == "welcome" else "leave.png"
    bg.save(filename)
    return filename

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name=CHANNEL_NAME)
    if channel is None:
        return

    image = make_image(member, "welcome")

    embed = discord.Embed(
        title="🎉 Selamat Datang!",
        description=f"{member.mention} bergabung ke server!",
        color=0x00ff99
    )
    embed.set_image(url=f"attachment://{image}")

    await channel.send(embed=embed, file=discord.File(image))

@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name=CHANNEL_NAME)
    if channel is None:
        return

    image = make_image(member, "leave")

    embed = discord.Embed(
        title="😢 Selamat Tinggal",
        description=f"{member.name} keluar dari server.",
        color=0xff5555
    )
    embed.set_image(url=f"attachment://{image}")

    await channel.send(embed=embed, file=discord.File(image))

bot.run("TOKEN")

