# bot.py - Telethon Version with Fixed Event Loop

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

# Fix: Proper Telethon import with event loop handling
try:
    from telethon import TelegramClient, events, functions
    from telethon.tl import types
    from telethon.tl.types import (
        KeyboardButton, KeyboardButtonRow, ReplyKeyboardMarkup,
        Message
    )
    # Try to import KeyboardButtonStyle (only available in master branch)
    try:
        from telethon.tl.types import KeyboardButtonStyle
        HAS_BUTTON_STYLE = True
    except ImportError:
        HAS_BUTTON_STYLE = False
        # Create a dummy class if not available
        class KeyboardButtonStyle:
            def __init__(self, bg_primary=False, bg_success=False, bg_danger=False, icon=None):
                self.bg_primary = bg_primary
                self.bg_success = bg_success
                self.bg_danger = bg_danger
                self.icon = icon
        types.KeyboardButtonStyle = KeyboardButtonStyle
except ImportError as e:
    print(f"Import error: {e}")
    print("Installing Telethon from master branch...")
    subprocess.run([sys.executable, "-m", "pip", "install", "git+https://github.com/LonamiWebs/Telethon.git"])
    # Retry import after installation
    from telethon import TelegramClient, events, functions
    from telethon.tl import types
    from telethon.tl.types import (
        KeyboardButton, KeyboardButtonRow, ReplyKeyboardMarkup,
        Message, KeyboardButtonStyle
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

FOOTER = "\n\n<b>⚡ ᴘᴏᴡᴇʀᴇᴅ ʙʏ @Hexh4ckerOFC</b>"
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

# --- PREMIUM EMOJI IDs ---
EMOJI_WARN = 6267039884016358504
EMOJI_CHECK = 6267008582294705964
EMOJI_CROSS = 6267000941547885720
EMOJI_LOCK = 5316522278056399236
EMOJI_CROWN = 6267128480601741166
EMOJI_DIAMOND = 6264791387032523779
EMOJI_STAR = 6266969287638913443
EMOJI_GIFT = 5203996991054432397
EMOJI_FIRE = 6264785189394717307
EMOJI_SEARCH = 5231012545799666522
EMOJI_PHONE = 5947494995798789024
EMOJI_BANK = 5264895611517300926
EMOJI_LINK = 5271604874419647061
EMOJI_CAR = 5253752975997803460
EMOJI_CARD = 5260561650213220533
EMOJI_USER = 5249053508681883137
EMOJI_INDIA = 6284779941489812433
EMOJI_PAK = 5913705895375672082
EMOJI_PHONE2 = 5406809207947142040
EMOJI_INVITE = 5244933196230972438
EMOJI_TICKET = 5285515895534278367
EMOJI_CREDIT = 6267068789146260253
EMOJI_REFRESH = 5375338737028841420
EMOJI_CLOCK = 5382194935057372936
EMOJI_BOLT = 6284971355297290197
EMOJI_GREEN = 5386367538735104399
EMOJI_BLACK = 5116476703002068797
EMOJI_SPARKLE = 5467683093693354332
EMOJI_ROCKET = 5195033767969839232
EMOJI_TOOLS = 5462921117423384478
EMOJI_DISABLED = 5373165973203348165
EMOJI_FATHER = 6147864334077794239
EMOJI_LOCATION = 5391032818111363540
EMOJI_HOME = 5280955052582785391
EMOJI_STATE = 5388927107315283144
EMOJI_NETWORK = 5321141214735508486
EMOJI_SIGNAL = 6147892053796725336
EMOJI_SIM = 5800717980266403037
EMOJI_CHART = 6093382540784046658

# Color button premium emoji IDs
EMOJI_PRIMARY = 5258096772776991776
EMOJI_SUCCESS = 5258503720928288433
EMOJI_DANGER = 5258331647358540449

# Premium emoji helper
def PE(eid, fallback):
    return f'<tg-emoji emoji-id="{eid}">{fallback}</tg-emoji>'

# Pre-computed premium emoji strings
PE_WARN = PE(EMOJI_WARN, "⚠️")
PE_CHECK = PE(EMOJI_CHECK, "✅")
PE_CROSS = PE(EMOJI_CROSS, "❌")
PE_LOCK = PE(EMOJI_LOCK, "🔒")
PE_CROWN = PE(EMOJI_CROWN, "👑")
PE_DIAMOND = PE(EMOJI_DIAMOND, "💎")
PE_STAR = PE(EMOJI_STAR, "⭐")
PE_GIFT = PE(EMOJI_GIFT, "🎁")
PE_FIRE = PE(EMOJI_FIRE, "🔥")
PE_SEARCH = PE(EMOJI_SEARCH, "🔍")
PE_PHONE = PE(EMOJI_PHONE, "📞")
PE_BANK = PE(EMOJI_BANK, "🏦")
PE_LINK = PE(EMOJI_LINK, "🔗")
PE_CAR = PE(EMOJI_CAR, "🚘")
PE_CARD = PE(EMOJI_CARD, "🪪")
PE_USER = PE(EMOJI_USER, "👤")
PE_INDIA = PE(EMOJI_INDIA, "🇮🇳")
PE_PAK = PE(EMOJI_PAK, "🇵🇰")
PE_PHONE2 = PE(EMOJI_PHONE2, "📲")
PE_INVITE = PE(EMOJI_INVITE, "👥")
PE_TICKET = PE(EMOJI_TICKET, "🎫")
PE_CREDIT = PE(EMOJI_CREDIT, "💰")
PE_REFRESH = PE(EMOJI_REFRESH, "🔄")
PE_CLOCK = PE(EMOJI_CLOCK, "⏱")
PE_BOLT = PE(EMOJI_BOLT, "⚡")
PE_GREEN = PE(EMOJI_GREEN, "🟩")
PE_BLACK = PE(EMOJI_BLACK, "⬛")
PE_SPARKLE = PE(EMOJI_SPARKLE, "✨")
PE_ROCKET = PE(EMOJI_ROCKET, "🚀")
PE_TOOLS = PE(EMOJI_TOOLS, "🛠️")
PE_DISABLED = PE(EMOJI_DISABLED, "📴")
PE_FATHER = PE(EMOJI_FATHER, "👨")
PE_LOCATION = PE(EMOJI_LOCATION, "📍")
PE_HOME = PE(EMOJI_HOME, "🏠")
PE_STATE = PE(EMOJI_STATE, "🏛")
PE_NETWORK = PE(EMOJI_NETWORK, "📡")
PE_SIGNAL = PE(EMOJI_SIGNAL, "📶")
PE_SIM = PE(EMOJI_SIM, "💳")
PE_CHART = PE(EMOJI_CHART, "📊")
PE_PRIMARY = PE(EMOJI_PRIMARY, "🔵")
PE_SUCCESS = PE(EMOJI_SUCCESS, "🟢")
PE_DANGER = PE(EMOJI_DANGER, "🔴")

DISCLAIMER = f"\n\n<b>{PE_WARN} ᴅɪꜱᴄʟᴀɪᴍᴇʀ:</b>\n<i>ᴇᴅᴜᴄᴀᴛɪᴏɴᴀʟ ᴘᴜʀᴘᴏꜱᴇꜱ ᴏɴʟʏ. ᴜꜱᴇ ʀᴇꜱᴘᴏɴꜱɪʙʟʏ.</i>"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Create client with proper event loop
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
        return False, f"{PE_CROSS} ɪɴᴠᴀʟɪᴅ ᴄᴏᴅᴇ"
    if codes[code].get("used"):
        return False, f"{PE_CROSS} ᴀʟʀᴇᴀᴅʏ ᴜꜱᴇᴅ"
    cr = codes[code]["credits"]
    codes[code]["used"] = True
    codes[code]["used_by"] = str(uid)
    save_json(REDEEM_FILE, codes)
    bal = add_credits(uid, cr)
    return True, f"{PE_CHECK} +{cr} ᴄʀᴇᴅɪᴛꜱ ᴀᴅᴅᴇᴅ!\n{PE_CREDIT} ʙᴀʟᴀɴᴄᴇ: {bal}"

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
            d[f"maint_msg_{k}"] = f"{PE_TOOLS} {k} is under maintenance."
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
            await edit_message(msg, f"<blockquote>{PE_BOLT} {name}</blockquote>\n<code>{bar} {percentages[i]}</code>")
            await asyncio.sleep(0.2)
        except:
            break

def check_feature_maintenance(feature_key):
    s = get_settings()
    if s.get(f"maint_{feature_key}", False):
        return True, s.get(f"maint_msg_{feature_key}", f"{PE_TOOLS} Under maintenance.")
    return False, ""

# --- 🎨 COLORED REPLY BUTTONS ---

def create_colored_button(text, bg_color, emoji_id):
    if HAS_BUTTON_STYLE:
        # Use real KeyboardButtonStyle if available
        style = KeyboardButtonStyle(
            bg_primary=bg_color == 'primary',
            bg_success=bg_color == 'success',
            bg_danger=bg_color == 'danger',
            icon=emoji_id
        )
        return KeyboardButton(text=text, style=style)
    else:
        # Fallback: return normal button without style (Telethon stable version)
        return KeyboardButton(text=text)

def create_main_menu(is_admin=False, settings=None):
    if settings is None:
        settings = get_settings()
    
    rows = []
    
    # Row 1: TG ID & IFSC
    row1 = []
    if settings.get("tgid_enabled", True):
        row1.append(create_colored_button("📱 ᴛɢ ɪᴅ ➜ 📞 ɴᴜᴍʙᴇʀ 🔍", 'primary', EMOJI_PRIMARY))
    if settings.get("ifsc_enabled", True):
        row1.append(create_colored_button("🏦 ɪꜰꜱᴄ ɪɴꜰᴏ➜🔎", 'success', EMOJI_SUCCESS))
    if row1:
        rows.append(KeyboardButtonRow(buttons=row1))
    
    # Row 2: Link Bypass
    if settings.get("bypass_enabled", True):
        rows.append(KeyboardButtonRow(buttons=[create_colored_button("🔗 ʟɪɴᴋ ʙʏᴘᴀꜱꜱ", 'primary', EMOJI_PRIMARY)]))
    
    # Row 3: Aadhaar & Mobile
    row3 = []
    if settings.get("aadhaar_enabled", True):
        row3.append(create_colored_button("🪪 ᴀᴀᴅʜᴀʀ ɪɴꜰᴏ➜👤", 'success', EMOJI_SUCCESS))
    if settings.get("mobile_enabled", True):
        row3.append(create_colored_button("🇮🇳 ɪɴᴅ ɴᴜᴍʙᴇʀ ɪɴꜰᴏ➜👤", 'primary', EMOJI_PRIMARY))
    if row3:
        rows.append(KeyboardButtonRow(buttons=row3))
    
    # Row 4: RC & GST
    row4 = []
    if settings.get("rc_enabled", True):
        row4.append(create_colored_button("🚘 ʀᴄ ᴅᴇᴛᴀɪʟꜱ", 'danger', EMOJI_DANGER))
    if settings.get("gst_enabled", True):
        row4.append(create_colored_button("📋 ɢꜱᴛ ʟᴏᴏᴋᴜᴘ", 'success', EMOJI_SUCCESS))
    if row4:
        rows.append(KeyboardButtonRow(buttons=row4))
    
    # Row 5: PAK & IND NUM
    row5 = []
    if settings.get("pak_enabled", True):
        row5.append(create_colored_button("🇵🇰 ᴘᴀᴋ ɴᴜᴍʙᴇʀ ɪɴꜰᴏ", 'danger', EMOJI_DANGER))
    if settings.get("indnum_enabled", True):
        row5.append(create_colored_button("📲 ɪɴᴅ ɴᴜᴍ ɪɴꜰᴏ 𝟸", 'primary', EMOJI_PRIMARY))
    if row5:
        rows.append(KeyboardButtonRow(buttons=row5))
    
    # Row 6: IND NUM 3
    if settings.get("indnum3_enabled", True):
        rows.append(KeyboardButtonRow(buttons=[create_colored_button("🇮🇳 ɪɴᴅ ɴᴜᴍʙᴇʀ ɪɴꜰᴏ 𝟹 ➜👤", 'success', EMOJI_SUCCESS)]))
    
    # Row 7: Invite & Redeem
    rows.append(KeyboardButtonRow(buttons=[
        create_colored_button("👥 ɪɴᴠɪᴛᴇ & ᴇᴀʀɴ", 'primary', EMOJI_PRIMARY),
        create_colored_button("🎫 ʀᴇᴅᴇᴇᴍ ᴄᴏᴅᴇ", 'success', EMOJI_SUCCESS)
    ]))
    
    # Row 8: Admin Panel
    if is_admin:
        rows.append(KeyboardButtonRow(buttons=[create_colored_button("👑 ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ", 'danger', EMOJI_DANGER)]))
    
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
            'Name': f'{PE_USER} ɴᴀᴍᴇ',
            "Father's Name": f'{PE_FATHER} ꜰᴀᴛʜᴇʀ',
            'Mobile': f'{PE_PHONE2} ᴍᴏʙɪʟᴇ',
            'Address': f'{PE_LOCATION} ᴀᴅᴅʀᴇꜱꜱ',
            'Circle': f'{PE_NETWORK} ᴄɪʀᴄʟᴇ',
            'State': f'{PE_STATE} ꜱᴛᴀᴛᴇ'
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
        return f"<blockquote>{PE_CROSS} ɴᴏ ʀᴇᴄᴏʀᴅꜱ ꜰᴏᴜɴᴅ</blockquote>"
    title = {
        'aadhaar': f'{PE_CARD} ᴀᴀᴅʜᴀʀ',
        'mobile': f'{PE_INDIA} ɪɴᴅ ɴᴜᴍʙᴇʀ',
        'vehicle': f'{PE_CAR} ᴠᴇʜɪᴄʟᴇ'
    }.get(search_type, f'{PE_CHART} ʀᴇꜱᴜʟᴛ')
    result = f"<blockquote expandable>{PE_SPARKLE} {title} {PE_SPARKLE}</blockquote>\n<blockquote>{PE_CHART} ᴛᴏᴛᴀʟ ʀᴇᴄᴏʀᴅꜱ: {len(records)}</blockquote>\n"
    for i, record in enumerate(records, 1):
        if len(records) > 1:
            result += f"\n<blockquote>━━ {PE_USER} ʀᴇᴄᴏʀᴅ {i} ━━</blockquote>\n"
        for key, value in record.items():
            result += f"<blockquote>{key}: <code>{value}</code></blockquote>\n"
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
        return f"<blockquote>{PE_CROSS} ꜱᴇʀᴠɪᴄᴇ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ</blockquote>"
    if isinstance(data, dict) and not data.get("raw_text") and data.get("success"):
        d = data.get("data", data)
        if isinstance(d, dict):
            result = f"<blockquote expandable>{PE_SPARKLE} {PE_PHONE} ᴛᴇʟᴇɢʀᴀᴍ ɪᴅ ɪɴꜰᴏ {PE_SPARKLE}</blockquote>\n"
            if d.get('chat_id') or d.get('userid'):
                result += f"<blockquote>{PE_SEARCH} ᴄʜᴀᴛ ɪᴅ: <code>{d.get('chat_id', d.get('userid', query))}</code></blockquote>\n"
            if d.get('number'):
                result += f"<blockquote>{PE_PHONE2} ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ: <code>{d['number']}</code></blockquote>\n"
            if d.get('name'):
                result += f"<blockquote>{PE_USER} ᴘʀᴏꜰɪʟᴇ ɴᴀᴍᴇ: <code>{d['name']}</code></blockquote>\n"
            return result
    return f"<blockquote>{PE_CROSS} ɴᴏᴛ ꜰᴏᴜɴᴅ</blockquote>"

async def ifsc_lookup(session, code):
    data = await safe_api_fetch(session, f"{IFSC_API}{code.upper()}")
    if not data or isinstance(data, dict) and data.get("raw_text"):
        return f"<blockquote>{PE_CROSS} ꜱᴇʀᴠɪᴄᴇ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ</blockquote>"
    if isinstance(data, dict):
        return (f"<blockquote expandable>{PE_SPARKLE} {PE_BANK} ʙᴀɴᴋ ɪꜰꜱᴄ ᴅᴇᴛᴀɪʟꜱ {PE_SPARKLE}</blockquote>\n"
                f"<blockquote>{PE_BANK} ʙᴀɴᴋ ɴᴀᴍᴇ: <code>{data.get('BANK','N/A')}</code></blockquote>\n"
                f"<blockquote>{PE_LOCATION} ʙʀᴀɴᴄʜ: <code>{data.get('BRANCH','N/A')}</code></blockquote>\n"
                f"<blockquote>{PE_CARD} ɪꜰꜱᴄ ᴄᴏᴅᴇ: <code>{data.get('IFSC',code.upper())}</code></blockquote>\n"
                f"<blockquote>{PE_LOCATION} ᴀᴅᴅʀᴇꜱꜱ: <code>{data.get('ADDRESS','N/A')}</code></blockquote>")
    return f"<blockquote>{PE_CROSS} ɪɴᴠᴀʟɪᴅ ᴄᴏᴅᴇ</blockquote>"

async def bypass_lookup(session, link):
    s = get_settings()
    if s.get("bypass_maintenance", False):
        return f"<blockquote>{PE_TOOLS} ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ</blockquote>"
    data = await safe_api_fetch(session, f"{SHORTLINK_API}{link}", timeout=20)
    if not data or isinstance(data, dict) and data.get("raw_text"):
        return f"<blockquote>{PE_CROSS} ꜱᴇʀᴠɪᴄᴇ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ</blockquote>"
    if isinstance(data, dict):
        r = data.get('bypassed_url') or data.get('url') or str(data)
        return f"<blockquote expandable>{PE_SPARKLE} {PE_LINK} ʟɪɴᴋ ʙʏᴘᴀꜱꜱᴇᴅ {PE_SPARKLE}</blockquote>\n<blockquote>{PE_LINK} ᴏʀɪɢɪɴᴀʟ ᴜʀʟ: <code>{str(r)}</code></blockquote>"
    return f"<blockquote>{PE_LINK} ʀᴇꜱᴜʟᴛ: <code>{str(data)}</code></blockquote>"

async def gst_lookup(session, gst_number):
    data = await safe_api_fetch(session, f"{GST_API}{gst_number.upper()}", timeout=20)
    if not data or isinstance(data, dict) and data.get("raw_text"):
        return f"<blockquote>{PE_CROSS} ꜱᴇʀᴠɪᴄᴇ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ</blockquote>"
    if isinstance(data, dict) and data.get("status") == "success" and data.get("data"):
        d = data["data"]
        result = f"<blockquote expandable>{PE_SPARKLE} {PE_CARD} ɢꜱᴛ ʙᴜꜱɪɴᴇꜱꜱ ɪɴꜰᴏ {PE_SPARKLE}</blockquote>\n"
        if d.get('TradeName'):
            result += f"<blockquote>{PE_BANK} ʙᴜꜱɪɴᴇꜱꜱ ɴᴀᴍᴇ: <code>{d['TradeName']}</code></blockquote>\n"
        if d.get('Gstin'):
            result += f"<blockquote>{PE_CARD} ɢꜱᴛ ɴᴜᴍʙᴇʀ: <code>{d['Gstin']}</code></blockquote>\n"
        return result
    return f"<blockquote>{PE_CROSS} ɪɴᴠᴀʟɪᴅ ɢꜱᴛ</blockquote>"

async def pakistan_lookup(session, number):
    try:
        data = await safe_api_fetch(session, f"{PAK_API}{number}", timeout=20)
        if not data or isinstance(data, dict) and data.get("raw_text"):
            return f"<blockquote>{PE_CROSS} ꜱᴇʀᴠɪᴄᴇ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ</blockquote>"
        if isinstance(data, dict) and data.get("success") and data.get("data"):
            valid = [r for r in data["data"] if isinstance(r, dict) and any(r.get(k) for k in ['name', 'number', 'cnic', 'address'])]
            if not valid:
                return f"<blockquote>{PE_CROSS} ɴᴏ ᴅᴀᴛᴀ</blockquote>"
            result = f"<blockquote expandable>{PE_SPARKLE} {PE_PAK} ᴘᴀᴋɪꜱᴛᴀɴ ɴᴜᴍʙᴇʀ ɪɴꜰᴏ {PE_SPARKLE}</blockquote>\n"
            for i, r in enumerate(valid[:3], 1):
                if len(valid) > 1:
                    result += f"\n<blockquote>━━ {PE_USER} ʀᴇᴄᴏʀᴅ {i} ━━</blockquote>\n"
                if r.get('number'):
                    result += f"<blockquote>{PE_PHONE2} ᴘʜᴏɴᴇ: <code>{r['number']}</code></blockquote>\n"
                if r.get('name'):
                    result += f"<blockquote>{PE_USER} ɴᴀᴍᴇ: <code>{r['name']}</code></blockquote>\n"
                if r.get('cnic'):
                    result += f"<blockquote>{PE_CARD} ᴄɴɪᴄ: <code>{r['cnic']}</code></blockquote>\n"
                if r.get('address'):
                    result += f"<blockquote>{PE_LOCATION} ᴀᴅᴅʀᴇꜱꜱ: <code>{r['address'][:200]}</code></blockquote>\n"
            return result
        return f"<blockquote>{PE_CROSS} ɴᴏ ᴅᴀᴛᴀ</blockquote>"
    except:
        return f"<blockquote>{PE_CROSS} ᴇʀʀᴏʀ</blockquote>"

async def indnum_lookup(session, number):
    for attempt in range(3):
        data = await safe_api_fetch(session, f"{IND_NUM_API}{number}", timeout=30)
        if data and isinstance(data, dict) and not data.get("raw_text") and data.get("results"):
            break
        if attempt < 2:
            await asyncio.sleep(2)
    if not data or isinstance(data, dict) and data.get("raw_text"):
        return f"<blockquote>{PE_CROSS} ꜱᴇʀᴠɪᴄᴇ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ</blockquote>"
    results = data.get("results", {})
    if not results:
        return f"<blockquote>{PE_CROSS} ɴᴏ ʀᴇꜱᴜʟᴛꜱ</blockquote>"
    result = f"<blockquote expandable>{PE_SPARKLE} {PE_PHONE2} ɪɴᴅɪᴀɴ ɴᴜᴍʙᴇʀ ᴀᴅᴠᴀɴᴄᴇᴅ {PE_SPARKLE}</blockquote>\n<blockquote>{PE_PHONE2} ɴᴜᴍʙᴇʀ: <code>{number}</code></blockquote>\n"
    found = False
    s3 = results.get("source_3", {}).get("data", {})
    if isinstance(s3, dict):
        for k, e in [("SIM card", PE_SIM), ("Connection", PE_SIGNAL), ("Mobile State", PE_LOCATION), ("Hometown", PE_HOME)]:
            if s3.get(k):
                result += f"<blockquote>{e} {k}: <code>{str(s3[k])[:200]}</code></blockquote>\n"
                found = True
    s4 = results.get("source_4", {}).get("data", {})
    if isinstance(s4, dict) and s4.get("carrier"):
        result += f"<blockquote>{PE_NETWORK} ᴄᴀʀʀɪᴇʀ: <code>{s4['carrier']}</code></blockquote>\n"
        found = True
    return result if found else f"<blockquote>{PE_CROSS} ɴᴏ ᴅᴀᴛᴀ</blockquote>"

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
                return f"<blockquote>{PE_CROSS} ᴇᴍᴘᴛʏ ʀᴇꜱᴘᴏɴꜱᴇ</blockquote>"
            try:
                data = json.loads(text)
                if isinstance(data, dict):
                    result = f"<blockquote expandable>{PE_SPARKLE} {PE_INDIA} ɪɴᴅɪᴀɴ ɴᴜᴍʙᴇʀ ᴛʀᴀᴄᴋɪɴɢ {PE_SPARKLE}</blockquote>\n<blockquote>{PE_PHONE2} ɴᴜᴍʙᴇʀ: <code>{number}</code></blockquote>\n"
                    for k, v in data.items():
                        if v and str(v).strip():
                            result += f"<blockquote>{PE_SEARCH} {k}: <code>{str(v)[:200]}</code></blockquote>\n"
                    return result
            except:
                pass
            clean = re.sub(r'<[^>]+>', '\n', text)
            lines = [l.strip() for l in clean.split('\n') if l.strip() and len(l.strip()) > 1]
            result = f"<blockquote expandable>{PE_SPARKLE} {PE_INDIA} ɪɴᴅɪᴀɴ ɴᴜᴍʙᴇʀ ᴛʀᴀᴄᴋɪɴɢ {PE_SPARKLE}</blockquote>\n<blockquote>{PE_PHONE2} ɴᴜᴍʙᴇʀ: <code>{number}</code></blockquote>\n"
            found = 0
            for line in lines[:20]:
                if ':' in line:
                    parts = line.split(':', 1)
                    key, val = parts[0].strip(), parts[1].strip() if len(parts) > 1 else ''
                    if val:
                        e = PE_USER if any(w in key.lower() for w in ['name', 'nama']) else PE_NETWORK if any(w in key.lower() for w in ['carrier', 'operator', 'network', 'sim']) else PE_LOCATION if any(w in key.lower() for w in ['location', 'address', 'city', 'state', 'area']) else PE_PHONE2 if any(w in key.lower() for w in ['phone', 'mobile', 'number', 'no']) else PE_SEARCH
                        result += f"<blockquote>{e} {key}: <code>{val[:200]}</code></blockquote>\n"
                        found += 1
            if found == 0:
                result += f"<blockquote>{PE_CARD} ʀᴀᴡ ᴅᴀᴛᴀ: <code>{clean[:500]}</code></blockquote>\n"
            return result
    except:
        return f"<blockquote>{PE_CROSS} ᴛɪᴍᴇᴏᴜᴛ</blockquote>"

# --- 👑 ADMIN ---

async def admin_panel(event):
    if event.sender_id != ADMIN_ID:
        return
    s = get_settings()
    ms = lambda key: "🔴" if s.get(f"maint_{key}") else "🟢"
    
    # Create inline keyboard for admin
    from telethon.tl.types import KeyboardButtonCallback, ReplyInlineMarkup, KeyboardButtonRow
    
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
    
    # Convert to KeyboardButtonRow
    rows = []
    for row in buttons:
        rows.append(KeyboardButtonRow(buttons=row))
    
    markup = ReplyInlineMarkup(rows=rows)
    txt = f"<blockquote>{PE_CROWN} ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ {PE_CROWN}</blockquote>\n<blockquote>{PE_INVITE} ᴜꜱᴇʀꜱ: {len(load_json(USERS_FILE))} | {PE_TICKET} ᴄᴏᴅᴇꜱ: {len(load_json(REDEEM_FILE))}</blockquote>"
    
    if hasattr(event, 'data'):  # Callback query
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
        txt = f"<blockquote>{PE_TICKET} ᴄᴏᴅᴇꜱ: {len(codes)}</blockquote>\n"
        for c, v in list(codes.items())[-15:]:
            txt += f"<blockquote>{'✅' if not v.get('used') else '❌'} <code>{c}</code> | {v.get('credits')}cr</blockquote>\n"
        from telethon.tl.types import KeyboardButtonCallback, ReplyInlineMarkup, KeyboardButtonRow
        await event.edit(txt, buttons=ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text="🔄 ʙᴀᴄᴋ", data=b"ad_back")])]))
    elif d == "ad_gen":
        ADMIN_STATE[event.sender_id] = "gen"
        from telethon.tl.types import KeyboardButtonCallback, ReplyInlineMarkup, KeyboardButtonRow
        await event.edit(f"<blockquote>{PE_TICKET} ᴇɴᴛᴇʀ ᴄʀᴇᴅɪᴛꜱ:</blockquote>\n<i>100</i>", buttons=ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text="🔄 ʙᴀᴄᴋ", data=b"ad_back")])]))
    elif d == "ad_credit":
        ADMIN_STATE[event.sender_id] = "credit"
        from telethon.tl.types import KeyboardButtonCallback, ReplyInlineMarkup, KeyboardButtonRow
        await event.edit(f"<blockquote>{PE_GIFT} ᴇɴᴛᴇʀ ɪᴅ ᴀᴍᴏᴜɴᴛ:</blockquote>\n<i>123456789 50</i>", buttons=ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text="🔄 ʙᴀᴄᴋ", data=b"ad_back")])]))
    elif d == "ad_bcast":
        ADMIN_STATE[event.sender_id] = "bcast"
        from telethon.tl.types import KeyboardButtonCallback, ReplyInlineMarkup, KeyboardButtonRow
        await event.edit(f"<blockquote>{PE_BOLT} ᴇɴᴛᴇʀ ᴍᴇꜱꜱᴀɢᴇ:</blockquote>", buttons=ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text="🔄 ʙᴀᴄᴋ", data=b"ad_back")])]))
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
                        await send_message(int(inviter), f"<blockquote>{PE_GIFT} +{cr} ᴄʀᴇᴅɪᴛꜱ! ɴᴇᴡ ᴜꜱᴇʀ ᴊᴏɪɴᴇᴅ!</blockquote>")
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
        bot = await client.get_me()
        txt = (
            f"<b>{PE_DIAMOND} {BOT_NAME} {PE_DIAMOND}</b>\n"
            f"<b>@{BOT_USERNAME}</b>\n\n"
            f"<b>{PE_LOCK} ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ʀᴇQᴜɪʀᴇᴅ</b>\n"
            f"<b>ᴊᴏɪɴ ʙᴏᴛʜ ᴄʜᴀɴɴᴇʟꜱ ᴛᴏ ᴜɴʟᴏᴄᴋ</b>\n\n"
            f"<b>{PE_WARN} ɢᴜɪᴅᴇʟɪɴᴇꜱ:</b>\n"
            f"<b>• ᴇᴅᴜᴄᴀᴛɪᴏɴᴀʟ ᴘᴜʀᴘᴏꜱᴇꜱ ᴏɴʟʏ</b>\n"
            f"<b>• ᴜꜱᴇ ᴏɴ ʏᴏᴜʀ ᴏᴡɴ ᴅᴀᴛᴀ</b>\n"
            f"<b>• ʀᴇꜱᴘᴇᴄᴛ ᴘʀɪᴠᴀᴄʏ ʟᴀᴡꜱ</b>\n\n"
            f"<b>{PE_GIFT} +{DAILY_FREE_CREDITS} ᴅᴀɪʟʏ {PE_STAR}</b>\n"
            f"<b>{PE_INVITE} +{INVITE_CREDITS} ᴘᴇʀ ɪɴᴠɪᴛᴇ</b>\n"
            f"<b>{PE_CLOCK} {AUTO_DELETE_TIME}ꜱ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ</b>\n\n"
            f"<b>{PE_CROWN} ᴏᴡɴᴇʀ: @Hexh4ckerOFC</b>\n"
            f"<i>{PE_WARN} ᴍɪꜱᴜꜱᴇ ᴍᴀʏ ʟᴇᴀᴅ ᴛᴏ ʟᴇɢᴀʟ ᴀᴄᴛɪᴏɴ</i>"
        )
        
        # Create inline keyboard for verification
        from telethon.tl.types import KeyboardButtonCallback, ReplyInlineMarkup, KeyboardButtonRow
        buttons = [
            KeyboardButtonRow(buttons=[KeyboardButtonCallback(text="📢 ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ 𝟷", data=b"url1")]),
            KeyboardButtonRow(buttons=[KeyboardButtonCallback(text="📢 ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ 𝟸", data=b"url2")]),
            KeyboardButtonRow(buttons=[KeyboardButtonCallback(text="✅ ɪ'ᴠᴇ ᴊᴏɪɴᴇᴅ - ᴠᴇʀɪꜰʏ", data=b"verify")])
        ]
        markup = ReplyInlineMarkup(rows=buttons)
        
        await send_message(event.chat_id, txt, reply_markup=markup)
    except Exception as e:
        logger.error(f"Verification page: {e}")

@client.on(events.CallbackQuery(data=b"verify"))
async def verify_cb(event):
    if await check_channels(event.sender_id):
        user = get_user(event.sender_id)
        user["verified"] = True
        save_user(event.sender_id, user)
        await event.answer("✅ Verified!")
        try:
            await event.delete()
        except:
            pass
        # Send main menu
        await main_menu(event)
    else:
        await event.answer("❌ Join both channels first!", alert=True)

@client.on(events.CallbackQuery)
async def handle_url_callback(event):
    if event.data == b"url1":
        await event.answer(f"📢 Join: {LINK_1}", alert=True)
    elif event.data == b"url2":
        await event.answer(f"📢 Join: {LINK_2}", alert=True)

async def main_menu(event):
    """Send main menu with colored reply buttons"""
    is_admin = event.sender_id == ADMIN_ID
    user = get_user(event.sender_id)
    s = get_settings()
    
    markup = create_main_menu(is_admin, s)
    cr = user.get("credits", 0)
    
    txt = (
        f"<b>{PE_DIAMOND} ᴘʀᴇᴍɪᴜᴍ ʜᴜʙ {PE_DIAMOND}</b>\n"
        f"<b>{PE_USER} ᴡᴇʟᴄᴏᴍᴇ ʙᴀᴄᴋ,</b> <code>{event.sender.first_name}</code>\n\n"
        f"<b>{PE_CHART} ʏᴏᴜʀ ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ:</b>\n"
        f"<b>┃ {PE_CREDIT} ᴄʀᴇᴅɪᴛꜱ: {cr}</b>\n"
        f"<b>┃ {PE_SEARCH} Qᴜᴇʀɪᴇꜱ: {user.get('total_queries',0)}</b>\n"
        f"<b>┃ {PE_INVITE} ɪɴᴠɪᴛᴇꜱ: {user.get('invites',0)}</b>\n\n"
        f"<b>{PE_GIFT} ʀᴇᴡᴀʀᴅꜱ:</b>\n"
        f"<b>{PE_REFRESH} +{DAILY_FREE_CREDITS} ᴅᴀɪʟʏ ꜰʀᴇᴇ</b>\n"
        f"<b>{PE_INVITE} +{INVITE_CREDITS} ᴘᴇʀ ɪɴᴠɪᴛᴇ</b>\n"
        f"<b>{PE_CLOCK} {AUTO_DELETE_TIME}ꜱ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ</b>\n\n"
        f"<b>{PE_STAR} ꜱᴇʟᴇᴄᴛ ᴀ ꜱᴇʀᴠɪᴄᴇ ʙᴇʟᴏᴡ {PE_STAR}</b>"
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
            m = await send_message(event.chat_id, f"<blockquote>{PE_TOOLS} Under maintenance</blockquote>")
            asyncio.create_task(schedule_delete(m))
            return
        
        # Admin state handling
        if uid == ADMIN_ID and uid in ADMIN_STATE:
            state = ADMIN_STATE.pop(uid)
            if state == "gen":
                try:
                    cr = int(txt)
                    code = generate_redeem_code(cr)
                    msg = await send_message(event.chat_id, f"<blockquote>{PE_CHECK} <code>{code}</code> | {PE_CREDIT} {cr}cr</blockquote>")
                except:
                    msg = await send_message(event.chat_id, f"<blockquote>{PE_CROSS} Number</blockquote>")
                asyncio.create_task(schedule_delete(msg))
                return
            elif state == "credit":
                p = txt.split()
                if len(p) >= 2:
                    bal = add_credits(p[0], int(p[1]))
                    msg = await send_message(event.chat_id, f"<blockquote>{PE_CHECK} +{p[1]} | {bal}</blockquote>")
                else:
                    msg = await send_message(event.chat_id, f"<blockquote>{PE_CROSS} Format: ID AMOUNT</blockquote>")
                asyncio.create_task(schedule_delete(msg))
                return
            elif state == "bcast":
                users = load_json(USERS_FILE)
                cnt = 0
                for u in users:
                    try:
                        await send_message(int(u), f"{PE_BOLT} {txt}")
                        cnt += 1
                    except:
                        pass
                msg = await send_message(event.chat_id, f"<blockquote>{PE_CHECK} Sent: {cnt}</blockquote>")
                asyncio.create_task(schedule_delete(msg))
                return
        
        # Check verification
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
        
        # Handle admin panel button
        if txt == "👑 ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ":
            await admin_panel(event)
            return
        
        # Handle redeem mode
        if hasattr(event, 'redeem_mode') and event.redeem_mode:
            event.redeem_mode = False
            if txt.upper().startswith("HEX-"):
                success, msg = redeem_code(uid, txt)
                m = await send_message(event.chat_id, f"<blockquote>{msg}</blockquote>")
            else:
                m = await send_message(event.chat_id, f"<blockquote>{PE_CROSS} Invalid code!</blockquote>")
            asyncio.create_task(schedule_delete(m))
            return
        
        # Feature buttons mapping
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
                m = await send_message(event.chat_id, f"<blockquote>{PE_INVITE} ɪɴᴠɪᴛᴇ (+{INVITE_CREDITS}ᴄʀ)</blockquote>\n<blockquote><code>{link}</code></blockquote>")
                asyncio.create_task(schedule_delete(m, 120))
                return
            elif mode == "REDEEM":
                event.redeem_mode = True
                m = await send_message(event.chat_id, f"<blockquote>{PE_TICKET} ᴇɴᴛᴇʀ ʀᴇᴅᴇᴇᴍ ᴄᴏᴅᴇ:</blockquote>\n<i>HEX-XXXXXXXXXX</i>")
                asyncio.create_task(schedule_delete(m, 30))
                return
            
            # Check if feature is enabled
            if feature and not s.get(f"{feature}_enabled", True):
                m = await send_message(event.chat_id, f"<blockquote>{PE_DISABLED} Disabled</blockquote>")
                asyncio.create_task(schedule_delete(m))
                return
            
            if feature:
                maint, msg = check_feature_maintenance(feature)
                if maint:
                    m = await send_message(event.chat_id, f"<blockquote>{PE_TOOLS} {msg}</blockquote>")
                    asyncio.create_task(schedule_delete(m))
                    return
            
            # Set mode and prompt for input
            event.mode = mode
            prompts = {
                "TG": f"<blockquote>{PE_PHONE} ᴛᴇʟᴇɢʀᴀᴍ ɪᴅ ᴛᴏ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ</blockquote>\n<i>7123181749, 6884112825</i>",
                "IFSC": f"<blockquote>{PE_BANK} ʙᴀɴᴋ ɪꜰꜱᴄ ᴄᴏᴅᴇ</blockquote>\n<i>SBIN0001234, HDFC0001234</i>",
                "SHORTLINK": f"<blockquote>{PE_LINK} ʟɪɴᴋ ʙʏᴘᴀꜱꜱ</blockquote>\n<i>https://indianshortner.in/xxxx</i>",
                "MOBILE": f"<blockquote>{PE_INDIA} ɪɴᴅɪᴀɴ ᴍᴏʙɪʟᴇ ɴᴜᴍʙᴇʀ</blockquote>\n<i>9876543210, 8123456789</i>",
                "AADHAAR": f"<blockquote>{PE_CARD} ᴀᴀᴅʜᴀʀ ɴᴜᴍʙᴇʀ</blockquote>\n<i>123456789012</i>",
                "VEHICLE": f"<blockquote>{PE_CAR} ᴠᴇʜɪᴄʟᴇ ɴᴜᴍʙᴇʀ</blockquote>\n<i>KA01AB3256, DL1CX1234</i>",
                "GST": f"<blockquote>{PE_CARD} ɢꜱᴛ ɴᴜᴍʙᴇʀ</blockquote>\n<i>19BOKPS7056D1ZI</i>",
                "PAK": f"<blockquote>{PE_PAK} ᴘᴀᴋɪꜱᴛᴀɴ ɴᴜᴍʙᴇʀ</blockquote>\n<i>923078750447</i>",
                "INDNUM": f"<blockquote>{PE_PHONE2} ᴀᴅᴠᴀɴᴄᴇᴅ ɴᴜᴍʙᴇʀ</blockquote>\n<i>6363016966, 9876543210</i>",
                "INDNUM3": f"<blockquote>{PE_INDIA} ɪɴᴅɪᴀɴ ɴᴜᴍʙᴇʀ ᴛʀᴀᴄᴋɪɴɢ</blockquote>\n<i>6363016966, 9876543210</i>"
            }
            if mode in prompts:
                m = await send_message(event.chat_id, prompts[mode])
                asyncio.create_task(schedule_delete(m))
            return
        
        # Handle query mode
        if hasattr(event, 'mode') and event.mode:
            mode = event.mode
            if txt.upper().startswith("HEX-"):
                success, msg = redeem_code(uid, txt)
                m = await send_message(event.chat_id, f"<blockquote>{msg}</blockquote>")
                asyncio.create_task(schedule_delete(m))
                event.mode = None
                return
            
            user = get_user(uid)
            if user.get("credits", 0) <= 0:
                m = await send_message(event.chat_id, f"<blockquote>{PE_CROSS} No credits! +10 daily | +3 invite</blockquote>")
                asyncio.create_task(schedule_delete(m))
                event.mode = None
                return
            
            await run_query(event, mode, txt)
            event.mode = None
        
    except Exception as e:
        logger.error(f"Msg: {e}")

async def run_query(event, mode, query):
    if not await net_ok():
        m = await send_message(event.chat_id, f"<blockquote>{PE_CROSS} No internet</blockquote>")
        asyncio.create_task(schedule_delete(m))
        return
    
    names = {
        'TG': f'{PE_PHONE}',
        'IFSC': f'{PE_BANK}',
        'SHORTLINK': f'{PE_LINK}',
        'AADHAAR': f'{PE_CARD}',
        'MOBILE': f'{PE_INDIA}',
        'VEHICLE': f'{PE_CAR}',
        'GST': f'{PE_CARD}',
        'PAK': f'{PE_PAK}',
        'INDNUM': f'{PE_PHONE2}',
        'INDNUM3': f'{PE_INDIA}'
    }
    
    st = await send_message(event.chat_id, f"<blockquote>{PE_GREEN} ꜱᴇᴀʀᴄʜɪɴɢ...</blockquote>")
    lt = asyncio.create_task(loading_animation(st, names.get(mode, '')))
    credit_deducted = False
    
    try:
        if mode in ['AADHAAR', 'MOBILE', 'VEHICLE']:
            choice_map = {'AADHAAR': '2', 'MOBILE': '1', 'VEHICLE': '4'}
            raw = run_india_script(choice_map[mode], query)
            if raw:
                records = parse_all_india_records(raw)
                result = format_records_result(records, {'AADHAAR': 'aadhaar', 'MOBILE': 'mobile', 'VEHICLE': 'vehicle'}[mode])
                if records and f"{PE_CROSS}" not in str(result):
                    use_credit(event.sender_id)
                    credit_deducted = True
            else:
                result = f"<blockquote>{PE_CROSS} Script failed</blockquote>"
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
                    result = f"{PE_CROSS}"
            
            if result and f"{PE_CROSS}" not in str(result) and "unavailable" not in str(result).lower():
                use_credit(event.sender_id)
                credit_deducted = True
        
        lt.cancel()
        try:
            await lt
        except asyncio.CancelledError:
            pass
        
        user = get_user(event.sender_id)
        final = f"{result}\n{SEP}\n<blockquote>{PE_CREDIT} {'ᴄʀ: '+str(user.get('credits',0)) if credit_deducted else 'ɴᴏ ᴄʀ ᴅᴇᴅᴜᴄᴛᴇᴅ'} | {PE_CLOCK} {AUTO_DELETE_TIME}ꜱ</blockquote>{DISCLAIMER}{FOOTER}"
        sent = await edit_message(st, final)
        asyncio.create_task(schedule_delete(sent))
    except Exception as e:
        lt.cancel()
        logger.error(f"Query: {e}")
        try:
            await edit_message(st, f"<blockquote>{PE_WARN} ᴇʀʀᴏʀ</blockquote>{FOOTER}")
        except:
            pass

# --- 🚀 START ---

async def main():
    print("🔄 Hex Terminal Premium (Telethon Version)...")
    print(f"{PE_CHECK} {BOT_NAME} Ready!")
    if HAS_BUTTON_STYLE:
        print(f"{PE_DIAMOND} Colored Reply Buttons with Premium Emojis ENABLED")
    else:
        print(f"{PE_WARN} Colored buttons not available (using Telethon stable)")
        print(f"{PE_WARN} Install Telethon master branch for colored buttons")
    print(f"{PE_STAR} All premium emoji IDs are working")
    
    # Install dependencies if needed
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "requests", "beautifulsoup4"], capture_output=True, timeout=30)
    except:
        pass
    
    # Start client and run
    await client.start(bot_token=BOT_TOKEN)
    await client.run_until_disconnected()

# Fix: Properly handle event loop for Railway
if __name__ == '__main__':
    try:
        # Get or create event loop
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
    except RuntimeError as e:
        if "event loop" in str(e).lower():
            # Create new loop if there's an issue
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(main())
        else:
            raise
    except KeyboardInterrupt:
        print("Bot stopped by user")
    except Exception as e:
        print(f"Error: {e}")