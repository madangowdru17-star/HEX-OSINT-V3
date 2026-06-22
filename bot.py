# bot.py - Hex Terminal FINAL with HTML Parse Mode

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
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8687617595:AAGXvP6YiOX39vlRI0VYxpZjvlfmR7QMyf4')
ADMIN_ID = int(os.environ.get('ADMIN_ID', '7898928200'))

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

# --- PREMIUM EMOJIS FOR TEXT MESSAGES ---
PE = lambda eid, fallback: f'<tg-emoji emoji-id="{eid}">{fallback}</tg-emoji>'

EMOJI_WARN = PE("6267039884016358504", "⚠️")
EMOJI_CHECK = PE("6267008582294705964", "✅")
EMOJI_CROSS = PE("6267000941547885720", "❌")
EMOJI_LOCK = PE("5316522278056399236", "🔒")
EMOJI_CROWN = PE("6267128480601741166", "👑")
EMOJI_DIAMOND = PE("6264791387032523779", "💎")
EMOJI_STAR = PE("6266969287638913443", "⭐")
EMOJI_GIFT = PE("5203996991054432397", "🎁")
EMOJI_FIRE = PE("6264785189394717307", "🔥")
EMOJI_SEARCH = PE("5231012545799666522", "🔍")
EMOJI_PHONE = PE("5947494995798789024", "📞")
EMOJI_BANK = PE("5264895611517300926", "🏦")
EMOJI_LINK = PE("5271604874419647061", "🔗")
EMOJI_CAR = PE("5253752975997803460", "🚘")
EMOJI_CARD = PE("5260561650213220533", "🪪")
EMOJI_USER = PE("5249053508681883137", "👤")
EMOJI_INDIA = PE("6284779941489812433", "🇮🇳")
EMOJI_PAK = PE("5913705895375672082", "🇵🇰")
EMOJI_PHONE2 = PE("5406809207947142040", "📲")
EMOJI_INVITE = PE("5244933196230972438", "👥")
EMOJI_TICKET = PE("5285515895534278367", "🎫")
EMOJI_CREDIT = PE("6267068789146260253", "💰")
EMOJI_REFRESH = PE("5375338737028841420", "🔄")
EMOJI_CLOCK = PE("5382194935057372936", "⏱")
EMOJI_BOLT = PE("6284971355297290197", "⚡")
EMOJI_GREEN = PE("5386367538735104399", "🟩")
EMOJI_BLACK = PE("5116476703002068797", "⬛")
EMOJI_SPARKLE = PE("5467683093693354332", "✨")
EMOJI_ROCKET = PE("5195033767969839232", "🚀")
EMOJI_TOOLS = PE("5462921117423384478", "🛠️")
EMOJI_DISABLED = PE("5373165973203348165", "📴")
EMOJI_FATHER = PE("6147864334077794239", "👨")
EMOJI_LOCATION = PE("5391032818111363540", "📍")
EMOJI_HOME = PE("5280955052582785391", "🏠")
EMOJI_STATE = PE("5388927107315283144", "🏛")
EMOJI_NETWORK = PE("5321141214735508486", "📡")
EMOJI_SIGNAL = PE("6147892053796725336", "📶")
EMOJI_SIM = PE("5800717980266403037", "💳")
EMOJI_CHART = PE("6093382540784046658", "📊")

# --- BUTTON ICON IDs (3 IDs for all buttons) ---
EMOJI_PRIMARY = 5258096772776991776
EMOJI_SUCCESS = 5258503720928288433
EMOJI_DANGER = 5258331647358540449

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
            "invites": 0
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
        return False, f"{EMOJI_CROSS} ɪɴᴠᴀʟɪᴅ ᴄᴏᴅᴇ"
    if codes[code].get("used"):
        return False, f"{EMOJI_CROSS} ᴀʟʀᴇᴀᴅʏ ᴜꜱᴇᴅ"
    cr = codes[code]["credits"]
    codes[code]["used"] = True
    codes[code]["used_by"] = str(uid)
    save_json(REDEEM_FILE, codes)
    bal = add_credits(uid, cr)
    return True, f"{EMOJI_CHECK} +{cr} ᴄʀᴇᴅɪᴛꜱ ᴀᴅᴅᴇᴅ! {EMOJI_CREDIT} ʙᴀʟᴀɴᴄᴇ: {bal}"

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
            d[f"maint_msg_{k}"] = f"{EMOJI_TOOLS} {k} is under maintenance."
            d[f"maint_{k}"] = False
        save_json(SETTINGS_FILE, d)
        return d

def save_settings(data):
    save_json(SETTINGS_FILE, data)

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
        reply_markup=reply_markup,
        parse_mode='HTML'  # <--- IMPORTANT FIX
    ))

async def edit_message(msg, text, reply_markup=None):
    return await client(functions.messages.EditMessageRequest(
        peer=msg.peer_id,
        id=msg.id,
        message=text,
        reply_markup=reply_markup,
        parse_mode='HTML'  # <--- IMPORTANT FIX
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
            await edit_message(msg, f"<blockquote>{EMOJI_BOLT} {name}</blockquote>\n<code>{bar} {percentages[i]}</code>")
            await asyncio.sleep(0.2)
        except:
            break

def check_feature_maintenance(feature_key):
    s = get_settings()
    if s.get(f"maint_{feature_key}", False):
        return True, s.get(f"maint_msg_{feature_key}", f"{EMOJI_TOOLS} Under maintenance.")
    return False, ""

# --- 🎨 COLORED REPLY BUTTONS ---

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
        row1.append(create_colored_button("TG ID -> Phone Number", 'primary', EMOJI_PRIMARY))
    if settings.get("ifsc_enabled", True):
        row1.append(create_colored_button("IFSC Info", 'success', EMOJI_SUCCESS))
    if row1:
        rows.append(KeyboardButtonRow(buttons=row1))
    
    # Row 2: Link Bypass
    if settings.get("bypass_enabled", True):
        rows.append(KeyboardButtonRow(buttons=[create_colored_button("Link Bypass", 'primary', EMOJI_PRIMARY)]))
    
    # Row 3: Aadhaar & Mobile
    row3 = []
    if settings.get("aadhaar_enabled", True):
        row3.append(create_colored_button("Aadhar Info", 'success', EMOJI_SUCCESS))
    if settings.get("mobile_enabled", True):
        row3.append(create_colored_button("India Number Info", 'primary', EMOJI_PRIMARY))
    if row3:
        rows.append(KeyboardButtonRow(buttons=row3))
    
    # Row 4: RC & GST
    row4 = []
    if settings.get("rc_enabled", True):
        row4.append(create_colored_button("RC Details", 'danger', EMOJI_DANGER))
    if settings.get("gst_enabled", True):
        row4.append(create_colored_button("GST Lookup", 'success', EMOJI_SUCCESS))
    if row4:
        rows.append(KeyboardButtonRow(buttons=row4))
    
    # Row 5: PAK & IND NUM
    row5 = []
    if settings.get("pak_enabled", True):
        row5.append(create_colored_button("Pakistan Number Info", 'danger', EMOJI_DANGER))
    if settings.get("indnum_enabled", True):
        row5.append(create_colored_button("India Number Info 2", 'primary', EMOJI_PRIMARY))
    if row5:
        rows.append(KeyboardButtonRow(buttons=row5))
    
    # Row 6: IND NUM 3
    if settings.get("indnum3_enabled", True):
        rows.append(KeyboardButtonRow(buttons=[create_colored_button("India Number Tracking", 'success', EMOJI_SUCCESS)]))
    
    # Row 7: Invite & Redeem
    rows.append(KeyboardButtonRow(buttons=[
        create_colored_button("Invite & Earn", 'primary', EMOJI_PRIMARY),
        create_colored_button("Redeem Code", 'success', EMOJI_SUCCESS)
    ]))
    
    # Row 8: Admin Panel
    if is_admin:
        rows.append(KeyboardButtonRow(buttons=[create_colored_button("Admin Panel", 'danger', EMOJI_DANGER)]))
    
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
            'Name': f'{EMOJI_USER} ɴᴀᴍᴇ',
            "Father's Name": f'{EMOJI_FATHER} ꜰᴀᴛʜᴇʀ',
            'Mobile': f'{EMOJI_PHONE2} ᴍᴏʙɪʟᴇ',
            'Address': f'{EMOJI_LOCATION} ᴀᴅᴅʀᴇꜱꜱ',
            'Circle': f'{EMOJI_NETWORK} ᴄɪʀᴄʟᴇ',
            'State': f'{EMOJI_STATE} ꜱᴛᴀᴛᴇ'
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
        return f"{EMOJI_CROSS} ɴᴏ ʀᴇᴄᴏʀᴅꜱ ꜰᴏᴜɴᴅ"
    title = {
        'aadhaar': f'{EMOJI_CARD} ᴀᴀᴅʜᴀʀ',
        'mobile': f'{EMOJI_INDIA} ɪɴᴅ ɴᴜᴍʙᴇʀ',
        'vehicle': f'{EMOJI_CAR} ᴠᴇʜɪᴄʟᴇ'
    }.get(search_type, f'{EMOJI_CHART} ʀᴇꜱᴜʟᴛ')
    result = f"{EMOJI_SPARKLE} {title} {EMOJI_SPARKLE}\n{EMOJI_CHART} ᴛᴏᴛᴀʟ: {len(records)}\n"
    for i, record in enumerate(records, 1):
        if len(records) > 1:
            result += f"\n━━ {EMOJI_USER} ʀᴇᴄᴏʀᴅ {i} ━━\n"
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
        return f"{EMOJI_CROSS} ꜱᴇʀᴠɪᴄᴇ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ"
    if isinstance(data, dict) and not data.get("raw_text") and data.get("success"):
        d = data.get("data", data)
        if isinstance(d, dict):
            result = f"{EMOJI_SPARKLE} {EMOJI_PHONE} ᴛᴇʟᴇɢʀᴀᴍ ɪᴅ ɪɴꜰᴏ {EMOJI_SPARKLE}\n"
            if d.get('chat_id') or d.get('userid'):
                result += f"{EMOJI_SEARCH} ᴄʜᴀᴛ ɪᴅ: {d.get('chat_id', d.get('userid', query))}\n"
            if d.get('number'):
                result += f"{EMOJI_PHONE2} ᴘʜᴏɴᴇ: {d['number']}\n"
            if d.get('name'):
                result += f"{EMOJI_USER} ɴᴀᴍᴇ: {d['name']}\n"
            return result
    return f"{EMOJI_CROSS} ɴᴏᴛ ꜰᴏᴜɴᴅ"

async def ifsc_lookup(session, code):
    data = await safe_api_fetch(session, f"{IFSC_API}{code.upper()}")
    if not data or isinstance(data, dict) and data.get("raw_text"):
        return f"{EMOJI_CROSS} ꜱᴇʀᴠɪᴄᴇ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ"
    if isinstance(data, dict):
        return (f"{EMOJI_SPARKLE} {EMOJI_BANK} ʙᴀɴᴋ ɪꜰꜱᴄ ᴅᴇᴛᴀɪʟꜱ {EMOJI_SPARKLE}\n"
                f"{EMOJI_BANK} ʙᴀɴᴋ: {data.get('BANK','N/A')}\n"
                f"{EMOJI_LOCATION} ʙʀᴀɴᴄʜ: {data.get('BRANCH','N/A')}\n"
                f"{EMOJI_CARD} ɪꜰꜱᴄ: {data.get('IFSC',code.upper())}\n"
                f"{EMOJI_LOCATION} ᴀᴅᴅʀᴇꜱꜱ: {data.get('ADDRESS','N/A')}")
    return f"{EMOJI_CROSS} ɪɴᴠᴀʟɪᴅ ᴄᴏᴅᴇ"

async def bypass_lookup(session, link):
    s = get_settings()
    if s.get("bypass_maintenance", False):
        return f"{EMOJI_TOOLS} ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ"
    data = await safe_api_fetch(session, f"{SHORTLINK_API}{link}", timeout=20)
    if not data or isinstance(data, dict) and data.get("raw_text"):
        return f"{EMOJI_CROSS} ꜱᴇʀᴠɪᴄᴇ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ"
    if isinstance(data, dict):
        r = data.get('bypassed_url') or data.get('url') or str(data)
        return f"{EMOJI_SPARKLE} {EMOJI_LINK} ʟɪɴᴋ ʙʏᴘᴀꜱꜱᴇᴅ {EMOJI_SPARKLE}\n{EMOJI_LINK} ᴜʀʟ: {str(r)}"
    return f"{EMOJI_LINK} ʀᴇꜱᴜʟᴛ: {str(data)}"

async def gst_lookup(session, gst_number):
    data = await safe_api_fetch(session, f"{GST_API}{gst_number.upper()}", timeout=20)
    if not data or isinstance(data, dict) and data.get("raw_text"):
        return f"{EMOJI_CROSS} ꜱᴇʀᴠɪᴄᴇ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ"
    if isinstance(data, dict) and data.get("status") == "success" and data.get("data"):
        d = data["data"]
        result = f"{EMOJI_SPARKLE} {EMOJI_CARD} ɢꜱᴛ ɪɴꜰᴏ {EMOJI_SPARKLE}\n"
        if d.get('TradeName'):
            result += f"{EMOJI_BANK} ʙᴜꜱɪɴᴇꜱꜱ: {d['TradeName']}\n"
        if d.get('Gstin'):
            result += f"{EMOJI_CARD} ɢꜱᴛ: {d['Gstin']}\n"
        return result
    return f"{EMOJI_CROSS} ɪɴᴠᴀʟɪᴅ ɢꜱᴛ"

async def pakistan_lookup(session, number):
    try:
        data = await safe_api_fetch(session, f"{PAK_API}{number}", timeout=20)
        if not data or isinstance(data, dict) and data.get("raw_text"):
            return f"{EMOJI_CROSS} ꜱᴇʀᴠɪᴄᴇ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ"
        if isinstance(data, dict) and data.get("success") and data.get("data"):
            valid = [r for r in data["data"] if isinstance(r, dict) and any(r.get(k) for k in ['name', 'number', 'cnic', 'address'])]
            if not valid:
                return f"{EMOJI_CROSS} ɴᴏ ᴅᴀᴛᴀ"
            result = f"{EMOJI_SPARKLE} {EMOJI_PAK} ᴘᴀᴋɪꜱᴛᴀɴ ɴᴜᴍʙᴇʀ ɪɴꜰᴏ {EMOJI_SPARKLE}\n"
            for i, r in enumerate(valid[:3], 1):
                if len(valid) > 1:
                    result += f"\n━━ {EMOJI_USER} ʀᴇᴄᴏʀᴅ {i} ━━\n"
                if r.get('number'):
                    result += f"{EMOJI_PHONE2} ᴘʜᴏɴᴇ: {r['number']}\n"
                if r.get('name'):
                    result += f"{EMOJI_USER} ɴᴀᴍᴇ: {r['name']}\n"
                if r.get('cnic'):
                    result += f"{EMOJI_CARD} ᴄɴɪᴄ: {r['cnic']}\n"
                if r.get('address'):
                    result += f"{EMOJI_LOCATION} ᴀᴅᴅʀᴇꜱꜱ: {r['address'][:200]}\n"
            return result
        return f"{EMOJI_CROSS} ɴᴏ ᴅᴀᴛᴀ"
    except:
        return f"{EMOJI_CROSS} ᴇʀʀᴏʀ"

async def indnum_lookup(session, number):
    for attempt in range(3):
        data = await safe_api_fetch(session, f"{IND_NUM_API}{number}", timeout=30)
        if data and isinstance(data, dict) and not data.get("raw_text") and data.get("results"):
            break
        if attempt < 2:
            await asyncio.sleep(2)
    if not data or isinstance(data, dict) and data.get("raw_text"):
        return f"{EMOJI_CROSS} ꜱᴇʀᴠɪᴄᴇ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ"
    results = data.get("results", {})
    if not results:
        return f"{EMOJI_CROSS} ɴᴏ ʀᴇꜱᴜʟᴛꜱ"
    result = f"{EMOJI_SPARKLE} {EMOJI_PHONE2} ɪɴᴅɪᴀɴ ɴᴜᴍʙᴇʀ ᴀᴅᴠᴀɴᴄᴇᴅ {EMOJI_SPARKLE}\n{EMOJI_PHONE2} ɴᴜᴍʙᴇʀ: {number}\n"
    found = False
    s3 = results.get("source_3", {}).get("data", {})
    if isinstance(s3, dict):
        for k, e in [("SIM card", EMOJI_SIM), ("Connection", EMOJI_SIGNAL), ("Mobile State", EMOJI_LOCATION), ("Hometown", EMOJI_HOME)]:
            if s3.get(k):
                result += f"{e} {k}: {str(s3[k])[:200]}\n"
                found = True
    s4 = results.get("source_4", {}).get("data", {})
    if isinstance(s4, dict) and s4.get("carrier"):
        result += f"{EMOJI_NETWORK} ᴄᴀʀʀɪᴇʀ: {s4['carrier']}\n"
        found = True
    return result if found else f"{EMOJI_CROSS} ɴᴏ ᴅᴀᴛᴀ"

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
                return f"{EMOJI_CROSS} ᴇᴍᴘᴛʏ ʀᴇꜱᴘᴏɴꜱᴇ"
            try:
                data = json.loads(text)
                if isinstance(data, dict):
                    result = f"{EMOJI_SPARKLE} {EMOJI_INDIA} ɪɴᴅɪᴀɴ ɴᴜᴍʙᴇʀ ᴛʀᴀᴄᴋɪɴɢ {EMOJI_SPARKLE}\n{EMOJI_PHONE2} ɴᴜᴍʙᴇʀ: {number}\n"
                    for k, v in data.items():
                        if v and str(v).strip():
                            result += f"{EMOJI_SEARCH} {k}: {str(v)[:200]}\n"
                    return result
            except:
                pass
            clean = re.sub(r'<[^>]+>', '\n', text)
            lines = [l.strip() for l in clean.split('\n') if l.strip() and len(l.strip()) > 1]
            result = f"{EMOJI_SPARKLE} {EMOJI_INDIA} ɪɴᴅɪᴀɴ ɴᴜᴍʙᴇʀ ᴛʀᴀᴄᴋɪɴɢ {EMOJI_SPARKLE}\n{EMOJI_PHONE2} ɴᴜᴍʙᴇʀ: {number}\n"
            found = 0
            for line in lines[:20]:
                if ':' in line:
                    parts = line.split(':', 1)
                    key, val = parts[0].strip(), parts[1].strip() if len(parts) > 1 else ''
                    if val:
                        e = EMOJI_USER if any(w in key.lower() for w in ['name', 'nama']) else EMOJI_NETWORK if any(w in key.lower() for w in ['carrier', 'operator', 'network', 'sim']) else EMOJI_LOCATION if any(w in key.lower() for w in ['location', 'address', 'city', 'state', 'area']) else EMOJI_PHONE2 if any(w in key.lower() for w in ['phone', 'mobile', 'number', 'no']) else EMOJI_SEARCH
                        result += f"{e} {key}: {val[:200]}\n"
                        found += 1
            if found == 0:
                result += f"{EMOJI_CARD} ʀᴀᴡ: {clean[:500]}\n"
            return result
    except:
        return f"{EMOJI_CROSS} ᴛɪᴍᴇᴏᴜᴛ"

# --- 👑 ADMIN ---

async def admin_panel(event):
    if event.sender_id != ADMIN_ID:
        return
    s = get_settings()
    ms = lambda key: f"{EMOJI_DANGER}" if s.get(f"maint_{key}") else f"{EMOJI_SUCCESS}"
    
    buttons = [
        [KeyboardButtonCallback(text="Generate Code", data=b"ad_gen"), KeyboardButtonCallback(text="List Codes", data=b"ad_codes")],
        [KeyboardButtonCallback(text="Add Credits", data=b"ad_credit"), KeyboardButtonCallback(text="Broadcast", data=b"ad_bcast")],
        [KeyboardButtonCallback(text=f"{'🔴' if s.get('maintenance_mode') else '🟢'} Global", data=b"ad_maint")],
        [KeyboardButtonCallback(text=f"{'🟢' if s.get('tgid_enabled',True) else '🔴'} TG", data=b"ad_tgid"), KeyboardButtonCallback(text=f"{ms('tgid')} M", data=b"ad_maint_tgid")],
        [KeyboardButtonCallback(text=f"{'🟢' if s.get('ifsc_enabled',True) else '🔴'} IF", data=b"ad_ifsc"), KeyboardButtonCallback(text=f"{ms('ifsc')} M", data=b"ad_maint_ifsc")],
        [KeyboardButtonCallback(text=f"{'🟢' if s.get('bypass_enabled',True) else '🔴'} BY", data=b"ad_bypass_toggle"), KeyboardButtonCallback(text=f"{ms('bypass')} M", data=b"ad_maint_bypass")],
        [KeyboardButtonCallback(text=f"{'🟢' if s.get('mobile_enabled',True) else '🔴'} MO", data=b"ad_mobile"), KeyboardButtonCallback(text=f"{ms('mobile')} M", data=b"ad_maint_mobile")],
        [KeyboardButtonCallback(text=f"{'🟢' if s.get('aadhaar_enabled',True) else '🔴'} AA", data=b"ad_aadhaar"), KeyboardButtonCallback(text=f"{ms('aadhaar')} M", data=b"ad_maint_aadhaar")],
        [KeyboardButtonCallback(text=f"{'🟢' if s.get('rc_enabled',True) else '🔴'} RC", data=b"ad_rc"), KeyboardButtonCallback(text=f"{ms('rc')} M", data=b"ad_maint_rc")],
        [KeyboardButtonCallback(text=f"{'🟢' if s.get('gst_enabled',True) else '🔴'} GS", data=b"ad_gst"), KeyboardButtonCallback(text=f"{ms('gst')} M", data=b"ad_maint_gst")],
        [KeyboardButtonCallback(text=f"{'🟢' if s.get('pak_enabled',True) else '🔴'} PA", data=b"ad_pak"), KeyboardButtonCallback(text=f"{ms('pak')} M", data=b"ad_maint_pak")],
        [KeyboardButtonCallback(text=f"{'🟢' if s.get('indnum_enabled',True) else '🔴'} IN2", data=b"ad_indnum"), KeyboardButtonCallback(text=f"{ms('indnum')} M", data=b"ad_maint_indnum")],
        [KeyboardButtonCallback(text=f"{'🟢' if s.get('indnum3_enabled',True) else '🔴'} IN3", data=b"ad_indnum3"), KeyboardButtonCallback(text=f"{ms('indnum3')} M", data=b"ad_maint_indnum3")],
        [KeyboardButtonCallback(text="Close", data=b"ad_close")]
    ]
    
    rows = []
    for row in buttons:
        rows.append(KeyboardButtonRow(buttons=row))
    
    markup = ReplyInlineMarkup(rows=rows)
    txt = f"{EMOJI_CROWN} ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ {EMOJI_CROWN}\n{EMOJI_INVITE} ᴜꜱᴇʀꜱ: {len(load_json(USERS_FILE))} | {EMOJI_TICKET} ᴄᴏᴅᴇꜱ: {len(load_json(REDEEM_FILE))}"
    
    if hasattr(event, 'data'):
        await event.edit(txt, buttons=markup)
    else:
        await send_message(event.chat_id, txt, reply_markup=markup)

async def admin_callback(event):
    if event.sender_id != ADMIN_ID:
        await event.answer(f"{EMOJI_CROSS}", alert=True)
        return
    d = event.data.decode()
    s = get_settings()
    
    if d == "ad_close":
        await event.delete()
    elif d == "ad_codes":
        codes = load_json(REDEEM_FILE)
        txt = f"{EMOJI_TICKET} ᴄᴏᴅᴇꜱ: {len(codes)}\n"
        for c, v in list(codes.items())[-15:]:
            txt += f"{EMOJI_CHECK if not v.get('used') else EMOJI_CROSS} {c} | {v.get('credits')}cr\n"
        from telethon.tl.types import KeyboardButtonCallback, ReplyInlineMarkup, KeyboardButtonRow
        await event.edit(txt, buttons=ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text="Back", data=b"ad_back")])]))
    elif d == "ad_gen":
        ADMIN_STATE[event.sender_id] = "gen"
        from telethon.tl.types import KeyboardButtonCallback, ReplyInlineMarkup, KeyboardButtonRow
        await event.edit(f"{EMOJI_TICKET} ᴇɴᴛᴇʀ ᴄʀᴇᴅɪᴛꜱ:\n100", buttons=ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text="Back", data=b"ad_back")])]))
    elif d == "ad_credit":
        ADMIN_STATE[event.sender_id] = "credit"
        from telethon.tl.types import KeyboardButtonCallback, ReplyInlineMarkup, KeyboardButtonRow
        await event.edit(f"{EMOJI_GIFT} ᴇɴᴛᴇʀ ɪᴅ ᴀᴍᴏᴜɴᴛ:\n123456789 50", buttons=ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text="Back", data=b"ad_back")])]))
    elif d == "ad_bcast":
        ADMIN_STATE[event.sender_id] = "bcast"
        from telethon.tl.types import KeyboardButtonCallback, ReplyInlineMarkup, KeyboardButtonRow
        await event.edit(f"{EMOJI_BOLT} ᴇɴᴛᴇʀ ᴍᴇꜱꜱᴀɢᴇ:", buttons=ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text="Back", data=b"ad_back")])]))
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
                        await send_message(int(inviter), f"{EMOJI_GIFT} +{cr} ᴄʀᴇᴅɪᴛꜱ! {EMOJI_USER} ɴᴇᴡ ᴜꜱᴇʀ ᴊᴏɪɴᴇᴅ!")
                    except:
                        pass
                    break
        
        await main_menu(event)
    except Exception as e:
        logger.error(f"Start: {e}")

async def main_menu(event):
    is_admin = event.sender_id == ADMIN_ID
    user = get_user(event.sender_id)
    s = get_settings()
    
    markup = create_main_menu(is_admin, s)
    cr = user.get("credits", 0)
    
    txt = (
        f"{EMOJI_DIAMOND} ʜᴇx ᴛᴇʀᴍɪɴᴀʟ ʜᴜʙ {EMOJI_DIAMOND}\n"
        f"{EMOJI_USER} ᴡᴇʟᴄᴏᴍᴇ ʙᴀᴄᴋ, {event.sender.first_name}\n\n"
        f"{EMOJI_CHART} ʏᴏᴜʀ ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ:\n"
        f"{EMOJI_CREDIT} ᴄʀᴇᴅɪᴛꜱ: {cr}\n"
        f"{EMOJI_SEARCH} Qᴜᴇʀɪᴇꜱ: {user.get('total_queries',0)}\n"
        f"{EMOJI_INVITE} ɪɴᴠɪᴛᴇꜱ: {user.get('invites',0)}\n\n"
        f"{EMOJI_GIFT} ʀᴇᴡᴀʀᴅꜱ:\n"
        f"{EMOJI_REFRESH} +{DAILY_FREE_CREDITS} ᴅᴀɪʟʏ ꜰʀᴇᴇ\n"
        f"{EMOJI_INVITE} +{INVITE_CREDITS} ᴘᴇʀ ɪɴᴠɪᴛᴇ\n"
        f"{EMOJI_CLOCK} {AUTO_DELETE_TIME}ꜱ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ\n\n"
        f"{EMOJI_STAR} ꜱᴇʟᴇᴄᴛ ᴀ ꜱᴇʀᴠɪᴄᴇ ʙᴇʟᴏᴡ {EMOJI_STAR}"
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
            m = await send_message(event.chat_id, f"{EMOJI_TOOLS} Under maintenance")
            asyncio.create_task(schedule_delete(m))
            return
        
        if uid == ADMIN_ID and uid in ADMIN_STATE:
            state = ADMIN_STATE.pop(uid)
            if state == "gen":
                try:
                    cr = int(txt)
                    code = generate_redeem_code(cr)
                    msg = await send_message(event.chat_id, f"{EMOJI_CHECK} {code} | {EMOJI_CREDIT} {cr}cr")
                except:
                    msg = await send_message(event.chat_id, f"{EMOJI_CROSS} Number")
                asyncio.create_task(schedule_delete(msg))
                return
            elif state == "credit":
                p = txt.split()
                if len(p) >= 2:
                    bal = add_credits(p[0], int(p[1]))
                    msg = await send_message(event.chat_id, f"{EMOJI_CHECK} +{p[1]} | {bal}")
                else:
                    msg = await send_message(event.chat_id, f"{EMOJI_CROSS} Format: ID AMOUNT")
                asyncio.create_task(schedule_delete(msg))
                return
            elif state == "bcast":
                users = load_json(USERS_FILE)
                cnt = 0
                for u in users:
                    try:
                        await send_message(int(u), f"{EMOJI_BOLT} {txt}")
                        cnt += 1
                    except:
                        pass
                msg = await send_message(event.chat_id, f"{EMOJI_CHECK} Sent: {cnt}")
                asyncio.create_task(schedule_delete(msg))
                return
        
        # Handle admin panel button
        if txt == "Admin Panel":
            await admin_panel(event)
            return
        
        # Handle redeem mode
        if hasattr(event, 'redeem_mode') and event.redeem_mode:
            event.redeem_mode = False
            if txt.upper().startswith("HEX-"):
                success, msg = redeem_code(uid, txt)
                m = await send_message(event.chat_id, msg)
            else:
                m = await send_message(event.chat_id, f"{EMOJI_CROSS} Invalid code!")
            asyncio.create_task(schedule_delete(m))
            return
        
        # Feature buttons mapping
        mode = None
        feature_map = {
            "TG ID -> Phone Number": ("TG", "tgid"),
            "IFSC Info": ("IFSC", "ifsc"),
            "Link Bypass": ("SHORTLINK", "bypass"),
            "India Number Info": ("MOBILE", "mobile"),
            "Aadhar Info": ("AADHAAR", "aadhaar"),
            "RC Details": ("VEHICLE", "rc"),
            "GST Lookup": ("GST", "gst"),
            "Pakistan Number Info": ("PAK", "pak"),
            "India Number Info 2": ("INDNUM", "indnum"),
            "India Number Tracking": ("INDNUM3", "indnum3"),
            "Invite & Earn": ("INVITE", None),
            "Redeem Code": ("REDEEM", None)
        }
        
        if txt in feature_map:
            mode, feature = feature_map[txt]
            
            if mode == "INVITE":
                user = get_user(uid)
                bot_username = BOT_USERNAME
                link = f"https://t.me/{bot_username}?start={user['invite_code']}"
                m = await send_message(event.chat_id, f"{EMOJI_INVITE} ɪɴᴠɪᴛᴇ (+{INVITE_CREDITS}ᴄʀ)\n{EMOJI_LINK} {link}")
                asyncio.create_task(schedule_delete(m, 120))
                return
            elif mode == "REDEEM":
                event.redeem_mode = True
                m = await send_message(event.chat_id, f"{EMOJI_TICKET} ᴇɴᴛᴇʀ ʀᴇᴅᴇᴇᴍ ᴄᴏᴅᴇ:\nHEX-XXXXXXXXXX")
                asyncio.create_task(schedule_delete(m, 30))
                return
            
            if feature and not s.get(f"{feature}_enabled", True):
                m = await send_message(event.chat_id, f"{EMOJI_DISABLED} Disabled")
                asyncio.create_task(schedule_delete(m))
                return
            
            if feature:
                maint, msg = check_feature_maintenance(feature)
                if maint:
                    m = await send_message(event.chat_id, f"{EMOJI_TOOLS} {msg}")
                    asyncio.create_task(schedule_delete(m))
                    return
            
            event.mode = mode
            prompts = {
                "TG": f"{EMOJI_PHONE} ᴇɴᴛᴇʀ ᴛɢ ɪᴅ:\n7123181749, 6884112825",
                "IFSC": f"{EMOJI_BANK} ᴇɴᴛᴇʀ ɪꜰꜱᴄ:\nSBIN0001234, HDFC0001234",
                "SHORTLINK": f"{EMOJI_LINK} ᴇɴᴛᴇʀ ʟɪɴᴋ:\nhttps://indianshortner.in/xxxx",
                "MOBILE": f"{EMOJI_INDIA} ᴇɴᴛᴇʀ ɴᴜᴍʙᴇʀ:\n9876543210, 8123456789",
                "AADHAAR": f"{EMOJI_CARD} ᴇɴᴛᴇʀ ᴀᴀᴅʜᴀʀ:\n123456789012",
                "VEHICLE": f"{EMOJI_CAR} ᴇɴᴛᴇʀ ᴠᴇʜɪᴄʟᴇ:\nKA01AB3256, DL1CX1234",
                "GST": f"{EMOJI_CARD} ᴇɴᴛᴇʀ ɢꜱᴛ:\n19BOKPS7056D1ZI",
                "PAK": f"{EMOJI_PAK} ᴇɴᴛᴇʀ ɴᴜᴍʙᴇʀ:\n923078750447",
                "INDNUM": f"{EMOJI_PHONE2} ᴇɴᴛᴇʀ ɴᴜᴍʙᴇʀ:\n6363016966, 9876543210",
                "INDNUM3": f"{EMOJI_INDIA} ᴇɴᴛᴇʀ ɴᴜᴍʙᴇʀ:\n6363016966, 9876543210"
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
                m = await send_message(event.chat_id, msg)
                asyncio.create_task(schedule_delete(m))
                event.mode = None
                return
            
            user = get_user(uid)
            if user.get("credits", 0) <= 0:
                m = await send_message(event.chat_id, f"{EMOJI_CROSS} No credits! +10 daily | +3 invite")
                asyncio.create_task(schedule_delete(m))
                event.mode = None
                return
            
            await run_query(event, mode, txt)
            event.mode = None
        
    except Exception as e:
        logger.error(f"Msg: {e}")

async def run_query(event, mode, query):
    if not await net_ok():
        m = await send_message(event.chat_id, f"{EMOJI_CROSS} No internet")
        asyncio.create_task(schedule_delete(m))
        return
    
    st = await send_message(event.chat_id, f"{EMOJI_GREEN} ꜱᴇᴀʀᴄʜɪɴɢ...")
    lt = asyncio.create_task(loading_animation(st, mode))
    credit_deducted = False
    
    try:
        if mode in ['AADHAAR', 'MOBILE', 'VEHICLE']:
            choice_map = {'AADHAAR': '2', 'MOBILE': '1', 'VEHICLE': '4'}
            raw = run_india_script(choice_map[mode], query)
            if raw:
                records = parse_all_india_records(raw)
                result = format_records_result(records, {'AADHAAR': 'aadhaar', 'MOBILE': 'mobile', 'VEHICLE': 'vehicle'}[mode])
                if records and f"{EMOJI_CROSS}" not in str(result):
                    use_credit(event.sender_id)
                    credit_deducted = True
            else:
                result = f"{EMOJI_CROSS} Script failed"
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
                    result = f"{EMOJI_CROSS} ERROR"
            
            if result and f"{EMOJI_CROSS}" not in str(result) and "unavailable" not in str(result).lower():
                use_credit(event.sender_id)
                credit_deducted = True
        
        lt.cancel()
        try:
            await lt
        except asyncio.CancelledError:
            pass
        
        user = get_user(event.sender_id)
        final = f"{result}\n{SEP}\n{EMOJI_CREDIT} {'ᴄʀ: '+str(user.get('credits',0)) if credit_deducted else 'ɴᴏ ᴄʀ ᴅᴇᴅᴜᴄᴛᴇᴅ'} | {EMOJI_CLOCK} {AUTO_DELETE_TIME}ꜱ{FOOTER}"
        sent = await edit_message(st, final)
        asyncio.create_task(schedule_delete(sent))
    except Exception as e:
        lt.cancel()
        logger.error(f"Query: {e}")
        try:
            await edit_message(st, f"{EMOJI_WARN} Error{FOOTER}")
        except:
            pass

# --- 🚀 START ---

async def main():
    print("Hex Terminal FINAL Version")
    print("ALL Premium Emojis Working with parse_mode='HTML'")
    print("3 button icon IDs used for all buttons")
    
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