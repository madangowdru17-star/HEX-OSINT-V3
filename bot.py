# bot.py - Hex OSINT Bot FINAL WORKING with Perfect Quote Format

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

try:
    from telethon import TelegramClient, events, functions
    from telethon.tl.types import (
        KeyboardButton, KeyboardButtonRow, ReplyKeyboardMarkup,
        KeyboardButtonStyle, KeyboardButtonCallback, ReplyInlineMarkup,
        KeyboardButtonUrl
    )
    from telethon.tl.functions.channels import GetParticipantRequest
    from telethon.errors import UserNotParticipantError, ChannelPrivateError
    HAS_BUTTON_STYLE = True
except ImportError:
    print("Installing Telethon...")
    subprocess.run([sys.executable, "-m", "pip", "install", "git+https://github.com/LonamiWebs/Telethon.git"])
    from telethon import TelegramClient, events, functions
    from telethon.tl.types import (
        KeyboardButton, KeyboardButtonRow, ReplyKeyboardMarkup,
        KeyboardButtonStyle, KeyboardButtonCallback, ReplyInlineMarkup,
        KeyboardButtonUrl
    )
    from telethon.tl.functions.channels import GetParticipantRequest
    from telethon.errors import UserNotParticipantError, ChannelPrivateError
    HAS_BUTTON_STYLE = True

# --- ⚙️ CONFIGURATION ---
API_ID = int(os.environ.get('API_ID', '37996037'))
API_HASH = os.environ.get('API_HASH', '47ee9fa07b5eeb865edb3d79ada726a5')
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8687617595:AAGXvP6YiOX39vlRI0VYxpZjvlfmR7QMyf4')
ADMIN_ID = int(os.environ.get('ADMIN_ID', '7898928200'))

CHANNEL_1_ID = int(os.environ.get('CHANNEL_1_ID', '-1003240507339'))
CHANNEL_2_ID = int(os.environ.get('CHANNEL_2_ID', '-1003806004135'))

LINK_1 = os.environ.get('LINK_1', 'https://t.me/+dP7xLb3AoE1jNmRl')
LINK_2 = os.environ.get('LINK_2', 'https://t.me/+9vuPcr9LJ8piODdl')

FOOTER = "\n\n💎 ᴘᴏᴡᴇʀᴇᴅ ʙʏ @Hexh4ckerOFC 💎"
SEP = "━━━━━━━━━━━━━━━━━━━"

# APIs
LOOKUP_API = "https://toxic-tg.vercel.app/?userid="
IFSC_API = "https://ifsc.razorpay.com/"
SHORTLINK_API = "https://link-btpass.onrender.com/bypass?key=9c44ad66b95cef8aecd7a99cfb362ce0&link="
GST_API = "https://gst-0y-vishal.vercel.app/api/gst.js?gstNumber="
PAK_API = "https://api-server-virid-two.vercel.app/number="
IND_NUM_API = "https://all-number-info-rajan-eta.vercel.app/api?number="

VERIFY_SCRIPT = "verify_india.py"

USERS_FILE = os.path.join(os.getcwd(), "users.json")
REDEEM_FILE = os.path.join(os.getcwd(), "redeem_codes.json")
SETTINGS_FILE = os.path.join(os.getcwd(), "settings.json")

DAILY_FREE_CREDITS = 10
INVITE_CREDITS = 3
AUTO_DELETE_TIME = 60

BOT_NAME = "𝗛𝗲𝘅 𝗢𝗦𝗜𝗡𝗧 𝗕𝗼𝘁"
BOT_USERNAME = "Hex_Terminal_bot"

# --- ALL PREMIUM EMOJI IDs ---
PE = lambda eid, fallback: f'<tg-emoji emoji-id="{eid}">{fallback}</tg-emoji>'

E_STAR = PE("6266969287638913443", "⭐")
E_DIAMOND = PE("6264791387032523779", "💎")
E_CROWN = PE("6267128480601741166", "👑")
E_FIRE = PE("6264785189394717307", "🔥")
E_CHECK = PE("6267008582294705964", "✅")
E_CROSS = PE("6267000941547885720", "❌")
E_WARN = PE("6267039884016358504", "⚠️")
E_LOCK = PE("5316522278056399236", "🔒")
E_PHONE = PE("5947494995798789024", "📞")
E_PHONE2 = PE("5406809207947142040", "📲")
E_BANK = PE("5264895611517300926", "🏦")
E_CAR = PE("5253752975997803460", "🚘")
E_CARD = PE("5260561650213220533", "🪪")
E_USER = PE("5249053508681883137", "👤")
E_USERS = PE("5244933196230972438", "👥")
E_INDIA = PE("6284779941489812433", "🇮🇳")
E_PAK = PE("5913705895375672082", "🇵🇰")
E_SEARCH = PE("5231012545799666522", "🔍")
E_CREDIT = PE("6267068789146260253", "💰")
E_REFRESH = PE("5375338737028841420", "🔄")
E_CLOCK = PE("5382194935057372936", "⏱")
E_BOLT = PE("6284971355297290197", "⚡")
E_GIFT = PE("5203996991054432397", "🎁")
E_TICKET = PE("5285515895534278367", "🎫")
E_TOOLS = PE("5462921117423384478", "🛠️")
E_DISABLED = PE("5373165973203348165", "📴")
E_LOCATION = PE("5391032818111363540", "📍")
E_HOME = PE("5280955052582785391", "🏠")
E_STATE = PE("5388927107315283144", "🏛")
E_NETWORK = PE("5321141214735508486", "📡")
E_SIGNAL = PE("6147892053796725336", "📶")
E_SIM = PE("5800717980266403037", "💳")
E_CHART = PE("6093382540784046658", "📊")
E_SPARKLE = PE("5467683093693354332", "✨")
E_ROCKET = PE("5195033767969839232", "🚀")
E_STAR2 = PE("6266969287638913443", "🌟")
E_LINK = PE("5271604874419647061", "🔗")
E_GEAR = PE("5462921117423384478", "⚙️")
E_WELCOME = PE("6266969287638913443", "✨")
E_INFO = PE("5231012545799666522", "ℹ️")
E_LIST = PE("6093382540784046658", "📋")
E_PIN = PE("5280955052582785391", "📌")
E_BOOK = PE("5285515895534278367", "📖")
E_COIN = PE("6267068789146260253", "🪙")
E_WALLET = PE("6267068789146260253", "👛")
E_DOC = PE("5260561650213220533", "📄")
E_POINT = PE("6266969287638913443", "🔹")
E_TROPHY = PE("6267128480601741166", "🏆")
E_BOOKMARK = PE("5271604874419647061", "🔖")
E_TARGET = PE("5231012545799666522", "🎯")
E_FLAG = PE("6284779941489812433", "🏁")
E_BABY = PE("6264785189394717307", "🍼")
E_MAGIC = PE("6264785189394717307", "🪄")

# --- BUTTON ICON IDs ---
ICON_IFSC = 5264895611517300926
ICON_AADHAAR = 5260561650213220533
ICON_INDIA = 6284779941489812433
ICON_RC = 5253752975997803460
ICON_GST = 5260561650213220533
ICON_PAK = 5913705895375672082
ICON_INVITE = 5244933196230972438
ICON_REDEEM = 5285515895534278367
ICON_ADMIN = 6267128480601741166
ICON_NEXT = 5258331647358540449
ICON_PRIMARY = 5258096772776991776

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
ADMIN_STATE = {}
USER_MODES = {}

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
        return False, f"{E_CROSS} ɪɴᴠᴀʟɪᴅ ᴄᴏᴅᴇ"
    if codes[code].get("used"):
        return False, f"{E_CROSS} ᴀʟʀᴇᴀᴅʏ ᴜꜱᴇᴅ"
    cr = codes[code]["credits"]
    codes[code]["used"] = True
    codes[code]["used_by"] = str(uid)
    save_json(REDEEM_FILE, codes)
    bal = add_credits(uid, cr)
    return True, f"{E_CHECK} +{cr} ᴄʀᴇᴅɪᴛꜱ ᴀᴅᴅᴇᴅ!\n{E_CREDIT} ʙᴀʟᴀɴᴄᴇ: {bal}"

def get_settings():
    try:
        return load_json(SETTINGS_FILE)
    except:
        d = {
            "bypass_maintenance": False,
            "ifsc_enabled": True,
            "mobile_enabled": True,
            "aadhaar_enabled": True,
            "rc_enabled": True,
            "gst_enabled": True,
            "pak_enabled": True,
            "maintenance_mode": False,
            "page": 1
        }
        for k in ["ifsc", "mobile", "aadhaar", "rc", "gst", "pak"]:
            d[f"maint_msg_{k}"] = f"{E_TOOLS} {k} is under maintenance."
            d[f"maint_{k}"] = False
        save_json(SETTINGS_FILE, d)
        return d

def save_settings(data):
    save_json(SETTINGS_FILE, data)

# --- 🔍 VERIFY ---

async def check_channel_member(channel_id, user_id):
    try:
        result = await client(GetParticipantRequest(
            channel=channel_id,
            participant=user_id
        ))
        return True
    except UserNotParticipantError:
        return False
    except:
        return False

async def check_channels(uid):
    try:
        in_channel1 = await check_channel_member(CHANNEL_1_ID, uid)
        in_channel2 = await check_channel_member(CHANNEL_2_ID, uid)
        return in_channel1 and in_channel2
    except:
        return False

async def check_individual_channels(uid):
    try:
        in_channel1 = await check_channel_member(CHANNEL_1_ID, uid)
        in_channel2 = await check_channel_member(CHANNEL_2_ID, uid)
        return in_channel1, in_channel2
    except:
        return False, False

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

async def send_html(chat_id, text, reply_markup=None):
    return await client.send_message(
        chat_id,
        text,
        buttons=reply_markup,
        parse_mode='html'
    )

async def edit_html(msg, text, reply_markup=None):
    return await client.edit_message(
        msg,
        text,
        buttons=reply_markup,
        parse_mode='html'
    )

def check_feature_maintenance(feature_key):
    s = get_settings()
    if s.get(f"maint_{feature_key}", False):
        return True, s.get(f"maint_msg_{feature_key}", f"{E_TOOLS} Under maintenance.")
    return False, ""

# --- 📋 PERFECT QUOTE FORMAT ---

def quote_format(content):
    """
    Creates a perfect quote format:
    First line: border
    Second line: empty
    Then: content
    Last line: empty
    Last line: border
    """
    border = "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬"
    
    # If content is a list, join with newlines
    if isinstance(content, list):
        content = "\n".join(content)
    
    return f"{border}\n\n{content}\n\n{border}"

def quote_box(title, content, emoji=None):
    """Create a quote box with title and content"""
    lines = []
    if emoji:
        lines.append(f"{emoji} <b>{title}</b> {emoji}")
    else:
        lines.append(f"<b>{title}</b>")
    lines.append("")
    if isinstance(content, list):
        lines.extend(content)
    else:
        lines.append(str(content))
    lines.append("")
    lines.append(f"{E_DIAMOND} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @Hexh4ckerOFC {E_DIAMOND}")
    
    return quote_format("\n".join(lines))

def info_quote(title, instruction, example, tip=None):
    """Create info message with quote format"""
    lines = []
    lines.append(f"<b>{title}</b>")
    lines.append("")
    lines.append(instruction)
    lines.append("")
    lines.append(f"ᴇxᴀᴍᴩʟᴇ: {example}")
    if tip:
        lines.append(f"ᴛɪᴩ: {tip}")
    lines.append("")
    lines.append(f"<b>ᴛᴏᴛᴀʟ ᴩᴏɪɴᴛꜱ:</b> 2 ᴩᴏɪɴᴛ")
    lines.append(f"<b>ꜱᴇᴀʀᴄʜ ᴄᴏꜱᴛ:</b> 1 ᴩᴏɪɴᴛ")
    lines.append("")
    lines.append(f"{E_DIAMOND} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @Hexh4ckerOFC {E_DIAMOND}")
    
    return quote_format("\n".join(lines))

def result_quote(title, records, emoji=None):
    """Create result message with quote format"""
    lines = []
    if emoji:
        lines.append(f"{emoji} <b>{title}</b> {emoji}")
    else:
        lines.append(f"<b>{title}</b>")
    lines.append("")
    lines.append(f"<b>ᴛᴏᴛᴀʟ:</b> {len(records)}")
    lines.append("")
    
    for i, record in enumerate(records, 1):
        lines.append(f"<b>ʀᴇᴄᴏʀᴅ {i}</b>")
        if isinstance(record, dict):
            for key, value in record.items():
                clean_key = key.replace('🏦', '').replace('📍', '').replace('🪪', '').replace('👤', '').replace('📲', '').replace('📡', '').replace('🏛', '').strip()
                lines.append(f"<b>{clean_key}:</b> {value}")
        else:
            lines.append(str(record))
        if i < len(records):
            lines.append("")
    
    lines.append("")
    lines.append(f"{E_DIAMOND} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @Hexh4ckerOFC {E_DIAMOND}")
    
    return quote_format("\n".join(lines))

def simple_quote(title, content, emoji=None):
    """Create simple quote message"""
    lines = []
    if emoji:
        lines.append(f"{emoji} <b>{title}</b> {emoji}")
    else:
        lines.append(f"<b>{title}</b>")
    lines.append("")
    if isinstance(content, list):
        lines.extend(content)
    else:
        lines.append(str(content))
    lines.append("")
    lines.append(f"{E_DIAMOND} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @Hexh4ckerOFC {E_DIAMOND}")
    
    return quote_format("\n".join(lines))

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
    
    page = settings.get("page", 1)
    rows = []
    
    if page == 1:
        row1 = []
        if settings.get("ifsc_enabled", True):
            row1.append(create_colored_button("IFSC Lookup", 'primary', ICON_IFSC))
        if settings.get("aadhaar_enabled", True):
            row1.append(create_colored_button("Aadhar Lookup", 'primary', ICON_AADHAAR))
        if row1:
            rows.append(KeyboardButtonRow(buttons=row1))
        
        row2 = []
        if settings.get("mobile_enabled", True):
            row2.append(create_colored_button("India Number", 'primary', ICON_INDIA))
        if settings.get("rc_enabled", True):
            row2.append(create_colored_button("RC Check", 'primary', ICON_RC))
        if row2:
            rows.append(KeyboardButtonRow(buttons=row2))
        
        row3 = []
        if settings.get("gst_enabled", True):
            row3.append(create_colored_button("GST Verify", 'primary', ICON_GST))
        if settings.get("pak_enabled", True):
            row3.append(create_colored_button("Pakistan Number", 'primary', ICON_PAK))
        if row3:
            rows.append(KeyboardButtonRow(buttons=row3))
        
        rows.append(KeyboardButtonRow(buttons=[
            create_colored_button("Invite & Earn", 'primary', ICON_INVITE),
            create_colored_button("Redeem Code", 'primary', ICON_REDEEM)
        ]))
        
        next_row = []
        next_row.append(create_colored_button("Next Page ➜", 'danger', ICON_NEXT))
        if is_admin:
            next_row.append(create_colored_button("Admin Panel", 'danger', ICON_ADMIN))
        rows.append(KeyboardButtonRow(buttons=next_row))
    
    else:
        rows.append(KeyboardButtonRow(buttons=[create_colored_button("Service 1", 'primary', ICON_PRIMARY)]))
        rows.append(KeyboardButtonRow(buttons=[create_colored_button("Service 2", 'primary', ICON_PRIMARY)]))
        rows.append(KeyboardButtonRow(buttons=[create_colored_button("Service 3", 'primary', ICON_PRIMARY)]))
        rows.append(KeyboardButtonRow(buttons=[create_colored_button("Service 4", 'primary', ICON_PRIMARY)]))
        rows.append(KeyboardButtonRow(buttons=[create_colored_button("Service 5", 'primary', ICON_PRIMARY)]))
        
        prev_row = []
        prev_row.append(create_colored_button("◀ Previous Page", 'danger', ICON_NEXT))
        if is_admin:
            prev_row.append(create_colored_button("Admin Panel", 'danger', ICON_ADMIN))
        rows.append(KeyboardButtonRow(buttons=prev_row))
    
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
            'Name': 'NAME',
            "Father's Name": 'FATHER',
            'Mobile': 'MOBILE',
            'Address': 'ADDRESS',
            'Circle': 'CIRCLE',
            'State': 'STATE'
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
        return f"{E_CROSS} ɴᴏ ʀᴇᴄᴏʀᴅꜱ ꜰᴏᴜɴᴅ"
    
    title = {
        'aadhaar': f'{E_CARD} ᴀᴀᴅʜᴀʀ',
        'mobile': f'{E_INDIA} ɪɴᴅɪᴀɴ ɴᴜᴍʙᴇʀ',
        'vehicle': f'{E_CAR} ᴠᴇʜɪᴄʟᴇ'
    }.get(search_type, f'{E_CHART} ʀᴇꜱᴜʟᴛ')
    
    return result_quote(title, records, E_SPARKLE)

# --- 🔗 API FUNCTIONS ---

async def safe_api_fetch(session, url, timeout=20):
    for attempt in range(3):
        try:
            headers = {'User-Agent': 'Mozilla/5.0', 'Accept': '*/*'}
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

async def ifsc_lookup(session, code):
    data = await safe_api_fetch(session, f"{IFSC_API}{code.upper()}")
    if not data or isinstance(data, dict) and data.get("raw_text"):
        return f"{E_CROSS} ꜱᴇʀᴠɪᴄᴇ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ"
    if isinstance(data, dict):
        record = {
            "ʙᴀɴᴋ": data.get('BANK','N/A'),
            "ʙʀᴀɴᴄʜ": data.get('BRANCH','N/A'),
            "ɪꜰꜱᴄ": data.get('IFSC',code.upper()),
            "ᴀᴅᴅʀᴇꜱꜱ": data.get('ADDRESS','N/A')
        }
        return result_quote("ʙᴀɴᴋ ɪꜰꜱᴄ ᴅᴇᴛᴀɪʟꜱ", [record], E_SPARKLE)
    return f"{E_CROSS} ɪɴᴠᴀʟɪᴅ ᴄᴏᴅᴇ"

async def gst_lookup(session, gst_number):
    data = await safe_api_fetch(session, f"{GST_API}{gst_number.upper()}", timeout=20)
    if not data or isinstance(data, dict) and data.get("raw_text"):
        return f"{E_CROSS} ꜱᴇʀᴠɪᴄᴇ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ"
    if isinstance(data, dict) and data.get("status") == "success" and data.get("data"):
        d = data["data"]
        record = {}
        if d.get('TradeName'):
            record["ʙᴜꜱɪɴᴇꜱꜱ"] = d['TradeName']
        if d.get('Gstin'):
            record["ɢꜱᴛ"] = d['Gstin']
        return result_quote("ɢꜱᴛ ɪɴꜰᴏ", [record], E_SPARKLE)
    return f"{E_CROSS} ɪɴᴠᴀʟɪᴅ ɢꜱᴛ"

async def pakistan_lookup(session, number):
    try:
        data = await safe_api_fetch(session, f"{PAK_API}{number}", timeout=20)
        if not data or isinstance(data, dict) and data.get("raw_text"):
            return f"{E_CROSS} ꜱᴇʀᴠɪᴄᴇ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ"
        if isinstance(data, dict) and data.get("success") and data.get("data"):
            valid = [r for r in data["data"] if isinstance(r, dict) and any(r.get(k) for k in ['name', 'number', 'cnic', 'address'])]
            if not valid:
                return f"{E_CROSS} ɴᴏ ᴅᴀᴛᴀ"
            
            records = []
            for r in valid[:3]:
                record = {}
                if r.get('number'):
                    record["ᴘʜᴏɴᴇ"] = r['number']
                if r.get('name'):
                    record["ɴᴀᴍᴇ"] = r['name']
                if r.get('cnic'):
                    record["ᴄɴɪᴄ"] = r['cnic']
                if r.get('address'):
                    record["ᴀᴅᴅʀᴇꜱꜱ"] = r['address'][:200]
                if record:
                    records.append(record)
            
            return result_quote(f"{E_PAK} ᴘᴀᴋɪꜱᴛᴀɴ ɴᴜᴍʙᴇʀ ɪɴꜰᴏ", records, E_SPARKLE)
        return f"{E_CROSS} ɴᴏ ᴅᴀᴛᴀ"
    except:
        return f"{E_CROSS} ᴇʀʀᴏʀ"

# --- 👑 ADMIN ---

async def admin_panel(event):
    if event.sender_id != ADMIN_ID:
        return
    s = get_settings()
    ms = lambda key: f"{E_CROSS}" if s.get(f"maint_{key}") else f"{E_CHECK}"
    
    buttons = [
        [KeyboardButtonCallback(text="Generate Code", data=b"ad_gen"), KeyboardButtonCallback(text="List Codes", data=b"ad_codes")],
        [KeyboardButtonCallback(text="Add Credits", data=b"ad_credit"), KeyboardButtonCallback(text="Broadcast", data=b"ad_bcast")],
        [KeyboardButtonCallback(text=f"{E_CROSS if s.get('maintenance_mode') else E_CHECK} Global", data=b"ad_maint")],
        [KeyboardButtonCallback(text=f"{E_CHECK if s.get('ifsc_enabled',True) else E_CROSS} IF", data=b"ad_ifsc"), KeyboardButtonCallback(text=f"{ms('ifsc')} M", data=b"ad_maint_ifsc")],
        [KeyboardButtonCallback(text=f"{E_CHECK if s.get('mobile_enabled',True) else E_CROSS} MO", data=b"ad_mobile"), KeyboardButtonCallback(text=f"{ms('mobile')} M", data=b"ad_maint_mobile")],
        [KeyboardButtonCallback(text=f"{E_CHECK if s.get('aadhaar_enabled',True) else E_CROSS} AA", data=b"ad_aadhaar"), KeyboardButtonCallback(text=f"{ms('aadhaar')} M", data=b"ad_maint_aadhaar")],
        [KeyboardButtonCallback(text=f"{E_CHECK if s.get('rc_enabled',True) else E_CROSS} RC", data=b"ad_rc"), KeyboardButtonCallback(text=f"{ms('rc')} M", data=b"ad_maint_rc")],
        [KeyboardButtonCallback(text=f"{E_CHECK if s.get('gst_enabled',True) else E_CROSS} GS", data=b"ad_gst"), KeyboardButtonCallback(text=f"{ms('gst')} M", data=b"ad_maint_gst")],
        [KeyboardButtonCallback(text=f"{E_CHECK if s.get('pak_enabled',True) else E_CROSS} PA", data=b"ad_pak"), KeyboardButtonCallback(text=f"{ms('pak')} M", data=b"ad_maint_pak")],
        [KeyboardButtonCallback(text="Close", data=b"ad_close")]
    ]
    
    rows = []
    for row in buttons:
        rows.append(KeyboardButtonRow(buttons=row))
    
    markup = ReplyInlineMarkup(rows=rows)
    
    txt = simple_quote(
        "ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ",
        [
            f"{E_USERS} <b>ᴜꜱᴇʀꜱ:</b> {len(load_json(USERS_FILE))}",
            f"{E_TICKET} <b>ᴄᴏᴅᴇꜱ:</b> {len(load_json(REDEEM_FILE))}"
        ],
        E_CROWN
    )
    
    if hasattr(event, 'data'):
        await event.edit(txt, buttons=markup)
    else:
        await send_html(event.chat_id, txt, reply_markup=markup)

async def admin_callback(event):
    if event.sender_id != ADMIN_ID:
        await event.answer(f"{E_CROSS}", alert=True)
        return
    d = event.data.decode()
    s = get_settings()
    
    if d == "ad_close":
        await event.delete()
    elif d == "ad_codes":
        codes = load_json(REDEEM_FILE)
        content = []
        for c, v in list(codes.items())[-15:]:
            status = f"{E_CHECK}" if not v.get('used') else f"{E_CROSS}"
            content.append(f"{status} <code>{c}</code> | {v.get('credits')}ᴄʀ")
        txt = simple_quote("ᴄᴏᴅᴇꜱ", content, E_TICKET)
        from telethon.tl.types import KeyboardButtonCallback, ReplyInlineMarkup, KeyboardButtonRow
        await event.edit(txt, buttons=ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text="Back", data=b"ad_back")])]))
    elif d == "ad_gen":
        ADMIN_STATE[event.sender_id] = "gen"
        from telethon.tl.types import KeyboardButtonCallback, ReplyInlineMarkup, KeyboardButtonRow
        txt = simple_quote(
            "ɢᴇɴᴇʀᴀᴛᴇ ᴄᴏᴅᴇ",
            "ꜱᴇɴᴅ ɴᴜᴍʙᴇʀ ᴏꜰ ᴄʀᴇᴅɪᴛꜱ:\n<code>100</code>",
            E_TICKET
        )
        await event.edit(txt, buttons=ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text="Back", data=b"ad_back")])]))
    elif d == "ad_credit":
        ADMIN_STATE[event.sender_id] = "credit"
        from telethon.tl.types import KeyboardButtonCallback, ReplyInlineMarkup, KeyboardButtonRow
        txt = simple_quote(
            "ᴀᴅᴅ ᴄʀᴇᴅɪᴛꜱ",
            "ꜱᴇɴᴅ ꜰᴏʀᴍᴀᴛ:\n<code>ᴜꜱᴇʀ_ɪᴅ ᴀᴍᴏᴜɴᴛ</code>",
            E_GIFT
        )
        await event.edit(txt, buttons=ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text="Back", data=b"ad_back")])]))
    elif d == "ad_bcast":
        ADMIN_STATE[event.sender_id] = "bcast"
        from telethon.tl.types import KeyboardButtonCallback, ReplyInlineMarkup, KeyboardButtonRow
        txt = simple_quote(
            "ʙʀᴏᴀᴅᴄᴀꜱᴛ",
            "ꜱᴇɴᴅ ʏᴏᴜʀ ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴍᴇꜱꜱᴀɢᴇ:",
            E_BOLT
        )
        await event.edit(txt, buttons=ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text="Back", data=b"ad_back")])]))
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
            "ad_ifsc": "ifsc_enabled",
            "ad_mobile": "mobile_enabled",
            "ad_aadhaar": "aadhaar_enabled",
            "ad_rc": "rc_enabled",
            "ad_gst": "gst_enabled",
            "ad_pak": "pak_enabled"
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
                        await send_html(int(inviter), f"{E_GIFT} +{cr} ᴄʀᴇᴅɪᴛꜱ! ɴᴇᴡ ᴜꜱᴇʀ ᴊᴏɪɴᴇᴅ!")
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

@client.on(events.CallbackQuery(data=b"verify"))
async def verify_cb(event):
    try:
        uid = event.sender_id
        
        in_channel1, in_channel2 = await check_individual_channels(uid)
        
        if in_channel1 and in_channel2:
            user = get_user(uid)
            user["verified"] = True
            save_user(uid, user)
            await event.answer("✅ Verified!", alert=True)
            try:
                await event.delete()
            except:
                pass
            try:
                await event.message.delete()
            except:
                pass
            await main_menu(event)
        elif not in_channel1 and not in_channel2:
            await event.answer("❌ Join both channels first!", alert=True)
        elif not in_channel1:
            await event.answer("❌ Join Channel 1 first!", alert=True)
        elif not in_channel2:
            await event.answer("❌ Join Channel 2 first!", alert=True)
    except Exception as e:
        logger.error(f"Verify callback error: {e}")
        await event.answer("❌ Error, try again", alert=True)

@client.on(events.CallbackQuery)
async def handle_url_callback(event):
    if event.data == b"url1":
        await event.answer(f"{E_LINK} Join: {LINK_1}", alert=True)
    elif event.data == b"url2":
        await event.answer(f"{E_LINK} Join: {LINK_2}", alert=True)

async def main_menu(event):
    is_admin = event.sender_id == ADMIN_ID
    user = get_user(event.sender_id)
    s = get_settings()
    
    if not await check_channels(event.sender_id):
        user["verified"] = False
        save_user(event.sender_id, user)
        await show_verification_page(event)
        return
    
    markup = create_main_menu(is_admin, s)
    cr = user.get("credits", 0)
    name = event.sender.first_name or "User"
    
    txt = simple_quote(
        f"{BOT_NAME}",
        [
            f"@{BOT_USERNAME}",
            "",
            f"{E_WARN} <b>ᴡᴇʟᴄᴏᴍᴇ</b> {name}!",
            "",
            f"{E_CREDIT} <b>ᴄʀᴇᴅɪᴛꜱ:</b> {cr}",
            f"{E_CROWN} <b>ᴘʀᴇᴍɪᴜᴍ:</b> ᴜɴʟɪᴍɪᴛᴇᴅ",
            "",
            f"{E_GEAR} ᴜꜱᴇ ᴛʜᴇ ʙᴜᴛᴛᴏɴꜱ ʙᴇʟᴏᴡ",
            f"{E_STAR} /ʜᴇʟᴘ ꜰᴏʀ ᴄᴏᴍᴍᴀɴᴅꜱ",
            "",
            f"{E_STAR2} ꜱᴇʟᴇᴄᴛ ᴀ ꜱᴇʀᴠɪᴄᴇ ʙᴇʟᴏᴡ"
        ],
        E_DIAMOND
    )
    
    msg = await send_html(event.chat_id, txt, reply_markup=markup)
    asyncio.create_task(schedule_delete(msg, AUTO_DELETE_TIME))

@client.on(events.NewMessage)
async def msg_handler(event):
    try:
        uid = event.sender_id
        txt = event.message.message.strip()
        
        if not txt:
            return
            
        if not txt.startswith('/start'):
            asyncio.create_task(schedule_delete(event.message, AUTO_DELETE_TIME))
        
        s = get_settings()
        
        if s.get("maintenance_mode", False) and uid != ADMIN_ID:
            m = await send_html(event.chat_id, simple_quote(
                "ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴍᴏᴅᴇ",
                "ʙᴏᴛ ɪꜱ ᴄᴜʀʀᴇɴᴛʟʏ ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ.",
                E_TOOLS
            ))
            asyncio.create_task(schedule_delete(m))
            return
        
        if txt == "Next Page ➜":
            s["page"] = 2
            save_settings(s)
            await main_menu(event)
            return
        elif txt == "◀ Previous Page":
            s["page"] = 1
            save_settings(s)
            await main_menu(event)
            return
        
        if uid == ADMIN_ID and uid in ADMIN_STATE:
            state = ADMIN_STATE.pop(uid)
            if state == "gen":
                try:
                    cr = int(txt)
                    code = generate_redeem_code(cr)
                    msg = await send_html(event.chat_id, simple_quote(
                        "ᴄᴏᴅᴇ ɢᴇɴᴇʀᴀᴛᴇᴅ",
                        [
                            f"<code>{code}</code>",
                            f"{E_CREDIT} <b>ᴄʀᴇᴅɪᴛꜱ:</b> {cr}"
                        ],
                        E_CHECK
                    ))
                except:
                    msg = await send_html(event.chat_id, simple_quote(
                        "ᴇʀʀᴏʀ",
                        "ɪɴᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ ꜰᴏʀᴍᴀᴛ!",
                        E_CROSS
                    ))
                asyncio.create_task(schedule_delete(msg))
                return
            elif state == "credit":
                p = txt.split()
                if len(p) >= 2:
                    bal = add_credits(p[0], int(p[1]))
                    msg = await send_html(event.chat_id, simple_quote(
                        "ᴄʀᴇᴅɪᴛꜱ ᴀᴅᴅᴇᴅ",
                        [
                            f"<b>ᴜꜱᴇʀ:</b> {p[0]}",
                            f"<b>ᴀᴅᴅᴇᴅ:</b> +{p[1]}",
                            f"<b>ɴᴇᴡ ʙᴀʟᴀɴᴄᴇ:</b> {bal}"
                        ],
                        E_CHECK
                    ))
                else:
                    msg = await send_html(event.chat_id, simple_quote(
                        "ᴇʀʀᴏʀ",
                        "ꜰᴏʀᴍᴀᴛ: <code>ᴜꜱᴇʀ_ɪᴅ ᴀᴍᴏᴜɴᴛ</code>",
                        E_CROSS
                    ))
                asyncio.create_task(schedule_delete(msg))
                return
            elif state == "bcast":
                users = load_json(USERS_FILE)
                cnt = 0
                for u in users:
                    try:
                        await send_html(int(u), simple_quote(
                            "ʙʀᴏᴀᴅᴄᴀꜱᴛ",
                            txt,
                            E_BOLT
                        ))
                        cnt += 1
                    except:
                        pass
                msg = await send_html(event.chat_id, simple_quote(
                    "ʙʀᴏᴀᴅᴄᴀꜱᴛ ꜱᴇɴᴛ",
                    f"<b>ᴅᴇʟɪᴠᴇʀᴇᴅ ᴛᴏ:</b> {cnt} ᴜꜱᴇʀꜱ",
                    E_CHECK
                ))
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
        
        if txt == "Admin Panel":
            await admin_panel(event)
            return
        
        if hasattr(event, 'redeem_mode') and event.redeem_mode:
            event.redeem_mode = False
            if txt.upper().startswith("HEX-"):
                success, msg = redeem_code(uid, txt)
                m = await send_html(event.chat_id, msg)
            else:
                m = await send_html(event.chat_id, simple_quote(
                    "ɪɴᴠᴀʟɪᴅ ᴄᴏᴅᴇ",
                    "ᴄᴏᴅᴇ ᴍᴜꜱᴛ ꜱᴛᴀʀᴛ ᴡɪᴛʜ <code>HEX-</code>",
                    E_CROSS
                ))
            asyncio.create_task(schedule_delete(m))
            return
        
        feature_map = {
            "IFSC Lookup": ("IFSC", "ifsc"),
            "Aadhar Lookup": ("AADHAAR", "aadhaar"),
            "India Number": ("MOBILE", "mobile"),
            "RC Check": ("VEHICLE", "rc"),
            "GST Verify": ("GST", "gst"),
            "Pakistan Number": ("PAK", "pak"),
            "Invite & Earn": ("INVITE", None),
            "Redeem Code": ("REDEEM", None)
        }
        
        if txt in feature_map:
            mode, feature = feature_map[txt]
            
            if mode == "INVITE":
                user = get_user(uid)
                bot_username = BOT_USERNAME
                link = f"https://t.me/{bot_username}?start={user['invite_code']}"
                
                invite_msg = simple_quote(
                    "ɪɴᴠɪᴛᴇ & ᴇᴀʀɴ",
                    [
                        f"{E_USERS} +{INVITE_CREDITS} ᴄʀᴇᴅɪᴛꜱ ᴘᴇʀ ɪɴᴠɪᴛᴇ",
                        f"{E_LINK} <a href='{link}'>{link}</a>"
                    ],
                    E_STAR
                )
                m = await send_html(event.chat_id, invite_msg)
                asyncio.create_task(schedule_delete(m, 120))
                return
            elif mode == "REDEEM":
                event.redeem_mode = True
                m = await send_html(event.chat_id, simple_quote(
                    "ʀᴇᴅᴇᴇᴍ ᴄᴏᴅᴇ",
                    "ꜱᴇɴᴅ ʏᴏᴜʀ ʀᴇᴅᴇᴇᴍ ᴄᴏᴅᴇ:\n<code>HEX-XXXXXXXXXX</code>",
                    E_TICKET
                ))
                asyncio.create_task(schedule_delete(m, 30))
                return
            
            if feature and not s.get(f"{feature}_enabled", True):
                m = await send_html(event.chat_id, simple_quote(
                    "ꜱᴇʀᴠɪᴄᴇ ᴅɪꜱᴀʙʟᴇᴅ",
                    "ᴛʜɪꜱ ꜱᴇʀᴠɪᴄᴇ ɪꜱ ᴄᴜʀʀᴇɴᴛʟʏ ᴅɪꜱᴀʙʟᴇᴅ.",
                    E_DISABLED
                ))
                asyncio.create_task(schedule_delete(m))
                return
            
            if feature:
                maint, msg = check_feature_maintenance(feature)
                if maint:
                    m = await send_html(event.chat_id, simple_quote(
                        "ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ",
                        msg,
                        E_TOOLS
                    ))
                    asyncio.create_task(schedule_delete(m))
                    return
            
            USER_MODES[str(uid)] = mode
            
            prompts = {
                "IFSC": {
                    "title": "ɪꜰꜱᴄ ʟᴏᴏᴋᴜᴘ",
                    "instruction": "ꜱᴇɴᴅ ɪꜰꜱᴄ ᴄᴏᴅᴇ",
                    "example": "SBIN0001234"
                },
                "AADHAAR": {
                    "title": "ᴀᴀᴅʜᴀʀ ʟᴏᴏᴋᴜᴘ",
                    "instruction": "ꜱᴇɴᴅ 12-ᴅɪɢɪᴛ ᴀᴀᴅʜᴀʀ ɴᴜᴍʙᴇʀ",
                    "example": "123456789012"
                },
                "MOBILE": {
                    "title": "ɴᴜᴍʙᴇʀ ɪɴꜰᴏ",
                    "instruction": "ꜱᴇɴᴅ 10-ᴅɪɢɪᴛ ᴍᴏʙɪʟᴇ ɴᴜᴍʙᴇʀ",
                    "example": "9876543210",
                    "tip": "ᴡɪᴛʜ ᴏʀ ᴡɪᴛʜᴏᴜᴛ +91"
                },
                "VEHICLE": {
                    "title": "ʀᴄ ᴄʜᴇᴄᴋ",
                    "instruction": "ꜱᴇɴᴅ ᴠᴇʜɪᴄʟᴇ ɴᴜᴍʙᴇʀ",
                    "example": "KA01AB3256"
                },
                "GST": {
                    "title": "ɢꜱᴛ ᴠᴇʀɪꜰʏ",
                    "instruction": "ꜱᴇɴᴅ ɢꜱᴛ ɴᴜᴍʙᴇʀ",
                    "example": "19BOKPS7056D1ZI"
                },
                "PAK": {
                    "title": "ᴘᴀᴋɪꜱᴛᴀɴ ɴᴜᴍʙᴇʀ",
                    "instruction": "ꜱᴇɴᴅ ᴘᴀᴋɪꜱᴛᴀɴ ɴᴜᴍʙᴇʀ",
                    "example": "923078750447"
                }
            }
            if mode in prompts:
                p = prompts[mode]
                m = await send_html(event.chat_id, info_quote(
                    p['title'],
                    p['instruction'],
                    p['example'],
                    p.get('tip', None)
                ))
                asyncio.create_task(schedule_delete(m))
            return
        
        uid_str = str(uid)
        if uid_str in USER_MODES and USER_MODES[uid_str]:
            mode = USER_MODES[uid_str]
            
            if txt.upper().startswith("HEX-"):
                success, msg = redeem_code(uid, txt)
                m = await send_html(event.chat_id, msg)
                asyncio.create_task(schedule_delete(m))
                USER_MODES[uid_str] = None
                return
            
            user = get_user(uid)
            if user.get("credits", 0) <= 0:
                m = await send_html(event.chat_id, simple_quote(
                    "ɪɴꜱᴜꜰꜰɪᴄɪᴇɴᴛ ᴄʀᴇᴅɪᴛꜱ",
                    [
                        "ɴᴏ ᴄʀᴇᴅɪᴛꜱ ʟᴇꜰᴛ!",
                        f"ɢᴇᴛ +{DAILY_FREE_CREDITS} ᴅᴀɪʟʏ",
                        f"+{INVITE_CREDITS} ᴘᴇʀ ɪɴᴠɪᴛᴇ"
                    ],
                    E_CROSS
                ))
                asyncio.create_task(schedule_delete(m))
                USER_MODES[uid_str] = None
                return
            
            await run_query(event, mode, txt)
            USER_MODES[uid_str] = None
            return
        
    except Exception as e:
        logger.error(f"Msg handler error: {e}")

async def run_query(event, mode, query):
    if not await net_ok():
        m = await send_html(event.chat_id, simple_quote(
            "ɴᴏ ɪɴᴛᴇʀɴᴇᴛ",
            "ᴘʟᴇᴀꜱᴇ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴄᴏɴɴᴇᴄᴛɪᴏɴ.",
            E_CROSS
        ))
        asyncio.create_task(schedule_delete(m))
        return
    
    st = await send_html(event.chat_id, simple_quote(
        "ꜱᴇᴀʀᴄʜɪɴɢ",
        "ᴘʀᴏᴄᴇꜱꜱɪɴɢ ʏᴏᴜʀ ʀᴇQᴜᴇꜱᴛ...",
        E_SEARCH
    ))
    
    for i in range(5):
        try:
            await edit_html(st, simple_quote(
                "ꜱᴇᴀʀᴄʜɪɴɢ",
                f"ᴘʀᴏᴄᴇꜱꜱɪɴɢ... {i+1}/5",
                E_SEARCH
            ))
            await asyncio.sleep(0.4)
        except:
            pass
    
    credit_deducted = False
    
    try:
        if mode in ['AADHAAR', 'MOBILE', 'VEHICLE']:
            choice_map = {'AADHAAR': '2', 'MOBILE': '1', 'VEHICLE': '4'}
            raw = run_india_script(choice_map[mode], query)
            if raw:
                records = parse_all_india_records(raw)
                result = format_records_result(records, {'AADHAAR': 'aadhaar', 'MOBILE': 'mobile', 'VEHICLE': 'vehicle'}[mode])
                if records and f"{E_CROSS}" not in str(result):
                    use_credit(event.sender_id)
                    credit_deducted = True
            else:
                result = simple_quote(
                    "ᴇʀʀᴏʀ",
                    "ꜱᴄʀɪᴘᴛ ꜰᴀɪʟᴇᴅ ᴛᴏ ᴇxᴇᴄᴜᴛᴇ.",
                    E_CROSS
                )
        else:
            async with aiohttp.ClientSession() as s:
                if mode == 'IFSC':
                    result = await ifsc_lookup(s, query)
                elif mode == 'GST':
                    result = await gst_lookup(s, query)
                elif mode == 'PAK':
                    result = await pakistan_lookup(s, query)
                else:
                    result = simple_quote(
                        "ᴇʀʀᴏʀ",
                        "ᴜɴᴋɴᴏᴡɴ ꜱᴇʀᴠɪᴄᴇ.",
                        E_CROSS
                    )
            
            if result and f"{E_CROSS}" not in str(result) and "unavailable" not in str(result).lower():
                use_credit(event.sender_id)
                credit_deducted = True
        
        user = get_user(event.sender_id)
        
        if f"{E_DIAMOND}" not in str(result):
            credit_line = f"{E_CREDIT} <b>ᴄʀᴇᴅɪᴛꜱ:</b> {user.get('credits', 0)}" if credit_deducted else "<b>ꜱᴛᴀᴛᴜꜱ:</b> ɴᴏ ᴄʀᴇᴅɪᴛ ᴅᴇᴅᴜᴄᴛᴇᴅ"
            final = f"{result}\n\n{credit_line}"
        else:
            final = result
        
        sent = await edit_html(st, final)
        asyncio.create_task(schedule_delete(sent))
    except Exception as e:
        logger.error(f"Query error: {e}")
        try:
            await edit_html(st, simple_quote(
                "ᴇʀʀᴏʀ",
                "ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ᴘʀᴏᴄᴇꜱꜱɪɴɢ.",
                E_WARN
            ))
        except:
            pass

# --- 📋 SHOW VERIFICATION ---

async def show_verification_page(event):
    try:
        txt = simple_quote(
            f"{BOT_NAME}",
            [
                f"@{BOT_USERNAME}",
                "",
                f"{E_LOCK} <b>ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ʀᴇQᴜɪʀᴇᴅ</b>",
                "ᴊᴏɪɴ ʙᴏᴛʜ ᴄʜᴀɴɴᴇʟꜱ ᴛᴏ ᴜɴʟᴏᴄᴋ",
                "",
                f"{E_STAR2} <b>ɢᴜɪᴅᴇʟɪɴᴇꜱ:</b>",
                "• ᴇᴅᴜᴄᴀᴛɪᴏɴᴀʟ ᴘᴜʀᴘᴏꜱᴇꜱ ᴏɴʟʏ",
                "• ᴜꜱᴇ ᴏɴ ʏᴏᴜʀ ᴏᴡɴ ᴅᴀᴛᴀ",
                "• ʀᴇꜱᴘᴇᴄᴛ ᴘʀɪᴠᴀᴄʏ ʟᴀᴡꜱ",
                "",
                f"{E_GIFT} +{DAILY_FREE_CREDITS} ᴅᴀɪʟʏ {E_STAR}",
                f"{E_USERS} +{INVITE_CREDITS} ᴘᴇʀ ɪɴᴠɪᴛᴇ",
                f"{E_CLOCK} {AUTO_DELETE_TIME}ꜱ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ",
                "",
                f"{E_CROWN} <b>ᴏᴡɴᴇʀ: @Hexh4ckerOFC</b>"
            ],
            E_DIAMOND
        )
        
        button1 = KeyboardButtonUrl(text="📢 JOIN CHANNEL 1", url=LINK_1)
        button2 = KeyboardButtonUrl(text="📢 JOIN CHANNEL 2", url=LINK_2)
        button3 = KeyboardButtonCallback(text="✅ I'VE JOINED - VERIFY", data=b"verify")
        
        markup = ReplyInlineMarkup(rows=[
            KeyboardButtonRow(buttons=[button1]),
            KeyboardButtonRow(buttons=[button2]),
            KeyboardButtonRow(buttons=[button3])
        ])
        
        await send_html(event.chat_id, txt, reply_markup=markup)
    except Exception as e:
        logger.error(f"Verification page error: {e}")

# --- 🚀 START ---

async def main():
    print("Hex OSINT Bot ULTIMATE EDITION")
    print("Premium UI with Unique Emojis")
    print("All features working!")
    
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