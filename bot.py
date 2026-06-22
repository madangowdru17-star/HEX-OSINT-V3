# bot.py - Hex Terminal with ONLY Premium Emoji IDs (Like Your Demo)

import logging
import asyncio
import aiohttp
import socket
import json
import random
import string
import subprocess
import re
import os
import sys
from datetime import datetime, timedelta

# Telethon import
try:
    from telethon import TelegramClient, events, functions
    from telethon.tl.types import (
        KeyboardButton, KeyboardButtonRow, ReplyKeyboardMarkup,
        KeyboardButtonStyle, KeyboardButtonCallback, ReplyInlineMarkup
    )
    HAS_BUTTON_STYLE = True
except ImportError:
    print("Installing Telethon from master branch...")
    subprocess.run([sys.executable, "-m", "pip", "install", "git+https://github.com/LonamiWebs/Telethon.git"])
    from telethon import TelegramClient, events, functions
    from telethon.tl.types import (
        KeyboardButton, KeyboardButtonRow, ReplyKeyboardMarkup,
        KeyboardButtonStyle, KeyboardButtonCallback, ReplyInlineMarkup
    )
    HAS_BUTTON_STYLE = True

# --- ⚙️ CONFIGURATION ---
API_ID = int(os.environ.get('API_ID', '37996037'))
API_HASH = os.environ.get('API_HASH', '47ee9fa07b5eeb865edb3d79ada726a5')
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8687617595:AAGcgsclpi0waOdvOCYblCwJ2-g7KFVoQIc')
ADMIN_ID = int(os.environ.get('ADMIN_ID', '7898928200'))

CHANNEL_1_ID = int(os.environ.get('CHANNEL_1_ID', '-1003240507339'))
CHANNEL_2_ID = int(os.environ.get('CHANNEL_2_ID', '-1003806004135'))

LINK_1 = os.environ.get('LINK_1', 'https://t.me/+dP7xLb3AoE1jNmRl')
LINK_2 = os.environ.get('LINK_2', 'https://t.me/+9vuPcr9LJ8piODdl')

FOOTER = "\n\n⚡ ᴘᴏᴡᴇʀᴇᴅ ʙʏ @Hexh4ckerOFC"
SEP = "━━━━━━━━━━━━━━━━━━━"

# APIs
LOOKUP_API = "https://toxic-tg.vercel.app/?userid="
IFSC_API = "https://ifsc.razorpay.com/"
SHORTLINK_API = "https://link-btpass.onrender.com/bypass?key=9c44ad66b95cef8aecd7a99cfb362ce0&link="
GST_API = "https://gst-0y-vishal.vercel.app/api/gst.js?gstNumber="
PAK_API = "https://api-server-virid-two.vercel.app/number="
IND_NUM_API = "https://all-number-info-rajan-eta.vercel.app/api?number="
IND_NUM_API_3 = "https://exploitsindia.site/track/live.php?term="

VERIFY_SCRIPT = "verify_india.py"

USERS_FILE = os.path.join(os.getcwd(), "users.json")
REDEEM_FILE = os.path.join(os.getcwd(), "redeem_codes.json")
SETTINGS_FILE = os.path.join(os.getcwd(), "settings.json")

DAILY_FREE_CREDITS = 10
INVITE_CREDITS = 3
AUTO_DELETE_TIME = 60

BOT_NAME = "𝗛𝗲𝘅 𝗧𝗲𝗿𝗺𝗶𝗻𝗮𝗹"
BOT_USERNAME = "Hex_Terminal_bot"

# Premium Emoji IDs - ONLY IDs (NO EMOJIS IN TEXT)
PREMIUM_BLUE = 5258096772776991776
PREMIUM_GREEN = 5258503720928288433
PREMIUM_RED = 5258331647358540449
PREMIUM_STAR = 5258096772776991776
PREMIUM_CHECK = 5258096772776991776
PREMIUM_SPARKLE = 5258503720928288433
PREMIUM_HEART = 5258331647358540449

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Create client
client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
ADMIN_STATE = {}

# --- 💾 DATA FUNCTIONS ---

def load_json(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_json(filename, data):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except:
        pass

def get_user(user_id):
    users = load_json(USERS_FILE)
    uid = str(user_id)
    today = datetime.now().strftime("%Y-%m-%d")
    if uid not in users:
        users[uid] = {
            "credits": DAILY_FREE_CREDITS,
            "total_queries": 0,
            "daily_queries": 0,
            "last_reset": today,
            "invite_code": f"HEX-{''.join(random.choices(string.ascii_uppercase+string.digits, k=8))}",
            "invites": 0,
            "verified": False
        }
        save_json(USERS_FILE, users)
    elif users[uid].get("last_reset") != today:
        users[uid]["credits"] = DAILY_FREE_CREDITS
        users[uid]["daily_queries"] = 0
        users[uid]["last_reset"] = today
        save_json(USERS_FILE, users)
    return users[uid]

def save_user(uid, data):
    users = load_json(USERS_FILE)
    users[str(uid)] = data
    save_json(USERS_FILE, users)

def add_credits(uid, amount):
    users = load_json(USERS_FILE)
    uid = str(uid)
    if uid in users:
        users[uid]["credits"] = users[uid].get("credits", 0) + amount
        save_json(USERS_FILE, users)
        return users[uid]["credits"]
    return 0

def use_credit(uid):
    users = load_json(USERS_FILE)
    uid = str(uid)
    if uid in users and users[uid].get("credits", 0) > 0:
        users[uid]["credits"] -= 1
        users[uid]["total_queries"] = users[uid].get("total_queries", 0) + 1
        users[uid]["daily_queries"] = users[uid].get("daily_queries", 0) + 1
        save_json(USERS_FILE, users)
        return True
    return False

def process_invite(inviter_id, new_id):
    users = load_json(USERS_FILE)
    inviter = str(inviter_id)
    new = str(new_id)
    if inviter in users:
        users[inviter]["credits"] = users[inviter].get("credits", 0) + INVITE_CREDITS
        users[inviter]["invites"] = users[inviter].get("invites", 0) + 1
    if new in users:
        users[new]["credits"] = users[new].get("credits", 0) + INVITE_CREDITS
        users[new]["invited_by"] = inviter
    save_json(USERS_FILE, users)
    return INVITE_CREDITS

def generate_redeem_code(credits):
    code = f"HEX-{''.join(random.choices(string.ascii_uppercase+string.digits, k=10))}"
    codes = load_json(REDEEM_FILE)
    codes[code] = {"credits": credits, "used": False, "created": datetime.now().isoformat()}
    save_json(REDEEM_FILE, codes)
    return code

def redeem_code(uid, code):
    codes = load_json(REDEEM_FILE)
    code = code.upper().strip()
    if code not in codes:
        return False, "ɪɴᴠᴀʟɪᴅ ᴄᴏᴅᴇ"
    if codes[code].get("used"):
        return False, "ᴀʟʀᴇᴀᴅʏ ᴜꜱᴇᴅ"
    cr = codes[code]["credits"]
    codes[code]["used"] = True
    codes[code]["used_by"] = str(uid)
    save_json(REDEEM_FILE, codes)
    bal = add_credits(uid, cr)
    return True, f"+{cr} ᴄʀᴇᴅɪᴛꜱ ᴀᴅᴅᴇᴅ! ʙᴀʟᴀɴᴄᴇ: {bal}"

def get_settings():
    try:
        return load_json(SETTINGS_FILE)
    except:
        d = {
            "bypass_maintenance": False,
            "tgid_enabled": True,
            "ifsc_enabled": True,
            "bypass_enabled": True,
            "mobile_enabled": True,
            "aadhaar_enabled": True,
            "rc_enabled": True,
            "gst_enabled": True,
            "pak_enabled": True,
            "indnum_enabled": True,
            "indnum3_enabled": True,
            "maintenance_mode": False
        }
        for k in ["tgid", "ifsc", "bypass", "mobile", "aadhaar", "rc", "gst", "pak", "indnum", "indnum3"]:
            d[f"maint_msg_{k}"] = f"{k} is under maintenance."
            d[f"maint_{k}"] = False
        save_json(SETTINGS_FILE, d)
        return d

def save_settings(data):
    save_json(SETTINGS_FILE, data)

# --- 🔍 VERIFY ---

async def check_channels(uid):
    try:
        m1 = await client.get_permissions(CHANNEL_1_ID, uid)
        m2 = await client.get_permissions(CHANNEL_2_ID, uid)
        return m1.is_member and m2.is_member
    except:
        return False

# --- 🛠️ UTILS ---

async def net_ok():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except:
        return False

async def schedule_delete(msg, delay=AUTO_DELETE_TIME):
    await asyncio.sleep(delay)
    try:
        await msg.delete()
    except:
        pass

async def send_message(chat_id, text, reply_markup=None):
    return await client(functions.messages.SendMessageRequest(
        peer=chat_id,
        message=text,
        random_id=random.getrandbits(63),
        reply_markup=reply_markup
    ))

async def edit_message(msg, text, reply_markup=None):
    return await client(functions.messages.EditMessageRequest(
        peer=msg.peer_id,
        id=msg.id,
        message=text,
        reply_markup=reply_markup
    ))

async def loading_animation(msg, name):
    bars = [
        "🟩⬛⬛⬛⬛⬛⬛⬛⬛⬛",
        "🟩🟩⬛⬛⬛⬛⬛⬛⬛⬛",
        "🟩🟩🟩⬛⬛⬛⬛⬛⬛⬛",
        "🟩🟩🟩🟩⬛⬛⬛⬛⬛⬛",
        "🟩🟩🟩🟩🟩⬛⬛⬛⬛⬛",
        "🟩🟩🟩🟩🟩🟩⬛⬛⬛⬛",
        "🟩🟩🟩🟩🟩🟩🟩⬛⬛⬛",
        "🟩🟩🟩🟩🟩🟩🟩🟩⬛⬛",
        "🟩🟩🟩🟩🟩🟩🟩🟩🟩⬛",
        "🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩"
    ]
    percentages = ["0%", "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"]
    for i, bar in enumerate(bars):
        try:
            await edit_message(msg, f"<blockquote>{name}</blockquote>\n<code>{bar} {percentages[i]}</code>")
            await asyncio.sleep(0.2)
        except:
            break

def check_feature_maintenance(feature_key):
    s = get_settings()
    if s.get(f"maint_{feature_key}", False):
        return True, s.get(f"maint_msg_{feature_key}", f"{feature_key} is under maintenance.")
    return False, ""

# --- 🎨 COLORED REPLY BUTTONS (Like Your Demo) ---

def create_colored_button(text, bg_color, emoji_id):
    style = KeyboardButtonStyle(
        bg_primary=bg_color == 'primary',
        bg_success=bg_color == 'success',
        bg_danger=bg_color == 'danger',
        icon=emoji_id
    )
    return KeyboardButton(text=text, style=style)

def create_main_menu(is_admin=False, settings=None):
    if settings is None:
        settings = get_settings()
    
    rows = []
    
    # Row 1: TG ID & IFSC
    row1 = []
    if settings.get("tgid_enabled", True):
        row1.append(create_colored_button("📱 ᴛɢ ɪᴅ ➜ 📞 ɴᴜᴍʙᴇʀ 🔍", 'primary', PREMIUM_BLUE))
    if settings.get("ifsc_enabled", True):
        row1.append(create_colored_button("🏦 ɪꜰꜱᴄ ɪɴꜰᴏ➜🔎", 'success', PREMIUM_GREEN))
    if row1:
        rows.append(KeyboardButtonRow(buttons=row1))
    
    # Row 2: Link Bypass
    if settings.get("bypass_enabled", True):
        rows.append(KeyboardButtonRow(buttons=[create_colored_button("🔗 ʟɪɴᴋ ʙʏᴘᴀꜱꜱ", 'primary', PREMIUM_BLUE)]))
    
    # Row 3: Aadhaar & Mobile
    row3 = []
    if settings.get("aadhaar_enabled", True):
        row3.append(create_colored_button("🪪 ᴀᴀᴅʜᴀʀ ɪɴꜰᴏ➜👤", 'success', PREMIUM_GREEN))
    if settings.get("mobile_enabled", True):
        row3.append(create_colored_button("🇮🇳 ɪɴᴅ ɴᴜᴍʙᴇʀ ɪɴꜰᴏ➜👤", 'primary', PREMIUM_BLUE))
    if row3:
        rows.append(KeyboardButtonRow(buttons=row3))
    
    # Row 4: RC & GST
    row4 = []
    if settings.get("rc_enabled", True):
        row4.append(create_colored_button("🚘 ʀᴄ ᴅᴇᴛᴀɪʟꜱ", 'danger', PREMIUM_RED))
    if settings.get("gst_enabled", True):
        row4.append(create_colored_button("📋 ɢꜱᴛ ʟᴏᴏᴋᴜᴘ", 'success', PREMIUM_GREEN))
    if row4:
        rows.append(KeyboardButtonRow(buttons=row4))
    
    # Row 5: PAK & IND NUM
    row5 = []
    if settings.get("pak_enabled", True):
        row5.append(create_colored_button("🇵🇰 ᴘᴀᴋ ɴᴜᴍʙᴇʀ ɪɴꜰᴏ", 'danger', PREMIUM_RED))
    if settings.get("indnum_enabled", True):
        row5.append(create_colored_button("📲 ɪɴᴅ ɴᴜᴍ ɪɴꜰᴏ 𝟸", 'primary', PREMIUM_BLUE))
    if row5:
        rows.append(KeyboardButtonRow(buttons=row5))
    
    # Row 6: IND NUM 3
    if settings.get("indnum3_enabled", True):
        rows.append(KeyboardButtonRow(buttons=[create_colored_button("🇮🇳 ɪɴᴅ ɴᴜᴍʙᴇʀ ɪɴꜰᴏ 𝟹 ➜👤", 'success', PREMIUM_GREEN)]))
    
    # Row 7: Invite & Redeem
    rows.append(KeyboardButtonRow(buttons=[
        create_colored_button("👥 ɪɴᴠɪᴛᴇ & ᴇᴀʀɴ", 'primary', PREMIUM_BLUE),
        create_colored_button("🎫 ʀᴇᴅᴇᴇᴍ ᴄᴏᴅᴇ", 'success', PREMIUM_GREEN)
    ]))
    
    # Row 8: Admin Panel
    if is_admin:
        rows.append(KeyboardButtonRow(buttons=[create_colored_button("👑 ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ", 'danger', PREMIUM_RED)]))
    
    return ReplyKeyboardMarkup(rows=rows, resize=True)

# --- 📊 INDIA DATA ---

def clean_text(text):
    if not text:
        return ""
    return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', text)

def run_india_script(choice, value):
    script_path = os.path.join(os.getcwd(), VERIFY_SCRIPT)
    if not os.path.exists(script_path):
        return None
    try:
        process = subprocess.Popen(
            [sys.executable, script_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.getcwd()
        )
        stdout, stderr = process.communicate(f"{choice}\n{value}\n0\n", timeout=45)
        return stdout if stdout and len(stdout) > 20 else None
    except:
        return None

def parse_all_india_records(raw):
    raw = clean_text(raw) if raw else ""
    if not raw:
        return []
    records = []
    sections = re.split(r'={5,}|-{5,}|Record\s*\d+[:\s-]*', raw)
    for section in sections:
        section = section.strip()
        if len(section) < 10:
            continue
        record = {}
        for field, label in {
            'Name': 'ɴᴀᴍᴇ',
            "Father's Name": 'ꜰᴀᴛʜᴇʀ',
            'Mobile': 'ᴍᴏʙɪʟᴇ',
            'Address': 'ᴀᴅᴅʀᴇꜱꜱ',
            'Circle': 'ᴄɪʀᴄʟᴇ',
            'State': 'ꜱᴛᴀᴛᴇ'
        }.items():
            match = re.search(rf'{re.escape(field)}:\s*([^\n]+)', section, re.IGNORECASE)
            if match and match.group(1).strip() not in ['None', '', 'N/A', 'null']:
                record[label] = match.group(1).strip()
        if record:
            seen = set()
            unique = {}
            for k, v in record.items():
                if v not in seen:
                    seen.add(v)
                    unique[k] = v
            if unique:
                records.append(unique)
    final = []
    seen = set()
    for r in records:
        combo = tuple(sorted(r.items()))
        if combo not in seen:
            seen.add(combo)
            final.append(r)
    return final

def format_records_result(records, search_type):
    if not records:
        return "ɴᴏ ʀᴇᴄᴏʀᴅꜱ ꜰᴏᴜɴᴅ"
    title = {
        'aadhaar': 'ᴀᴀᴅʜᴀʀ',
        'mobile': 'ɪɴᴅ ɴᴜᴍʙᴇʀ',
        'vehicle': 'ᴠᴇʜɪᴄʟᴇ'
    }.get(search_type, 'ʀᴇꜱᴜʟᴛ')
    result = f"{title}\n"
    for i, record in enumerate(records, 1):
        if len(records) > 1:
            result += f"\n━━ ʀᴇᴄᴏʀᴅ {i} ━━\n"
        for key, value in record.items():
            result += f"{key}: {value}\n"
    return result

# --- 🔗 API FUNCTIONS ---

async def safe_api_fetch(session, url, timeout=20):
    for attempt in range(3):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0',
                'Accept': '*/*'
            }
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout), headers=headers, allow_redirects=True) as r:
                text = await r.text()
                if not text:
                    continue
                try:
                    return json.loads(text)
                except:
                    return {"raw_text": text} if text.strip() else None
        except:
            if attempt == 2:
                return None
            await asyncio.sleep(1)
    return None

async def chatid_lookup(session, query):
    data = await safe_api_fetch(session, f"{LOOKUP_API}{query}")
    if not data:
        return "ꜱᴇʀᴠɪᴄᴇ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ"
    if isinstance(data, dict) and not data.get("raw_text") and data.get("success"):
        d = data.get("data", data)
        if isinstance(d, dict):
            result = "ᴛᴇʟᴇɢʀᴀᴍ ɪᴅ ɪɴꜰᴏ\n"
            if d.get('chat_id') or d.get('userid'):
                result += f"ᴄʜᴀᴛ ɪᴅ: {d.get('chat_id', d.get('userid', query))}\n"
            if d.get('number'):
                result += f"ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ: {d['number']}\n"
            if d.get('name'):
                result += f"ᴘʀᴏꜰɪʟᴇ ɴᴀᴍᴇ: {d['name']}\n"
            return result
    return "ɴᴏᴛ ꜰᴏᴜɴᴅ"

async def ifsc_lookup(session, code):
    data = await safe_api_fetch(session, f"{IFSC_API}{code.upper()}")
    if not data or isinstance(data, dict) and data.get("raw_text"):
        return "ꜱᴇʀᴠɪᴄᴇ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ"
    if isinstance(data, dict):
        return (f"ʙᴀɴᴋ ɪꜰꜱᴄ ᴅᴇᴛᴀɪʟꜱ\n"
                f"ʙᴀɴᴋ ɴᴀᴍᴇ: {data.get('BANK','N/A')}\n"
                f"ʙʀᴀɴᴄʜ: {data.get('BRANCH','N/A')}\n"
                f"ɪꜰꜱᴄ ᴄᴏᴅᴇ: {data.get('IFSC',code.upper())}\n"
                f"ᴀᴅᴅʀᴇꜱꜱ: {data.get('ADDRESS','N/A')}")
    return "ɪɴᴠᴀʟɪᴅ ᴄᴏᴅᴇ"

async def bypass_lookup(session, link):
    s = get_settings()
    if s.get("bypass_maintenance", False):
        return "ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ"
    data = await safe_api_fetch(session, f"{SHORTLINK_API}{link}", timeout=20)
    if not data or isinstance(data, dict) and data.get("raw_text"):
        return "ꜱᴇʀᴠɪᴄᴇ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ"
    if isinstance(data, dict):
        r = data.get('bypassed_url') or data.get('url') or str(data)
        return f"ʟɪɴᴋ ʙʏᴘᴀꜱꜱᴇᴅ\nᴏʀɪɢɪɴᴀʟ ᴜʀʟ: {str(r)}"
    return f"ʀᴇꜱᴜʟᴛ: {str(data)}"

async def gst_lookup(session, gst_number):
    data = await safe_api_fetch(session, f"{GST_API}{gst_number.upper()}", timeout=20)
    if not data or isinstance(data, dict) and data.get("raw_text"):
        return "ꜱᴇʀᴠɪᴄᴇ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ"
    if isinstance(data, dict) and data.get("status") == "success" and data.get("data"):
        d = data["data"]
        result = "ɢꜱᴛ ʙᴜꜱɪɴᴇꜱꜱ ɪɴꜰᴏ\n"
        if d.get('TradeName'):
            result += f"ʙᴜꜱɪɴᴇꜱꜱ ɴᴀᴍᴇ: {d['TradeName']}\n"
        if d.get('Gstin'):
            result += f"ɢꜱᴛ ɴᴜᴍʙᴇʀ: {d['Gstin']}\n"
        return result
    return "ɪɴᴠᴀʟɪᴅ ɢꜱᴛ"

async def pakistan_lookup(session, number):
    try:
        data = await safe_api_fetch(session, f"{PAK_API}{number}", timeout=20)
        if not data or isinstance(data, dict) and data.get("raw_text"):
            return "ꜱᴇʀᴠɪᴄᴇ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ"
        if isinstance(data, dict) and data.get("success") and data.get("data"):
            valid = [r for r in data["data"] if isinstance(r, dict) and any(r.get(k) for k in ['name', 'number', 'cnic', 'address'])]
            if not valid:
                return "ɴᴏ ᴅᴀᴛᴀ"
            result = "ᴘᴀᴋɪꜱᴛᴀɴ ɴᴜᴍʙᴇʀ ɪɴꜰᴏ\n"
            for i, r in enumerate(valid[:3], 1):
                if len(valid) > 1:
                    result += f"\n━━ ʀᴇᴄᴏʀᴅ {i} ━━\n"
                if r.get('number'):
                    result += f"ᴘʜᴏɴᴇ: {r['number']}\n"
                if r.get('name'):
                    result += f"ɴᴀᴍᴇ: {r['name']}\n"
                if r.get('cnic'):
                    result += f"ᴄɴɪᴄ: {r['cnic']}\n"
                if r.get('address'):
                    result += f"ᴀᴅᴅʀᴇꜱꜱ: {r['address'][:200]}\n"
            return result
        return "ɴᴏ ᴅᴀᴛᴀ"
    except:
        return "ᴇʀʀᴏʀ"

async def indnum_lookup(session, number):
    for attempt in range(3):
        data = await safe_api_fetch(session, f"{IND_NUM_API}{number}", timeout=30)
        if data and isinstance(data, dict) and not data.get("raw_text") and data.get("results"):
            break
        if attempt < 2:
            await asyncio.sleep(2)
    if not data or isinstance(data, dict) and data.get("raw_text"):
        return "ꜱᴇʀᴠɪᴄᴇ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ"
    results = data.get("results", {})
    if not results:
        return "ɴᴏ ʀᴇꜱᴜʟᴛꜱ"
    result = f"ɪɴᴅɪᴀɴ ɴᴜᴍʙᴇʀ ᴀᴅᴠᴀɴᴄᴇᴅ\nɴᴜᴍʙᴇʀ: {number}\n"
    found = False
    s3 = results.get("source_3", {}).get("data", {})
    if isinstance(s3, dict):
        for k in ["SIM card", "Connection", "Mobile State", "Hometown"]:
            if s3.get(k):
                result += f"{k}: {str(s3[k])[:200]}\n"
                found = True
    s4 = results.get("source_4", {}).get("data", {})
    if isinstance(s4, dict) and s4.get("carrier"):
        result += f"ᴄᴀʀʀɪᴇʀ: {s4['carrier']}\n"
        found = True
    return result if found else "ɴᴏ ᴅᴀᴛᴀ"

async def indnum3_lookup(session, number):
    url = f"{IND_NUM_API_3}{number}"
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': '*/*'
        }
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=25), headers=headers, allow_redirects=True) as r:
            text = await r.text()
            if not text or len(text) < 20:
                return "ᴇᴍᴘᴛʏ ʀᴇꜱᴘᴏɴꜱᴇ"
            try:
                data = json.loads(text)
                if isinstance(data, dict):
                    result = f"ɪɴᴅɪᴀɴ ɴᴜᴍʙᴇʀ ᴛʀᴀᴄᴋɪɴɢ\nɴᴜᴍʙᴇʀ: {number}\n"
                    for k, v in data.items():
                        if v and str(v).strip():
                            result += f"{k}: {str(v)[:200]}\n"
                    return result
            except:
                pass
            clean = re.sub(r'<[^>]+>', '\n', text)
            lines = [l.strip() for l in clean.split('\n') if l.strip() and len(l.strip()) > 1]
            result = f"ɪɴᴅɪᴀɴ ɴᴜᴍʙᴇʀ ᴛʀᴀᴄᴋɪɴɢ\nɴᴜᴍʙᴇʀ: {number}\n"
            found = 0
            for line in lines[:20]:
                if ':' in line:
                    parts = line.split(':', 1)
                    key, val = parts[0].strip(), parts[1].strip() if len(parts) > 1 else ''
                    if val:
                        result += f"{key}: {val[:200]}\n"
                        found += 1
            if found == 0:
                result += f"ʀᴀᴡ ᴅᴀᴛᴀ: {clean[:500]}\n"
            return result
    except:
        return "ᴛɪᴍᴇᴏᴜᴛ"

# --- 👑 ADMIN ---

async def admin_panel(event):
    if event.sender_id != ADMIN_ID:
        return
    s = get_settings()
    ms = lambda key: "🔴" if s.get(f"maint_{key}") else "🟢"
    
    buttons = [
        [KeyboardButtonCallback(text="🎫 ɢᴇɴ ᴄᴏᴅᴇ", data=b"ad_gen"), KeyboardButtonCallback(text="📋 ᴄᴏᴅᴇꜱ", data=b"ad_codes")],
        [KeyboardButtonCallback(text="🎁 ᴀᴅᴅ ᴄʀ", data=b"ad_credit"), KeyboardButtonCallback(text="📢 ʙᴄᴀꜱᴛ", data=b"ad_bcast")],
        [KeyboardButtonCallback(text=f"{'🔴' if s.get('maintenance_mode') else '🟢'} ɢʟᴏʙᴀʟ", data=b"ad_maint")],
        [KeyboardButtonCallback(text=f"{'🟢' if s.get('tgid_enabled',True) else '🔴'} ᴛɢ", data=b"ad_tgid"), KeyboardButtonCallback(text=f"{ms('tgid')} ᴍ", data=b"ad_maint_tgid")],
        [KeyboardButtonCallback(text=f"{'🟢' if s.get('ifsc_enabled',True) else '🔴'} ɪꜰ", data=b"ad_ifsc"), KeyboardButtonCallback(text=f"{ms('ifsc')} ᴍ", data=b"ad_maint_ifsc")],
        [KeyboardButtonCallback(text=f"{'🟢' if s.get('bypass_enabled',True) else '🔴'} ʙʏ", data=b"ad_bypass_toggle"), KeyboardButtonCallback(text=f"{ms('bypass')} ᴍ", data=b"ad_maint_bypass")],
        [KeyboardButtonCallback(text=f"{'🟢' if s.get('mobile_enabled',True) else '🔴'} ᴍᴏ", data=b"ad_mobile"), KeyboardButtonCallback(text=f"{ms('mobile')} ᴍ", data=b"ad_maint_mobile")],
        [KeyboardButtonCallback(text=f"{'🟢' if s.get('aadhaar_enabled',True) else '🔴'} ᴀᴀ", data=b"ad_aadhaar"), KeyboardButtonCallback(text=f"{ms('aadhaar')} ᴍ", data=b"ad_maint_aadhaar")],
        [KeyboardButtonCallback(text=f"{'🟢' if s.get('rc_enabled',True) else '🔴'} ʀᴄ", data=b"ad_rc"), KeyboardButtonCallback(text=f"{ms('rc')} ᴍ", data=b"ad_maint_rc")],
        [KeyboardButtonCallback(text=f"{'🟢' if s.get('gst_enabled',True) else '🔴'} ɢꜱ", data=b"ad_gst"), KeyboardButtonCallback(text=f"{ms('gst')} ᴍ", data=b"ad_maint_gst")],
        [KeyboardButtonCallback(text=f"{'🟢' if s.get('pak_enabled',True) else '🔴'} ᴘᴀ", data=b"ad_pak"), KeyboardButtonCallback(text=f"{ms('pak')} ᴍ", data=b"ad_maint_pak")],
        [KeyboardButtonCallback(text=f"{'🟢' if s.get('indnum_enabled',True) else '🔴'} ɪɴ2", data=b"ad_indnum"), KeyboardButtonCallback(text=f"{ms('indnum')} ᴍ", data=b"ad_maint_indnum")],
        [KeyboardButtonCallback(text=f"{'🟢' if s.get('indnum3_enabled',True) else '🔴'} ɪɴ3", data=b"ad_indnum3"), KeyboardButtonCallback(text=f"{ms('indnum3')} ᴍ", data=b"ad_maint_indnum3")],
        [KeyboardButtonCallback(text="❌ ᴄʟᴏꜱᴇ", data=b"ad_close")]
    ]
    
    rows = []
    for row in buttons:
        rows.append(KeyboardButtonRow(buttons=row))
    
    markup = ReplyInlineMarkup(rows=rows)
    txt = f"ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ\nᴜꜱᴇʀꜱ: {len(load_json(USERS_FILE))} | ᴄᴏᴅᴇꜱ: {len(load_json(REDEEM_FILE))}"
    
    if hasattr(event, 'data'):
        await event.edit(txt, buttons=markup)
    else:
        await send_message(event.chat_id, txt, reply_markup=markup)

async def admin_callback(event):
    if event.sender_id != ADMIN_ID:
        await event.answer("❌", alert=True)
        return
    d = event.data.decode()
    s = get_settings()
    
    if d == "ad_close":
        await event.delete()
    elif d == "ad_codes":
        codes = load_json(REDEEM_FILE)
        txt = f"ᴄᴏᴅᴇꜱ: {len(codes)}\n"
        for c, v in list(codes.items())[-15:]:
            txt += f"{'✅' if not v.get('used') else '❌'} {c} | {v.get('credits')}cr\n"
        from telethon.tl.types import KeyboardButtonCallback, ReplyInlineMarkup, KeyboardButtonRow
        await event.edit(txt, buttons=ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text="🔄 ʙᴀᴄᴋ", data=b"ad_back")])]))
    elif d == "ad_gen":
        ADMIN_STATE[event.sender_id] = "gen"
        from telethon.tl.types import KeyboardButtonCallback, ReplyInlineMarkup, KeyboardButtonRow
        await event.edit("ᴇɴᴛᴇʀ ᴄʀᴇᴅɪᴛꜱ:\n100", buttons=ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text="🔄 ʙᴀᴄᴋ", data=b"ad_back")])]))
    elif d == "ad_credit":
        ADMIN_STATE[event.sender_id] = "credit"
        from telethon.tl.types import KeyboardButtonCallback, ReplyInlineMarkup, KeyboardButtonRow
        await event.edit("ᴇɴᴛᴇʀ ɪᴅ ᴀᴍᴏᴜɴᴛ:\n123456789 50", buttons=ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text="🔄 ʙᴀᴄᴋ", data=b"ad_back")])]))
    elif d == "ad_bcast":
        ADMIN_STATE[event.sender_id] = "bcast"
        from telethon.tl.types import KeyboardButtonCallback, ReplyInlineMarkup, KeyboardButtonRow
        await event.edit("ᴇɴᴛᴇʀ ᴍᴇꜱꜱᴀɢᴇ:", buttons=ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text="🔄 ʙᴀᴄᴋ", data=b"ad_back")])]))
    elif d == "ad_maint":
        s["maintenance_mode"] = not s.get("maintenance_mode", False)
        save_settings(s)
        await event.answer(f"Global: {'ON' if s['maintenance_mode'] else 'OFF'}", alert=True)
        await admin_panel(event)
    elif d.startswith("ad_maint_"):
        f = d.replace("ad_maint_", "")
        s[f"maint_{f}"] = not s.get(f"maint_{f}", False)
        save_settings(s)
        await event.answer(f"{f}: {'ON' if s[f'maint_{f}'] else 'OFF'}", alert=True)
        await admin_panel(event)
    elif d.startswith("ad_"):
        toggle_map = {
            "ad_tgid": "tgid_enabled",
            "ad_ifsc": "ifsc_enabled",
            "ad_bypass_toggle": "bypass_enabled",
            "ad_mobile": "mobile_enabled",
            "ad_aadhaar": "aadhaar_enabled",
            "ad_rc": "rc_enabled",
            "ad_gst": "gst_enabled",
            "ad_pak": "pak_enabled",
            "ad_indnum": "indnum_enabled",
            "ad_indnum3": "indnum3_enabled"
        }
        if d in toggle_map:
            k = toggle_map[d]
            s[k] = not s.get(k, True)
            save_settings(s)
            await event.answer(f"{k}: {'ON' if s[k] else 'OFF'}", alert=True)
        await admin_panel(event)
    elif d == "ad_back":
        await admin_panel(event)
    await event.answer()

# --- 🚀 HANDLERS ---

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    try:
        uid = event.sender_id
        args = event.message.message.split()
        if len(args) > 1 and args[1].startswith("HEX-"):
            users = load_json(USERS_FILE)
            for inviter, data in users.items():
                if data.get("invite_code") == args[1] and inviter != str(uid):
                    cr = process_invite(inviter, uid)
                    try:
                        await send_message(int(inviter), f"+{cr} ᴄʀᴇᴅɪᴛꜱ! ɴᴇᴡ ᴜꜱᴇʀ ᴊᴏɪɴᴇᴅ!")
                    except:
                        pass
                    break
        
        user = get_user(uid)
        if not user.get("verified"):
            if await check_channels(uid):
                user["verified"] = True
                save_user(uid, user)
                await main_menu(event)
                return
            await show_verification_page(event)
            return
        await main_menu(event)
    except Exception as e:
        logger.error(f"Start: {e}")

async def show_verification_page(event):
    try:
        txt = (
            f"{BOT_NAME}\n"
            f"@{BOT_USERNAME}\n\n"
            f"ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ʀᴇQᴜɪʀᴇᴅ\n"
            f"ᴊᴏɪɴ ʙᴏᴛʜ ᴄʜᴀɴɴᴇʟꜱ ᴛᴏ ᴜɴʟᴏᴄᴋ\n\n"
            f"ɢᴜɪᴅᴇʟɪɴᴇꜱ:\n"
            f"• ᴇᴅᴜᴄᴀᴛɪᴏɴᴀʟ ᴘᴜʀᴘᴏꜱᴇꜱ ᴏɴʟʏ\n"
            f"• ᴜꜱᴇ ᴏɴ ʏᴏᴜʀ ᴏᴡɴ ᴅᴀᴛᴀ\n"
            f"• ʀᴇꜱᴘᴇᴄᴛ ᴘʀɪᴠᴀᴄʏ ʟᴀᴡꜱ\n\n"
            f"+{DAILY_FREE_CREDITS} ᴅᴀɪʟʏ\n"
            f"+{INVITE_CREDITS} ᴘᴇʀ ɪɴᴠɪᴛᴇ\n"
            f"{AUTO_DELETE_TIME}ꜱ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ\n\n"
            f"ᴏᴡɴᴇʀ: @Hexh4ckerOFC\n"
            f"ᴍɪꜱᴜꜱᴇ ᴍᴀʏ ʟᴇᴀᴅ ᴛᴏ ʟᴇɢᴀʟ ᴀᴄᴛɪᴏɴ"
        )
        
        button1 = KeyboardButtonCallback(
            text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ 𝟷",
            data=b"url1"
        )
        button2 = KeyboardButtonCallback(
            text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ 𝟸",
            data=b"url2"
        )
        button3 = KeyboardButtonCallback(
            text="ɪ'ᴠᴇ ᴊᴏɪɴᴇᴅ - ᴠᴇʀɪꜰʏ",
            data=b"verify"
        )
        
        markup = ReplyInlineMarkup(rows=[
            KeyboardButtonRow(buttons=[button1]),
            KeyboardButtonRow(buttons=[button2]),
            KeyboardButtonRow(buttons=[button3])
        ])
        
        await send_message(event.chat_id, txt, reply_markup=markup)
    except Exception as e:
        logger.error(f"Verification page: {e}")

@client.on(events.CallbackQuery(data=b"verify"))
async def verify_cb(event):
    try:
        uid = event.sender_id
        if await check_channels(uid):
            user = get_user(uid)
            user["verified"] = True
            save_user(uid, user)
            await event.answer("✅ ᴠᴇʀɪꜰɪᴇᴅ!", alert=True)
            try:
                await event.delete()
            except:
                pass
            await main_menu(event)
        else:
            await event.answer("❌ ᴊᴏɪɴ ʙᴏᴛʜ ᴄʜᴀɴɴᴇʟꜱ ꜰɪʀꜱᴛ!", alert=True)
    except Exception as e:
        logger.error(f"Verify callback error: {e}")
        await event.answer("❌ ᴇʀʀᴏʀ, ᴛʀʏ ᴀɢᴀɪɴ", alert=True)

@client.on(events.CallbackQuery)
async def handle_url_callback(event):
    if event.data == b"url1":
        await event.answer(f"📢 ᴊᴏɪɴ: {LINK_1}", alert=True)
    elif event.data == b"url2":
        await event.answer(f"📢 ᴊᴏɪɴ: {LINK_2}", alert=True)

async def main_menu(event):
    is_admin = event.sender_id == ADMIN_ID
    user = get_user(event.sender_id)
    s = get_settings()
    
    markup = create_main_menu(is_admin, s)
    cr = user.get("credits", 0)
    
    txt = (
        f"ᴘʀᴇᴍɪᴜᴍ ʜᴜʙ\n"
        f"ᴡᴇʟᴄᴏᴍᴇ ʙᴀᴄᴋ, {event.sender.first_name}\n\n"
        f"ʏᴏᴜʀ ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ:\n"
        f"ᴄʀᴇᴅɪᴛꜱ: {cr}\n"
        f"Qᴜᴇʀɪᴇꜱ: {user.get('total_queries',0)}\n"
        f"ɪɴᴠɪᴛᴇꜱ: {user.get('invites',0)}\n\n"
        f"ʀᴇᴡᴀʀᴅꜱ:\n"
        f"+{DAILY_FREE_CREDITS} ᴅᴀɪʟʏ ꜰʀᴇᴇ\n"
        f"+{INVITE_CREDITS} ᴘᴇʀ ɪɴᴠɪᴛᴇ\n"
        f"{AUTO_DELETE_TIME}ꜱ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ\n\n"
        f"ꜱᴇʟᴇᴄᴛ ᴀ ꜱᴇʀᴠɪᴄᴇ ʙᴇʟᴏᴡ"
    )
    
    msg = await send_message(event.chat_id, txt, reply_markup=markup)
    asyncio.create_task(schedule_delete(msg, AUTO_DELETE_TIME))

@client.on(events.NewMessage)
async def msg_handler(event):
    try:
        uid = event.sender_id
        txt = event.message.message.strip()
        
        if not txt:
            return
            
        asyncio.create_task(schedule_delete(event.message, AUTO_DELETE_TIME))
        s = get_settings()
        
        if s.get("maintenance_mode", False) and uid != ADMIN_ID:
            m = await send_message(event.chat_id, "Under maintenance")
            asyncio.create_task(schedule_delete(m))
            return
        
        if uid == ADMIN_ID and uid in ADMIN_STATE:
            state = ADMIN_STATE.pop(uid)
            if state == "gen":
                try:
                    cr = int(txt)
                    code = generate_redeem_code(cr)
                    msg = await send_message(event.chat_id, f"{code} | {cr}cr")
                except:
                    msg = await send_message(event.chat_id, "Number")
                asyncio.create_task(schedule_delete(msg))
                return
            elif state == "credit":
                p = txt.split()
                if len(p) >= 2:
                    bal = add_credits(p[0], int(p[1]))
                    msg = await send_message(event.chat_id, f"+{p[1]} | {bal}")
                else:
                    msg = await send_message(event.chat_id, "Format: ID AMOUNT")
                asyncio.create_task(schedule_delete(msg))
                return
            elif state == "bcast":
                users = load_json(USERS_FILE)
                cnt = 0
                for u in users:
                    try:
                        await send_message(int(u), txt)
                        cnt += 1
                    except:
                        pass
                msg = await send_message(event.chat_id, f"Sent: {cnt}")
                asyncio.create_task(schedule_delete(msg))
                return
        
        user = get_user(uid)
        if not user.get("verified"):
            if await check_channels(uid):
                user["verified"] = True
                save_user(uid, user)
                await main_menu(event)
                return
            else:
                await show_verification_page(event)
                return
        
        if txt == "👑 ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ":
            await admin_panel(event)
            return
        
        if hasattr(event, 'redeem_mode') and event.redeem_mode:
            event.redeem_mode = False
            if txt.upper().startswith("HEX-"):
                success, msg = redeem_code(uid, txt)
                m = await send_message(event.chat_id, msg)
            else:
                m = await send_message(event.chat_id, "Invalid code!")
            asyncio.create_task(schedule_delete(m))
            return
        
        mode = None
        feature_map = {
            "📱 ᴛɢ ɪᴅ ➜ 📞 ɴᴜᴍʙᴇʀ 🔍": ("TG", "tgid"),
            "🏦 ɪꜰꜱᴄ ɪɴꜰᴏ➜🔎": ("IFSC", "ifsc"),
            "🔗 ʟɪɴᴋ ʙʏᴘᴀꜱꜱ": ("SHORTLINK", "bypass"),
            "🇮🇳 ɪɴᴅ ɴᴜᴍʙᴇʀ ɪɴꜰᴏ➜👤": ("MOBILE", "mobile"),
            "🪪 ᴀᴀᴅʜᴀʀ ɪɴꜰᴏ➜👤": ("AADHAAR", "aadhaar"),
            "🚘 ʀᴄ ᴅᴇᴛᴀɪʟꜱ": ("VEHICLE", "rc"),
            "📋 ɢꜱᴛ ʟᴏᴏᴋᴜᴘ": ("GST", "gst"),
            "🇵🇰 ᴘᴀᴋ ɴᴜᴍʙᴇʀ ɪɴꜰᴏ": ("PAK", "pak"),
            "📲 ɪɴᴅ ɴᴜᴍ ɪɴꜰᴏ 𝟸": ("INDNUM", "indnum"),
            "🇮🇳 ɪɴᴅ ɴᴜᴍʙᴇʀ ɪɴꜰᴏ 𝟹 ➜👤": ("INDNUM3", "indnum3"),
            "👥 ɪɴᴠɪᴛᴇ & ᴇᴀʀɴ": ("INVITE", None),
            "🎫 ʀᴇᴅᴇᴇᴍ ᴄᴏᴅᴇ": ("REDEEM", None)
        }
        
        if txt in feature_map:
            mode, feature = feature_map[txt]
            
            if mode == "INVITE":
                user = get_user(uid)
                bot_username = BOT_USERNAME
                link = f"https://t.me/{bot_username}?start={user['invite_code']}"
                m = await send_message(event.chat_id, f"ɪɴᴠɪᴛᴇ (+{INVITE_CREDITS}ᴄʀ)\n{link}")
                asyncio.create_task(schedule_delete(m, 120))
                return
            elif mode == "REDEEM":
                event.redeem_mode = True
                m = await send_message(event.chat_id, "ᴇɴᴛᴇʀ ʀᴇᴅᴇᴇᴍ ᴄᴏᴅᴇ:\nHEX-XXXXXXXXXX")
                asyncio.create_task(schedule_delete(m, 30))
                return
            
            if feature and not s.get(f"{feature}_enabled", True):
                m = await send_message(event.chat_id, "Disabled")
                asyncio.create_task(schedule_delete(m))
                return
            
            if feature:
                maint, msg = check_feature_maintenance(feature)
                if maint:
                    m = await send_message(event.chat_id, msg)
                    asyncio.create_task(schedule_delete(m))
                    return
            
            event.mode = mode
            prompts = {
                "TG": "ᴛᴇʟᴇɢʀᴀᴍ ɪᴅ ᴛᴏ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ\n7123181749, 6884112825",
                "IFSC": "ʙᴀɴᴋ ɪꜰꜱᴄ ᴄᴏᴅᴇ\nSBIN0001234, HDFC0001234",
                "SHORTLINK": "ʟɪɴᴋ ʙʏᴘᴀꜱꜱ\nhttps://indianshortner.in/xxxx",
                "MOBILE": "ɪɴᴅɪᴀɴ ᴍᴏʙɪʟᴇ ɴᴜᴍʙᴇʀ\n9876543210, 8123456789",
                "AADHAAR": "ᴀᴀᴅʜᴀʀ ɴᴜᴍʙᴇʀ\n123456789012",
                "VEHICLE": "ᴠᴇʜɪᴄʟᴇ ɴᴜᴍʙᴇʀ\nKA01AB3256, DL1CX1234",
                "GST": "ɢꜱᴛ ɴᴜᴍʙᴇʀ\n19BOKPS7056D1ZI",
                "PAK": "ᴘᴀᴋɪꜱᴛᴀɴ ɴᴜᴍʙᴇʀ\n923078750447",
                "INDNUM": "ᴀᴅᴠᴀɴᴄᴇᴅ ɴᴜᴍʙᴇʀ\n6363016966, 9876543210",
                "INDNUM3": "ɪɴᴅɪᴀɴ ɴᴜᴍʙᴇʀ ᴛʀᴀᴄᴋɪɴɢ\n6363016966, 9876543210"
            }
            if mode in prompts:
                m = await send_message(event.chat_id, prompts[mode])
                asyncio.create_task(schedule_delete(m))
            return
        
        if hasattr(event, 'mode') and event.mode:
            mode = event.mode
            if txt.upper().startswith("HEX-"):
                success, msg = redeem_code(uid, txt)
                m = await send_message(event.chat_id, msg)
                asyncio.create_task(schedule_delete(m))
                event.mode = None
                return
            
            user = get_user(uid)
            if user.get("credits", 0) <= 0:
                m = await send_message(event.chat_id, "No credits! +10 daily | +3 invite")
                asyncio.create_task(schedule_delete(m))
                event.mode = None
                return
            
            await run_query(event, mode, txt)
            event.mode = None
        
    except Exception as e:
        logger.error(f"Msg: {e}")

async def run_query(event, mode, query):
    if not await net_ok():
        m = await send_message(event.chat_id, "No internet")
        asyncio.create_task(schedule_delete(m))
        return
    
    names = {
        'TG': 'PHONE',
        'IFSC': 'BANK',
        'SHORTLINK': 'LINK',
        'AADHAAR': 'CARD',
        'MOBILE': 'INDIA',
        'VEHICLE': 'CAR',
        'GST': 'CARD',
        'PAK': 'PAK',
        'INDNUM': 'PHONE2',
        'INDNUM3': 'INDIA'
    }
    
    st = await send_message(event.chat_id, "ꜱᴇᴀʀᴄʜɪɴɢ...")
    lt = asyncio.create_task(loading_animation(st, names.get(mode, '')))
    credit_deducted = False
    
    try:
        if mode in ['AADHAAR', 'MOBILE', 'VEHICLE']:
            choice_map = {'AADHAAR': '2', 'MOBILE': '1', 'VEHICLE': '4'}
            raw = run_india_script(choice_map[mode], query)
            if raw:
                records = parse_all_india_records(raw)
                result = format_records_result(records, {'AADHAAR': 'aadhaar', 'MOBILE': 'mobile', 'VEHICLE': 'vehicle'}[mode])
                if records and "ɴᴏ" not in str(result):
                    use_credit(event.sender_id)
                    credit_deducted = True
            else:
                result = "Script failed"
        else:
            async with aiohttp.ClientSession() as s:
                if mode == 'TG':
                    result = await chatid_lookup(s, query)
                elif mode == 'IFSC':
                    result = await ifsc_lookup(s, query)
                elif mode == 'SHORTLINK':
                    result = await bypass_lookup(s, query)
                elif mode == 'GST':
                    result = await gst_lookup(s, query)
                elif mode == 'PAK':
                    result = await pakistan_lookup(s, query)
                elif mode == 'INDNUM':
                    result = await indnum_lookup(s, query)
                elif mode == 'INDNUM3':
                    result = await indnum3_lookup(s, query)
                else:
                    result = "ERROR"
            
            if result and "ɴᴏ" not in str(result) and "unavailable" not in str(result).lower():
                use_credit(event.sender_id)
                credit_deducted = True
        
        lt.cancel()
        try:
            await lt
        except asyncio.CancelledError:
            pass
        
        user = get_user(event.sender_id)
        final = f"{result}\n{SEP}\n{'ᴄʀ: '+str(user.get('credits',0)) if credit_deducted else 'ɴᴏ ᴄʀ ᴅᴇᴅᴜᴄᴛᴇᴅ'} | {AUTO_DELETE_TIME}ꜱ{DISCLAIMER}{FOOTER}"
        sent = await edit_message(st, final)
        asyncio.create_task(schedule_delete(sent))
    except Exception as e:
        lt.cancel()
        logger.error(f"Query: {e}")
        try:
            await edit_message(st, f"ᴇʀʀᴏʀ{FOOTER}")
        except:
            pass

# --- 🚀 START ---

async def main():
    print("Hex Terminal Premium (Telethon Version)...")
    print("ONLY Premium Emoji IDs in Buttons - NO Emojis in Text")
    print("Like your demo code!")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "requests", "beautifulsoup4"], capture_output=True, timeout=30)
    except:
        pass
    
    await client.start(bot_token=BOT_TOKEN)
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
    except RuntimeError as e:
        if "event loop" in str(e).lower():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(main())
        else:
            raise
    except KeyboardInterrupt:
        print("Bot stopped by user")
    except Exception as e:
        print(f"Error: {e}")