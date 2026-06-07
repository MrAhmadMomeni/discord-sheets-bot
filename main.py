import os
import re
import discord
import gspread
from google.oauth2.service_account import Credentials

# =========================
# تنظیمات
# =========================

CHANNEL_ID = 1513119990788915290
SPREADSHEET_NAME = "Mechanici-Beny"

# =========================
# اتصال به گوگل شیت
# =========================

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

# =========================
# دیسکورد
# =========================

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# =========================
# استخراج فیلدها
# =========================

def extract_field(text, field_name):
    pattern = rf"{re.escape(field_name)}:\s*(.*)"
    match = re.search(pattern, text)
    return match.group(1).strip() if match else ""

# =========================
# ربات آماده شد
# =========================

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

# =========================
# دریافت فرم استخدام
# =========================

@client.event
async def on_message(message):

    if message.author.bot:
        return

    if message.channel.id != CHANNEL_ID:
        return

    content = message.content

    data = [
        extract_field(content, "IC Name"),
        extract_field(content, "Discord ID"),
        extract_field(content, "Steam Name"),
        extract_field(content, "Steam Hex"),
        extract_field(content, "Sen OOC"),
        extract_field(content, "Level Dar Shahr"),
        extract_field(content, "IC Phone Number"),
        extract_field(content, "Time-Play Roozane Shoma"),
        extract_field(content, "Shift Kari (Sobh-Asr-Shab)"),
        extract_field(content, "Aya Dar Organe Dige Ozv Budin? Che Organi"),
        extract_field(content, "Aya Gavahi-Name Ranandegi Darid?"),
        extract_field(content, "Aya Gavahi-Name Heli Darid?"),
        extract_field(content, "Aya Tajrobe RP kardan Darid?")
    ]

    if not data[0]:
        return

    try:
        sheet.append_row(data)

        print(f"✅ Saved: {data[0]}")

        await message.add_reaction("✅")

    except Exception as e:
        print(f"❌ Error: {e}")

# =========================
# اجرای ربات
# =========================

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    print("❌ DISCORD_TOKEN not found")
else:
    client.run(TOKEN)
