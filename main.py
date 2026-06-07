import discord
import gspread
from google.oauth2.service_account import Credentials
import re

# ===== تنظیمات =====
CHANNEL_ID = 1513119990788915290
SPREADSHEET_NAME = "Mechanici-Beny"

# ===== اتصال به گوگل شیت =====
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPES
)

gc = gspread.authorize(creds)
sheet = gc.open(SPREADSHEET_NAME).sheet1

# ===== دیسکورد =====
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


def extract_field(text, field_name):
    pattern = rf"{re.escape(field_name)}:\s*(.*)"
    match = re.search(pattern, text)
    return match.group(1).strip() if match else ""


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):

    if message.author.bot:
        return

    if message.channel.id != CHANNEL_ID:
        return

    content = message.content

    ic_name = extract_field(content, "IC Name")
    steam_name = extract_field(content, "Steam Name")
    steam_hex = extract_field(content, "Steam Hex")
    phone_number = extract_field(content, "IC Phone Number")

    if not ic_name:
        return

    sheet.append_row([
        ic_name,
        steam_name,
        steam_hex,
        phone_number
    ])

    print(f"Saved: {ic_name}")


client.run("YOUR_BOT_TOKEN")
