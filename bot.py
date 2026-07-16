# bot.py - Hex OSINT Bot with FF Guest Generator

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
import threading
import time
from datetime import datetime, timedelta
from io import BytesIO

try:
    from telethon import TelegramClient, events, functions
    from telethon.tl.types import (
        KeyboardButton, KeyboardButtonRow, ReplyKeyboardMarkup,
        KeyboardButtonStyle, KeyboardButtonCallback, ReplyInlineMarkup,
        KeyboardButtonUrl, InputFile
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
        KeyboardButtonUrl, InputFile
    )
    from telethon.tl.functions.channels import GetParticipantRequest
    from telethon.errors import UserNotParticipantError, ChannelPrivateError
    HAS_BUTTON_STYLE = True

# ---- Ensure pycryptodome is installed ----
try:
    import Crypto
except ImportError:
    print("Installing pycryptodome...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pycryptodome"], capture_output=True, timeout=30)

# ---- Import gen.py ----
GEN_AVAILABLE = False
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    from gen import generate_accounts, REGION_LANG
    GEN_AVAILABLE = True
    print("✅ gen.py imported successfully")
except ImportError as e:
    print(f"⚠️ gen.py import error: {e}. Guest Generator disabled.")
    REGION_LANG = {"ME":"ar","IND":"hi","ID":"id","VN":"vi","TH":"th","BD":"bn","PK":"ur","TW":"zh","CIS":"ru","SAC":"es","BR":"pt"}
    def generate_accounts(*args, **kwargs):
        return []

# --- ⚙️ CONFIGURATION ---
API_ID = int(os.environ.get('API_ID', '37996037'))
API_HASH = os.environ.get('API_HASH', '47ee9fa07b5eeb865edb3d79ada726a5')
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8687617595:AAFF6FP5XWr92RFhM0wco6UHutB7UGUpFFA')
ADMIN_ID = int(os.environ.get('ADMIN_ID', '7898928200'))

CHANNEL_1_ID = int(os.environ.get('CHANNEL_1_ID', '-1003240507339'))
CHANNEL_2_ID = int(os.environ.get('CHANNEL_2_ID', '-1003806004135'))

LINK_1 = os.environ.get('LINK_1', 'https://t.me/+dP7xLb3AoE1jNmRl')
LINK_2 = os.environ.get('LINK_2', 'https://t.me/+9vuPcr9LJ8piODdl')

FOOTER = "\n\n⚡ ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr ⭐"
SEP = "━━━━━━━━━━━━━━━━━━━"

# APIs
LOOKUP_API = "https://toxic-tg.vercel.app/?userid="
IFSC_API = "https://ifsc.razorpay.com/"
SHORTLINK_API = "https://link-btpass.onrender.com/bypass?key=9c44ad66b95cef8aecd7a99cfb362ce0&link="
GST_API = "https://gst-0y-vishal.vercel.app/api/gst.js?gstNumber="
PAK_API = "https://api-server-virid-two.vercel.app/number="
IND_NUM_API = "https://all-number-info-rajan-eta.vercel.app/api?number="
TG_INFO_API = "https://telegram-info-plum.vercel.app/api/search?q="

VERIFY_SCRIPT = "verify_india.py"

USERS_FILE = os.path.join(os.getcwd(), "users.json")
REDEEM_FILE = os.path.join(os.getcwd(), "redeem_codes.json")
SETTINGS_FILE = os.path.join(os.getcwd(), "settings.json")

DAILY_FREE_CREDITS = 10
INVITE_CREDITS = 3
AUTO_DELETE_TIME = 60

BOT_NAME = "𝗛𝗲𝘅 𝗢𝗦𝗜𝗡𝗧 𝗕𝗼𝘁"
BOT_USERNAME = "Hex_Terminal_bot"

# --- YOUR PREMIUM EMOJI IDs ---
PE = lambda eid, fallback: f'<tg-emoji emoji-id="{eid}">{fallback}</tg-emoji>'

# Your exact emoji IDs
E_DIAMOND = PE("6314557546753440004", "💎")
E_LION = PE("5802980697886954454", "🦁")
E_HAPPY = PE("6154369208076470797", "🥹")
E_WALLET = PE("5256186332669035163", "👛")
E_CROWN = PE("6267128480601741166", "👑")
E_CAMERA = PE("6008258140108231117", "📸")
E_ARROW = PE("5875450995332353523", "➡️")
E_DIAMOND2 = PE("4961143940817355662", "💠")
E_STAR = PE("5289898724976240966", "⭐")
E_BOLT = PE("5377834924776627189", "⚡")
E_POWERED = PE("6176952682989754426", "⚡")

# Service Emojis
E_IFSC = PE("5264895611517300926", "🏦")
E_AADHAAR = PE("5260561650213220533", "🪪")
E_INDIA = PE("6284779941489812433", "🇮🇳")
E_RC = PE("5253752975997803460", "🚘")
E_GST = PE("5260561650213220533", "📋")
E_PAK = PE("5913705895375672082", "🇵🇰")
E_TG = PE("5039783602301175152", "✈️")

# India Number Info Premium Emojis
E_INDIAN_NUMBER = PE("6109380284644329775", "🇮🇳")
E_CHART = PE("6093382540784046658", "📊")
E_USER = PE("5249053508681883137", "👤")
E_USER2 = PE("5258362837411045098", "👤")
E_USER3 = PE("5258011929993026890", "👤")
E_PHONE = PE("5967591100532134862", "☎️")
E_LOCATION = PE("5985361068157833495", "📍")
E_CIRCLE = PE("5472373721966597010", "🔴")
E_GMAIL = PE("5303416490295304868", "📧")

# TG User ID Info Premium Emojis
E_TG_USER = PE("5039783602301175152", "✈️")
E_COUNTRY = PE("5465166522030764559", "🐈‍⬛")
E_COUNTRY_CODE = PE("5422814644093868925", "👨‍💻")
E_PHONE_NUMBER = PE("5339534764367955381", "🌟")
E_TG_ID = PE("5936017305585586269", "🪪")

# Guest Generator Emoji
E_GUEST = PE("5802980697886954454", "🎮")

# Additional emojis
E_CHECK = PE("6267008582294705964", "✅")
E_CROSS = PE("6267000941547885720", "❌")
E_WARN = PE("6267039884016358504", "⚠️")
E_LOCK = PE("5316522278056399236", "🔒")
E_PHONE2 = PE("5406809207947142040", "📲")
E_BANK = PE("5264895611517300926", "🏦")
E_CAR = PE("5253752975997803460", "🚘")
E_CARD = PE("5260561650213220533", "🪪")
E_USERS = PE("5244933196230972438", "👥")
E_PAK2 = PE("5913705895375672082", "🇵🇰")
E_SEARCH = PE("5231012545799666522", "🔍")
E_CREDIT = PE("6267068789146260253", "💰")
E_REFRESH = PE("5375338737028841420", "🔄")
E_CLOCK = PE("5382194935057372936", "⏱")
E_BOLT2 = PE("6284971355297290197", "⚡")
E_GIFT = PE("5203996991054432397", "🎁")
E_TICKET = PE("5285515895534278367", "🎫")
E_TOOLS = PE("5462921117423384478", "🛠️")
E_DISABLED = PE("5373165973203348165", "📴")
E_HOME = PE("5280955052582785391", "🏠")
E_STATE = PE("5388927107315283144", "🏛")
E_NETWORK = PE("5321141214735508486", "📡")
E_SIGNAL = PE("6147892053796725336", "📶")
E_SIM = PE("5800717980266403037", "💳")
E_SPARKLE = PE("5467683093693354332", "✨")
E_ROCKET = PE("5195033767969839232", "🚀")
E_STAR2 = PE("6266969287638913443", "🌟")
E_LINK = PE("5271604874419647061", "🔗")
E_BABY = PE("6264785189394717307", "🍼")
E_GEAR = PE("5462921117423384478", "⚙️")
E_WELCOME = PE("6266969287638913443", "✨")
E_FATHER = PE("6147864334077794239", "👨")
E_UPGRADE = PE("6267128480601741166", "👑")

# --- BUTTON ICON IDs ---
ICON_IFSC = 5264895611517300926
ICON_AADHAAR = 5260561650213220533
ICON_INDIA = 6284779941489812433
ICON_RC = 5253752975997803460
ICON_GST = 5260561650213220533
ICON_PAK = 5913705895375672082
ICON_TG = 5039783602301175152
ICON_INVITE = 5244933196230972438
ICON_UPGRADE = 6267128480601741166
ICON_GUEST = 5802980697886954454
ICON_ADMIN = 6267128480601741166
ICON_NEXT = 5258331647358540449
ICON_PRIMARY = 5258096772776991776

# --- VERIFICATION BUTTON ICON IDs ---
ICON_JOIN1 = 5802980697886954454
ICON_JOIN2 = 6154369208076470797
ICON_VERIFY = 5289898724976240966

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
ADMIN_STATE = {}
USER_MODES = {}

# Guest generator state
GUEST_STATE = {}

# Global lock to prevent duplicate processing
processing_lock = asyncio.Lock()
processed_messages = set()

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
            "verified": False,
            "premium": False,
            "started": False
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
            "tgid_enabled": True,
            "guest_enabled": True if GEN_AVAILABLE else False,
            "maintenance_mode": False,
            "page": 1
        }
        for k in ["ifsc", "mobile", "aadhaar", "rc", "gst", "pak", "tgid", "guest"]:
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

async def show_verification_page(event):
    try:
        txt = (
            f"<blockquote>{E_DIAMOND} {BOT_NAME} {E_DIAMOND}\n\n"
            f"@{BOT_USERNAME}\n\n"
            f"{E_LOCK} <b>VERIFICATION REQUIRED</b>\n\n"
            f"JOIN BOTH CHANNELS TO UNLOCK\n\n"
            f"{E_GIFT} +{DAILY_FREE_CREDITS} DAILY {E_STAR}\n\n"
            f"{E_USERS} +{INVITE_CREDITS} PER INVITE\n\n"
            f"{E_CLOCK} {AUTO_DELETE_TIME}s AUTO DELETE\n\n"
            f"{E_CROWN} <b>OWNER: @HeX_CiPhEr</b></blockquote>"
        )
        
        style1 = KeyboardButtonStyle(
            bg_primary=True,
            icon=ICON_JOIN1
        )
        button1 = KeyboardButtonUrl(
            text="JOIN CHANNEL 1",
            url=LINK_1,
            style=style1
        )
        
        style2 = KeyboardButtonStyle(
            bg_success=True,
            icon=ICON_JOIN2
        )
        button2 = KeyboardButtonUrl(
            text="JOIN CHANNEL 2",
            url=LINK_2,
            style=style2
        )
        
        style3 = KeyboardButtonStyle(
            bg_danger=True,
            icon=ICON_VERIFY
        )
        button3 = KeyboardButtonCallback(
            text="VERIFY",
            data=b"verify",
            style=style3
        )
        
        markup = ReplyInlineMarkup(rows=[
            KeyboardButtonRow(buttons=[button1]),
            KeyboardButtonRow(buttons=[button2]),
            KeyboardButtonRow(buttons=[button3])
        ])
        
        await send_html(event.chat_id, txt, reply_markup=markup)
    except Exception as e:
        logger.error(f"Verification page error: {e}")

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
            row1.append(create_colored_button("Iғsᴄ Iɴғᴏ", 'primary', ICON_IFSC))
        if settings.get("aadhaar_enabled", True):
            row1.append(create_colored_button("Aᴀᴅʜᴀʀ Iɴғᴏ", 'primary', ICON_AADHAAR))
        if row1:
            rows.append(KeyboardButtonRow(buttons=row1))
        
        row2 = []
        if settings.get("mobile_enabled", True):
            row2.append(create_colored_button("Iɴᴅɪᴀ Nᴜᴍʙᴇʀ Iɴғᴏ", 'primary', ICON_INDIA))
        if settings.get("rc_enabled", True):
            row2.append(create_colored_button("Rᴄ Iɴғᴏ", 'primary', ICON_RC))
        if row2:
            rows.append(KeyboardButtonRow(buttons=row2))
        
        row3 = []
        if settings.get("gst_enabled", True):
            row3.append(create_colored_button("Gsᴛ Iɴғᴏ", 'primary', ICON_GST))
        if settings.get("pak_enabled", True):
            row3.append(create_colored_button("Pᴀᴋ Nᴜᴍʙᴇʀ Iɴғᴏ", 'primary', ICON_PAK))
        if row3:
            rows.append(KeyboardButtonRow(buttons=row3))
        
        row4 = []
        if settings.get("tgid_enabled", True):
            row4.append(create_colored_button("Tɢ Usᴇʀ Iᴅ Iɴғᴏ", 'primary', ICON_TG))
        if row4:
            rows.append(KeyboardButtonRow(buttons=row4))
        
        # ---- GUEST GENERATOR BUTTON ----
        if GEN_AVAILABLE and settings.get("guest_enabled", True):
            row5 = []
            row5.append(create_colored_button("Fғ Gᴜᴇsᴛ Gᴇɴ", 'primary', ICON_GUEST))
            if row5:
                rows.append(KeyboardButtonRow(buttons=row5))
        # ---------------------------------
        
        rows.append(KeyboardButtonRow(buttons=[
            create_colored_button("Iɴᴠɪᴛᴇ & Eᴀʀɴ", 'primary', ICON_INVITE),
            create_colored_button("Uᴘɢʀᴀᴅᴇ Tᴏ Pʀᴇᴍɪᴜᴍ", 'primary', ICON_UPGRADE)
        ]))
        
        next_row = []
        next_row.append(create_colored_button("Nᴇxᴛ Pᴀɢᴇ ➜", 'danger', ICON_NEXT))
        if is_admin:
            next_row.append(create_colored_button("Aᴅᴍɪɴ Pᴀɴᴇʟ", 'danger', ICON_ADMIN))
        rows.append(KeyboardButtonRow(buttons=next_row))
    
    else:
        prev_row = []
        prev_row.append(create_colored_button("◀ Pʀᴇᴠɪᴏᴜs Pᴀɢᴇ", 'danger', ICON_NEXT))
        if is_admin:
            prev_row.append(create_colored_button("Aᴅᴍɪɴ Pᴀɴᴇʟ", 'danger', ICON_ADMIN))
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
            'State': 'STATE',
            'GMAIL': 'GMAIL',
            'Email': 'GMAIL'
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
        return f"<blockquote>{E_CROSS} NO RECORDS FOUND</blockquote>"
    
    title_map = {
        'aadhaar': f'{E_AADHAAR} AADHAR',
        'mobile': f'{E_INDIAN_NUMBER} INDIAN NUMBER',
        'vehicle': f'{E_RC} VEHICLE'
    }
    title = title_map.get(search_type, f'{E_CHART} RESULT')
    
    result = f"<blockquote>{E_SPARKLE} {title} {E_SPARKLE}\n\n"
    result += f"{E_CHART} TOTAL: {len(records)}\n\n"
    
    field_emojis = {
        'NAME': E_USER2,
        'FATHER': E_USER3,
        'MOBILE': E_PHONE,
        'ADDRESS': E_LOCATION,
        'CIRCLE': E_CIRCLE,
        'STATE': E_STATE,
        'GMAIL': E_GMAIL
    }
    
    for i, record in enumerate(records, 1):
        result += f"━━ {E_USER} RECORD {i} ━━\n\n"
        for key, value in record.items():
            emoji = field_emojis.get(key, E_USER)
            result += f"{emoji} {key}: {value}\n\n"
    
    result += f"{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"
    return result

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
        return f"<blockquote>{E_CROSS} SERVICE UNAVAILABLE</blockquote>"
    if isinstance(data, dict):
        return (f"<blockquote>{E_SPARKLE} {E_IFSC} BANK IFSC DETAILS {E_SPARKLE}\n\n"
                f"{E_BANK} BANK: {data.get('BANK','N/A')}\n\n"
                f"{E_LOCATION} BRANCH: {data.get('BRANCH','N/A')}\n\n"
                f"{E_CARD} IFSC: {data.get('IFSC',code.upper())}\n\n"
                f"{E_LOCATION} ADDRESS: {data.get('ADDRESS','N/A')}\n\n"
                f"{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>")
    return f"<blockquote>{E_CROSS} INVALID CODE</blockquote>"

async def gst_lookup(session, gst_number):
    data = await safe_api_fetch(session, f"{GST_API}{gst_number.upper()}", timeout=20)
    if not data or isinstance(data, dict) and data.get("raw_text"):
        return f"<blockquote>{E_CROSS} SERVICE UNAVAILABLE</blockquote>"
    if isinstance(data, dict) and data.get("status") == "success" and data.get("data"):
        d = data["data"]
        result = f"<blockquote>{E_SPARKLE} {E_GST} GST INFO {E_SPARKLE}\n\n"
        if d.get('TradeName'):
            result += f"{E_BANK} BUSINESS: {d['TradeName']}\n\n"
        if d.get('Gstin'):
            result += f"{E_CARD} GST: {d['Gstin']}\n\n"
        result += f"{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"
        return result
    return f"<blockquote>{E_CROSS} INVALID GST</blockquote>"

async def pakistan_lookup(session, number):
    try:
        data = await safe_api_fetch(session, f"{PAK_API}{number}", timeout=20)
        if not data or isinstance(data, dict) and data.get("raw_text"):
            return f"<blockquote>{E_CROSS} SERVICE UNAVAILABLE</blockquote>"
        if isinstance(data, dict) and data.get("success") and data.get("data"):
            valid = [r for r in data["data"] if isinstance(r, dict) and any(r.get(k) for k in ['name', 'number', 'cnic', 'address'])]
            if not valid:
                return f"<blockquote>{E_CROSS} NO DATA</blockquote>"
            result = f"<blockquote>{E_SPARKLE} {E_PAK} PAKISTAN NUMBER INFO {E_SPARKLE}\n\n"
            for i, r in enumerate(valid[:3], 1):
                if len(valid) > 1:
                    result += f"━━ {E_USER} RECORD {i} ━━\n\n"
                if r.get('number'):
                    result += f"{E_PHONE2} PHONE: {r['number']}\n\n"
                if r.get('name'):
                    result += f"{E_USER} NAME: {r['name']}\n\n"
                if r.get('cnic'):
                    result += f"{E_CARD} CNIC: {r['cnic']}\n\n"
                if r.get('address'):
                    result += f"{E_LOCATION} ADDRESS: {r['address'][:200]}\n\n"
            result += f"{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"
            return result
        return f"<blockquote>{E_CROSS} NO DATA</blockquote>"
    except:
        return f"<blockquote>{E_CROSS} ERROR</blockquote>"

async def tg_user_info(session, query):
    try:
        url = f"{TG_INFO_API}{query}"
        data = await safe_api_fetch(session, url, timeout=20)
        if not data or isinstance(data, dict) and data.get("raw_text"):
            return f"<blockquote>{E_CROSS} SERVICE UNAVAILABLE</blockquote>"
        if isinstance(data, dict) and data.get("success") and data.get("data"):
            d = data["data"]
            result = (
                f"<blockquote>{E_SPARKLE} {E_TG_USER} Usᴇʀɴᴀᴍᴇ / Iᴅ Iɴғᴏ {E_SPARKLE}\n\n"
                f"{E_COUNTRY} Cᴏᴜɴᴛʀʏ: {d.get('country', 'N/A')}\n\n"
                f"{E_COUNTRY_CODE} Cᴏᴜɴᴛʀʏ Cᴏᴅᴇ: {d.get('country_code', 'N/A')}\n\n"
                f"{E_PHONE_NUMBER} Pʜᴏɴᴇ Nᴜᴍʙᴇʀ: {d.get('phone_number', 'N/A')}\n\n"
                f"{E_TG_ID} Tᴇʟᴇɢʀᴀᴍ Iᴅ: {d.get('telegram_id', query)}\n\n"
                f"{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"
            )
            return result
        return f"<blockquote>{E_CROSS} NO DATA FOUND</blockquote>"
    except Exception as e:
        logger.error(f"TG User Info error: {e}")
        return f"<blockquote>{E_CROSS} ERROR: {str(e)}</blockquote>"

# --- 👑 ADMIN ---

async def admin_panel(event):
    if event.sender_id != ADMIN_ID:
        return
    s = get_settings()
    ms = lambda key: "❌" if s.get(f"maint_{key}") else "✅"
    
    buttons = [
        [KeyboardButtonCallback(text="🎫 Gen Code", data=b"ad_gen"), KeyboardButtonCallback(text="📋 Codes", data=b"ad_codes")],
        [KeyboardButtonCallback(text="🎁 Add Credits", data=b"ad_credit"), KeyboardButtonCallback(text="📢 Broadcast", data=b"ad_bcast")],
        [KeyboardButtonCallback(text=f"{'🔴' if s.get('maintenance_mode') else '🟢'} Global", data=b"ad_maint")],
        [KeyboardButtonCallback(text=f"{'🟢' if s.get('ifsc_enabled',True) else '🔴'} IF", data=b"ad_ifsc"), KeyboardButtonCallback(text=f"{ms('ifsc')} M", data=b"ad_maint_ifsc")],
        [KeyboardButtonCallback(text=f"{'🟢' if s.get('mobile_enabled',True) else '🔴'} MO", data=b"ad_mobile"), KeyboardButtonCallback(text=f"{ms('mobile')} M", data=b"ad_maint_mobile")],
        [KeyboardButtonCallback(text=f"{'🟢' if s.get('aadhaar_enabled',True) else '🔴'} AA", data=b"ad_aadhaar"), KeyboardButtonCallback(text=f"{ms('aadhaar')} M", data=b"ad_maint_aadhaar")],
        [KeyboardButtonCallback(text=f"{'🟢' if s.get('rc_enabled',True) else '🔴'} RC", data=b"ad_rc"), KeyboardButtonCallback(text=f"{ms('rc')} M", data=b"ad_maint_rc")],
        [KeyboardButtonCallback(text=f"{'🟢' if s.get('gst_enabled',True) else '🔴'} GS", data=b"ad_gst"), KeyboardButtonCallback(text=f"{ms('gst')} M", data=b"ad_maint_gst")],
        [KeyboardButtonCallback(text=f"{'🟢' if s.get('pak_enabled',True) else '🔴'} PA", data=b"ad_pak"), KeyboardButtonCallback(text=f"{ms('pak')} M", data=b"ad_maint_pak")],
        [KeyboardButtonCallback(text=f"{'🟢' if s.get('tgid_enabled',True) else '🔴'} TG", data=b"ad_tgid"), KeyboardButtonCallback(text=f"{ms('tgid')} M", data=b"ad_maint_tgid")],
        [KeyboardButtonCallback(text=f"{'🟢' if s.get('guest_enabled',True) else '🔴'} GU", data=b"ad_guest"), KeyboardButtonCallback(text=f"{ms('guest')} M", data=b"ad_maint_guest")] if GEN_AVAILABLE else [],
        [KeyboardButtonCallback(text="❌ Close", data=b"ad_close")]
    ]
    
    rows = []
    for row in buttons:
        if row:
            rows.append(KeyboardButtonRow(buttons=row))
    
    markup = ReplyInlineMarkup(rows=rows)
    
    txt = f"<blockquote>👑 ADMIN PANEL\n\n👥 USERS: {len(load_json(USERS_FILE))} | 🎫 CODES: {len(load_json(REDEEM_FILE))}\n\n{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"
    
    if hasattr(event, 'data'):
        await event.edit(txt, buttons=markup)
    else:
        await send_html(event.chat_id, txt, reply_markup=markup)

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
        txt = f"<blockquote>🎫 CODES: {len(codes)}\n\n"
        for c, v in list(codes.items())[-15:]:
            txt += f"{'✅' if not v.get('used') else '❌'} {c} | {v.get('credits')}cr\n\n"
        txt += f"{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"
        from telethon.tl.types import KeyboardButtonCallback, ReplyInlineMarkup, KeyboardButtonRow
        await event.edit(txt, buttons=ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text="🔙 Back", data=b"ad_back")])]))
    elif d == "ad_gen":
        ADMIN_STATE[event.sender_id] = "gen"
        from telethon.tl.types import KeyboardButtonCallback, ReplyInlineMarkup, KeyboardButtonRow
        await event.edit(f"<blockquote>🎫 ENTER CREDITS:\n\n100\n\n{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>", buttons=ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text="🔙 Back", data=b"ad_back")])]))
    elif d == "ad_credit":
        ADMIN_STATE[event.sender_id] = "credit"
        from telethon.tl.types import KeyboardButtonCallback, ReplyInlineMarkup, KeyboardButtonRow
        await event.edit(f"<blockquote>🎁 ENTER ID AMOUNT:\n\n123456789 50\n\n{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>", buttons=ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text="🔙 Back", data=b"ad_back")])]))
    elif d == "ad_bcast":
        ADMIN_STATE[event.sender_id] = "bcast"
        from telethon.tl.types import KeyboardButtonCallback, ReplyInlineMarkup, KeyboardButtonRow
        await event.edit(f"<blockquote>📢 ENTER MESSAGE:\n\n{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>", buttons=ReplyInlineMarkup(rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text="🔙 Back", data=b"ad_back")])]))
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
            "ad_pak": "pak_enabled",
            "ad_tgid": "tgid_enabled",
            "ad_guest": "guest_enabled"
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

# --- 🚀 GUEST GENERATOR INTEGRATION ---

async def send_json_direct(chat_id, data, filename, caption=""):
    """Send JSON data as a file without saving to disk"""
    try:
        if not data or len(data) == 0:
            return False
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        json_bytes = json_str.encode('utf-8')
        bio = BytesIO(json_bytes)
        bio.seek(0)
        await client.send_file(
            chat_id,
            bio,
            file_name=filename,
            caption=caption,
            parse_mode='html'
        )
        return True
    except Exception as e:
        logger.error(f"send_json_direct error: {e}")
        return False

def run_guest_generation(chat_id, region, is_ghost, name_prefix, password_prefix, total):
    """Run guest generation in a separate thread and send results using asyncio"""
    if not GEN_AVAILABLE:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(send_html(
            chat_id,
            f"<blockquote>{E_CROSS} Guest Generator is not available.\n\n"
            f"Please ensure gen.py and pycryptodome are installed.\n\n"
            f"{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"
        ))
        loop.close()
        return
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        # Send start message
        loop.run_until_complete(send_html(
            chat_id,
            f"<blockquote>{E_GUEST} Fғ Gᴜᴇsᴛ Gᴇɴ {E_GUEST}\n\n"
            f"<b>Region:</b> {region} {'(GHOST)' if is_ghost else ''}\n"
            f"<b>Name Prefix:</b> {name_prefix}\n"
            f"<b>Password Prefix:</b> {password_prefix}\n"
            f"<b>Total:</b> {total} accounts\n"
            f"<b>Threads:</b> 100 (ULTRA SPEED!)\n\n"
            f"{E_SEARCH} Generating... Please wait.</blockquote>"
        ))
        
        # Collect results
        accounts = []
        rare_accounts = []
        couple_pairs = []
        rare_count = 0
        couple_count = 0
        
        def progress_callback(account_data, is_rare, is_couple, reason, partner):
            nonlocal rare_count, couple_count
            accounts.append(account_data)
            if is_rare:
                rare_count += 1
                rare_accounts.append({
                    "account": account_data,
                    "reason": reason,
                    "score": account_data.get('rarity_score', 0)
                })
            if is_couple and partner:
                couple_count += 1
                couple_pairs.append({
                    "account1": account_data,
                    "account2": partner,
                    "reason": reason
                })
        
        # Start generation
        start_time = time.time()
        generated = generate_accounts(
            region=region,
            name_prefix=name_prefix,
            password_prefix=password_prefix,
            total=total,
            is_ghost=is_ghost,
            progress_callback=progress_callback
        )
        elapsed = time.time() - start_time
        
        # Ensure we have accounts from the callback (or from the return value)
        if not accounts and generated:
            accounts = generated
            # Also extract rare/couple from generated? Not needed, but we'll just rely on callback.
        
        # Send summary
        summary_msg = (
            f"<blockquote>{E_CHECK} Gᴇɴᴇʀᴀᴛɪᴏɴ Cᴏᴍᴘʟᴇᴛᴇ!\n\n"
            f"<b>Total Accounts:</b> {len(accounts)}\n"
            f"<b>Rare Found:</b> {rare_count}\n"
            f"<b>Couple Pairs:</b> {couple_count}\n"
            f"<b>Time:</b> {elapsed:.2f}s\n\n"
            f"{E_CREDIT} Sending JSON files...</blockquote>"
        )
        loop.run_until_complete(send_html(chat_id, summary_msg))
        
        # Send JSON files
        if accounts:
            sent = loop.run_until_complete(send_json_direct(chat_id, accounts, f"guest_accounts_{region}.json", f"📁 {len(accounts)} accounts"))
            if sent:
                loop.run_until_complete(send_html(chat_id, f"<blockquote>✅ Accounts file sent ({len(accounts)} accounts)</blockquote>"))
        if rare_accounts:
            sent = loop.run_until_complete(send_json_direct(chat_id, rare_accounts, f"guest_rare_{region}.json", f"⭐ {rare_count} rare accounts"))
            if sent:
                loop.run_until_complete(send_html(chat_id, f"<blockquote>✅ Rare file sent ({rare_count} rare)</blockquote>"))
        if couple_pairs:
            sent = loop.run_until_complete(send_json_direct(chat_id, couple_pairs, f"guest_couples_{region}.json", f"💑 {couple_count} couples"))
            if sent:
                loop.run_until_complete(send_html(chat_id, f"<blockquote>✅ Couples file sent ({couple_count} couples)</blockquote>"))
        
        # Send combined file
        full_data = {
            "generated_at": datetime.now().isoformat(),
            "region": region,
            "is_ghost": is_ghost,
            "total": len(accounts),
            "rare_count": rare_count,
            "couple_count": couple_count,
            "accounts": accounts
        }
        sent = loop.run_until_complete(send_json_direct(chat_id, full_data, f"guest_full_{region}.json", "📦 Complete data"))
        if sent:
            loop.run_until_complete(send_html(chat_id, f"<blockquote>✅ Full combined file sent</blockquote>"))
        
        loop.run_until_complete(send_html(
            chat_id,
            f"<blockquote>{E_DIAMOND} Aʟʟ ғɪʟᴇs sᴇɴᴛ! {E_DIAMOND}\n\n"
            f"{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"
        ))
        
    except Exception as e:
        logger.error(f"Guest generation error: {e}")
        loop.run_until_complete(send_html(
            chat_id,
            f"<blockquote>{E_CROSS} Gᴇɴᴇʀᴀᴛɪᴏɴ Fᴀɪʟᴇᴅ\n\n"
            f"Error: {str(e)}\n\n"
            f"{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"
        ))
    finally:
        loop.close()

# --- 🚀 HANDLERS ---

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    async with processing_lock:
        try:
            uid = event.sender_id
            
            user = get_user(uid)
            user["started"] = True
            save_user(uid, user)
            
            args = event.message.message.split()
            if len(args) > 1 and args[1].startswith("HEX-"):
                users = load_json(USERS_FILE)
                for inviter, data in users.items():
                    if data.get("invite_code") == args[1] and inviter != str(uid):
                        cr = process_invite(inviter, uid)
                        try:
                            await send_html(int(inviter), f"<blockquote>{E_GIFT} +{cr} CREDITS! NEW USER JOINED!\n\n{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>")
                        except:
                            pass
                        break
            
            await send_welcome(event)
            
        except Exception as e:
            logger.error(f"Start: {e}")
            await main_menu(event)

async def send_welcome(event):
    try:
        cr = get_user(event.sender_id).get('credits', 0)
        name = event.sender.first_name or "User"
        
        caption = (
            f"<blockquote>{E_DIAMOND} Hᴇx Osɪɴᴛ Bᴏᴛ {E_LION}\n\n"
            f"{E_HAPPY} ᴡᴇʟᴄᴏᴍᴇ {name}! {E_HAPPY}\n\n"
            f"{E_WALLET} ᴄʀᴇᴅɪᴛꜱ: {cr}\n\n"
            f"{E_CROWN} ᴘʀᴇᴍɪᴜᴍ: ᴜɴʟɪᴍɪᴛᴇᴅ\n\n"
            f"{E_CAMERA} ᴜꜱᴇ ᴛʜᴇ ʙᴜᴛᴛᴏɴꜱ ʙᴇʟᴏᴡ\n\n"
            f"{E_ARROW} /Help ꜰᴏʀ ᴄᴏᴍᴍᴀɴᴅꜱ\n\n"
            f"{E_DIAMOND2} ꜱᴇʟᴇᴄᴛ ᴀ ꜱᴇʀᴠɪᴄᴇ ʙᴇʟᴏᴡ\n\n"
            f"{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"
        )
        
        is_admin = event.sender_id == ADMIN_ID
        markup = create_main_menu(is_admin, get_settings())
        
        msg = await send_html(event.chat_id, caption, reply_markup=markup)
        asyncio.create_task(schedule_delete(msg, AUTO_DELETE_TIME))
        
    except Exception as e:
        logger.error(f"Send welcome error: {e}")
        await main_menu(event)

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
            await send_welcome(event)
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
async def admin_callback_handler(event):
    if event.data and event.data.startswith(b"ad_"):
        await admin_callback(event)

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
    
    welcome_text = (
        f"<blockquote>{E_DIAMOND} Hᴇx Osɪɴᴛ Bᴏᴛ {E_LION}\n\n"
        f"{E_HAPPY} ᴡᴇʟᴄᴏᴍᴇ {name}! {E_HAPPY}\n\n"
        f"{E_WALLET} ᴄʀᴇᴅɪᴛꜱ: {cr}\n\n"
        f"{E_CROWN} ᴘʀᴇᴍɪᴜᴍ: ᴜɴʟɪᴍɪᴛᴇᴅ\n\n"
        f"{E_CAMERA} ᴜꜱᴇ ᴛʜᴇ ʙᴜᴛᴛᴏɴꜱ ʙᴇʟᴏᴡ\n\n"
        f"{E_ARROW} /Help ꜰᴏʀ ᴄᴏᴍᴍᴀɴᴅꜱ\n\n"
        f"{E_DIAMOND2} ꜱᴇʟᴇᴄᴛ ᴀ ꜱᴇʀᴠɪᴄᴇ ʙᴇʟᴏᴡ\n\n"
        f"{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"
    )
    
    msg = await send_html(event.chat_id, welcome_text, reply_markup=markup)
    asyncio.create_task(schedule_delete(msg, AUTO_DELETE_TIME))

@client.on(events.NewMessage)
async def msg_handler(event):
    async with processing_lock:
        try:
            uid = event.sender_id
            txt = event.message.message.strip()
            
            if not txt:
                return
            
            if txt.startswith('/start'):
                return
            
            msg_id = event.message.id
            if msg_id in processed_messages:
                return
            processed_messages.add(msg_id)
            
            if len(processed_messages) > 500:
                processed_messages.clear()
            
            # Group handling
            if event.is_group:
                user = get_user(uid)
                if not user.get("started", False):
                    return
            
            # Auto-delete user message (except /start)
            asyncio.create_task(schedule_delete(event.message, AUTO_DELETE_TIME))
            
            s = get_settings()
            
            if s.get("maintenance_mode", False) and uid != ADMIN_ID:
                m = await send_html(event.chat_id, f"<blockquote>{E_TOOLS} Under maintenance\n\n{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>")
                asyncio.create_task(schedule_delete(m))
                return
            
            # Page navigation
            if txt == "Nᴇxᴛ Pᴀɢᴇ ➜":
                s["page"] = 2
                save_settings(s)
                await main_menu(event)
                return
            elif txt == "◀ Pʀᴇᴠɪᴏᴜs Pᴀɢᴇ":
                s["page"] = 1
                save_settings(s)
                await main_menu(event)
                return
            
            # Admin states
            if uid == ADMIN_ID and uid in ADMIN_STATE:
                state = ADMIN_STATE.pop(uid)
                if state == "gen":
                    try:
                        cr = int(txt)
                        code = generate_redeem_code(cr)
                        msg = await send_html(event.chat_id, f"<blockquote>{E_CHECK} {code} | {E_CREDIT} {cr}cr\n\n{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>")
                    except:
                        msg = await send_html(event.chat_id, f"<blockquote>{E_CROSS} Number\n\n{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>")
                    asyncio.create_task(schedule_delete(msg))
                    return
                elif state == "credit":
                    p = txt.split()
                    if len(p) >= 2:
                        bal = add_credits(p[0], int(p[1]))
                        msg = await send_html(event.chat_id, f"<blockquote>{E_CHECK} +{p[1]} | {bal}\n\n{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>")
                    else:
                        msg = await send_html(event.chat_id, f"<blockquote>{E_CROSS} Format: ID AMOUNT\n\n{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>")
                    asyncio.create_task(schedule_delete(msg))
                    return
                elif state == "bcast":
                    users = load_json(USERS_FILE)
                    cnt = 0
                    for u in users:
                        try:
                            await send_html(int(u), f"<blockquote>{E_BOLT} {txt}\n\n{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>")
                            cnt += 1
                        except:
                            pass
                    msg = await send_html(event.chat_id, f"<blockquote>{E_CHECK} Sent: {cnt}\n\n{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>")
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
            
            # Admin Panel
            if txt == "Aᴅᴍɪɴ Pᴀɴᴇʟ":
                await admin_panel(event)
                return
            
            # ---- GUEST GENERATOR FLOW ----
            if txt == "Fғ Gᴜᴇsᴛ Gᴇɴ":
                if not GEN_AVAILABLE:
                    await send_html(event.chat_id, f"<blockquote>{E_CROSS} Guest Generator is disabled.\n\nPlease ensure gen.py and pycryptodome are installed.</blockquote>")
                    return
                # Start guest generator flow
                GUEST_STATE[uid] = {"step": "region"}
                await send_guest_region_menu(event)
                return
            
            # Handle guest generator steps
            if uid in GUEST_STATE:
                state = GUEST_STATE[uid]
                step = state.get("step")
                
                if step == "region":
                    if txt.upper() in REGION_LANG or txt.upper() == "GHOST":
                        region = txt.upper()
                        is_ghost = region == "GHOST"
                        if is_ghost:
                            region = "BR"
                        state["region"] = region
                        state["is_ghost"] = is_ghost
                        state["step"] = "name"
                        await send_html(event.chat_id, f"<blockquote>✅ Region set to <b>{region}</b> {'(GHOST)' if is_ghost else ''}\n\n📝 Enter <b>Name Prefix</b> (e.g., JXE):</blockquote>")
                    else:
                        await send_html(event.chat_id, f"<blockquote>❌ Invalid region. Please select from the inline buttons.</blockquote>")
                    return
                
                elif step == "name":
                    state["name"] = txt
                    state["step"] = "password"
                    await send_html(event.chat_id, f"<blockquote>✅ Name prefix set to <b>{txt}</b>\n\n📝 Enter <b>Password Prefix</b> (e.g., JXE2026):</blockquote>")
                    return
                
                elif step == "password":
                    state["password"] = txt
                    state["step"] = "total"
                    await send_html(event.chat_id, f"<blockquote>✅ Password prefix set to <b>{txt}</b>\n\n📝 Enter <b>Total Accounts</b> (number):</blockquote>")
                    return
                
                elif step == "total":
                    if txt.isdigit() and int(txt) > 0:
                        total = int(txt)
                        state["total"] = total
                        region = state["region"]
                        is_ghost = state["is_ghost"]
                        name_prefix = state["name"]
                        password_prefix = state["password"]
                        
                        # Start generation in a separate thread
                        chat_id = event.chat_id
                        threading.Thread(
                            target=run_guest_generation,
                            args=(chat_id, region, is_ghost, name_prefix, password_prefix, total),
                            daemon=True
                        ).start()
                        
                        # Clear state
                        del GUEST_STATE[uid]
                        
                        await send_html(event.chat_id, f"<blockquote>🚀 Starting ULTRA SPEED generation with {total} accounts...\n\nResults will appear here.</blockquote>")
                    else:
                        await send_html(event.chat_id, f"<blockquote>❌ Please enter a valid positive number.</blockquote>")
                    return
                else:
                    del GUEST_STATE[uid]
                    await send_html(event.chat_id, f"<blockquote>⚠️ Session reset. Please click Fғ Gᴜᴇsᴛ Gᴇɴ again.</blockquote>")
                    return
            
            # ---- OTHER FEATURES ----
            if hasattr(event, 'upgrade_mode') and event.upgrade_mode:
                event.upgrade_mode = False
                m = await send_html(event.chat_id, 
                    f"<blockquote>{E_UPGRADE} Premium Upgrade\n\n"
                    f"Contact @HeX_CiPhEr for premium access!\n\n"
                    f"{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"
                )
                asyncio.create_task(schedule_delete(m))
                return
            
            feature_map = {
                "Iғsᴄ Iɴғᴏ": ("IFSC", "ifsc"),
                "Aᴀᴅʜᴀʀ Iɴғᴏ": ("AADHAAR", "aadhaar"),
                "Iɴᴅɪᴀ Nᴜᴍʙᴇʀ Iɴғᴏ": ("MOBILE", "mobile"),
                "Rᴄ Iɴғᴏ": ("VEHICLE", "rc"),
                "Gsᴛ Iɴғᴏ": ("GST", "gst"),
                "Pᴀᴋ Nᴜᴍʙᴇʀ Iɴғᴏ": ("PAK", "pak"),
                "Tɢ Usᴇʀ Iᴅ Iɴғᴏ": ("TGID", "tgid"),
                "Iɴᴠɪᴛᴇ & Eᴀʀɴ": ("INVITE", None),
                "Uᴘɢʀᴀᴅᴇ Tᴏ Pʀᴇᴍɪᴜᴍ": ("UPGRADE", None)
            }
            
            if txt in feature_map:
                mode, feature = feature_map[txt]
                
                if mode == "INVITE":
                    user = get_user(uid)
                    bot_username = BOT_USERNAME
                    link = f"https://t.me/{bot_username}?start={user['invite_code']}"
                    
                    invite_msg = (
                        f"<blockquote>{E_STAR} Invite & Earn {E_STAR}\n\n"
                        f"{E_USERS} +{INVITE_CREDITS} Credits per invite\n\n"
                        f"{E_LINK} {link}\n\n"
                        f"{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"
                    )
                    m = await send_html(event.chat_id, invite_msg)
                    asyncio.create_task(schedule_delete(m, 120))
                    return
                elif mode == "UPGRADE":
                    event.upgrade_mode = True
                    m = await send_html(event.chat_id, 
                        f"<blockquote>{E_UPGRADE} Uᴘɢʀᴀᴅᴇ Tᴏ Pʀᴇᴍɪᴜᴍ\n\n"
                        f"Contact @HeX_CiPhEr to upgrade your account!\n\n"
                        f"🌟 Premium Benefits:\n\n"
                        f"• Unlimited Credits\n\n"
                        f"• All Services Access\n\n"
                        f"• Priority Support\n\n"
                        f"• Exclusive Features\n\n"
                        f"{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"
                    )
                    asyncio.create_task(schedule_delete(m, 60))
                    return
                
                if feature and not s.get(f"{feature}_enabled", True):
                    m = await send_html(event.chat_id, f"<blockquote>{E_DISABLED} Disabled\n\n{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>")
                    asyncio.create_task(schedule_delete(m))
                    return
                
                if feature:
                    maint, msg = check_feature_maintenance(feature)
                    if maint:
                        m = await send_html(event.chat_id, f"<blockquote>{E_TOOLS} {msg}\n\n{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>")
                        asyncio.create_task(schedule_delete(m))
                        return
                
                USER_MODES[str(uid)] = mode
                
                user = get_user(uid)
                credits = user.get("credits", 0)
                
                prompts = {
                    "IFSC": (
                        f"<blockquote>{E_IFSC} Iғsᴄ Iɴғᴏ\n\n"
                        f"Send IFSC code\n\n"
                        f"Example: SBIN0001234\n\n"
                        f"{E_WALLET} Your Credits: {credits}\n\n"
                        f"Search Cost: 1 Point\n\n"
                        f"{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"
                    ),
                    "AADHAAR": (
                        f"<blockquote>{E_AADHAAR} Aᴀᴅʜᴀʀ Iɴғᴏ\n\n"
                        f"Send 12-digit Aadhar number\n\n"
                        f"Example: 123456789012\n\n"
                        f"{E_WALLET} Your Credits: {credits}\n\n"
                        f"Search Cost: 1 Point\n\n"
                        f"{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"
                    ),
                    "MOBILE": (
                        f"<blockquote>{E_INDIA} Iɴᴅɪᴀ Nᴜᴍʙᴇʀ Iɴғᴏ\n\n"
                        f"Send 10-digit mobile number\n\n"
                        f"Example: 9876543210\n\n"
                        f"Tip: with or without +91\n\n"
                        f"{E_WALLET} Your Credits: {credits}\n\n"
                        f"Search Cost: 1 Point\n\n"
                        f"{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"
                    ),
                    "VEHICLE": (
                        f"<blockquote>{E_RC} Rᴄ Iɴғᴏ\n\n"
                        f"Send vehicle number\n\n"
                        f"Example: KA01AB3256\n\n"
                        f"{E_WALLET} Your Credits: {credits}\n\n"
                        f"Search Cost: 1 Point\n\n"
                        f"{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"
                    ),
                    "GST": (
                        f"<blockquote>{E_GST} Gsᴛ Iɴғᴏ\n\n"
                        f"Send GST number\n\n"
                        f"Example: 19BOKPS7056D1ZI\n\n"
                        f"{E_WALLET} Your Credits: {credits}\n\n"
                        f"Search Cost: 1 Point\n\n"
                        f"{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"
                    ),
                    "PAK": (
                        f"<blockquote>{E_PAK} Pᴀᴋ Nᴜᴍʙᴇʀ Iɴғᴏ\n\n"
                        f"Send Pakistan number\n\n"
                        f"Example: 923078750447\n\n"
                        f"{E_WALLET} Your Credits: {credits}\n\n"
                        f"Search Cost: 1 Point\n\n"
                        f"{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"
                    ),
                    "TGID": (
                        f"<blockquote>{E_TG} Tɢ Usᴇʀ Iᴅ Iɴғᴏ\n\n"
                        f"Send Telegram username or chat ID\n\n"
                        f"Example: @username or 123456789\n\n"
                        f"{E_WALLET} Your Credits: {credits}\n\n"
                        f"Search Cost: 1 Point\n\n"
                        f"{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"
                    )
                }
                if mode in prompts:
                    m = await send_html(event.chat_id, prompts[mode])
                    asyncio.create_task(schedule_delete(m))
                return
            
            # Query mode
            uid_str = str(uid)
            if uid_str in USER_MODES and USER_MODES[uid_str]:
                mode = USER_MODES[uid_str]
                
                user = get_user(uid)
                if user.get("credits", 0) <= 0:
                    m = await send_html(event.chat_id, 
                        f"<blockquote>{E_CROSS} No credits! +10 daily | +3 invite\n\n{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"
                    )
                    asyncio.create_task(schedule_delete(m))
                    USER_MODES[uid_str] = None
                    return
                
                await run_query(event, mode, txt)
                USER_MODES[uid_str] = None
                return
            
        except Exception as e:
            logger.error(f"Msg handler error: {e}")

# --- GUEST GENERATOR REGION MENU ---

async def send_guest_region_menu(event):
    keyboard = [
        [KeyboardButtonCallback(text="🇮🇳 IND", data=b"g_region_IND")],
        [KeyboardButtonCallback(text="🇮🇩 ID", data=b"g_region_ID")],
        [KeyboardButtonCallback(text="🇻🇳 VN", data=b"g_region_VN")],
        [KeyboardButtonCallback(text="🇹🇭 TH", data=b"g_region_TH")],
        [KeyboardButtonCallback(text="🇧🇩 BD", data=b"g_region_BD")],
        [KeyboardButtonCallback(text="🇵🇰 PK", data=b"g_region_PK")],
        [KeyboardButtonCallback(text="🇹🇼 TW", data=b"g_region_TW")],
        [KeyboardButtonCallback(text="🇷🇺 CIS", data=b"g_region_CIS")],
        [KeyboardButtonCallback(text="🇪🇸 SAC", data=b"g_region_SAC")],
        [KeyboardButtonCallback(text="🇸🇦 ME", data=b"g_region_ME")],
        [KeyboardButtonCallback(text="👻 GHOST", data=b"g_region_GHOST")],
        [KeyboardButtonCallback(text="🔙 Back", data=b"g_region_back")]
    ]
    markup = ReplyInlineMarkup(rows=[
        KeyboardButtonRow(buttons=row) for row in keyboard
    ])
    await send_html(event.chat_id, f"<blockquote>{E_GUEST} Sᴇʟᴇᴄᴛ Rᴇɢɪᴏɴ:\n\nChoose your region below:</blockquote>", reply_markup=markup)

@client.on(events.CallbackQuery)
async def guest_region_callback(event):
    if event.data and event.data.startswith(b"g_region_"):
        data = event.data.decode()
        region = data.replace("g_region_", "")
        uid = event.sender_id
        
        if region == "back":
            await event.answer()
            await main_menu(event)
            return
        
        is_ghost = region == "GHOST"
        if is_ghost:
            region = "BR"
        
        GUEST_STATE[uid] = {
            "step": "name",
            "region": region,
            "is_ghost": is_ghost
        }
        
        await event.answer(f"Region set to {region}{' (GHOST)' if is_ghost else ''}")
        await send_html(event.chat_id, f"<blockquote>✅ Region set to <b>{region}</b> {'(GHOST)' if is_ghost else ''}\n\n📝 Enter <b>Name Prefix</b> (e.g., JXE):</blockquote>")
    else:
        await event.answer()

# --- QUERY RUNNER ---

async def run_query(event, mode, query):
    if not await net_ok():
        m = await send_html(event.chat_id, f"<blockquote>{E_CROSS} No internet\n\n{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>")
        asyncio.create_task(schedule_delete(m))
        return
    
    st = await send_html(event.chat_id, f"<blockquote>{E_SEARCH} Searching...\n\n{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>")
    
    for i in range(5):
        try:
            await edit_html(st, f"<blockquote>{E_SEARCH} Searching... {i+1}/5\n\n{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>")
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
                result = f"<blockquote>{E_CROSS} Script failed\n\n{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"
        elif mode == 'TGID':
            async with aiohttp.ClientSession() as s:
                result = await tg_user_info(s, query)
                if result and f"{E_CROSS}" not in str(result) and "NO DATA" not in str(result):
                    use_credit(event.sender_id)
                    credit_deducted = True
        else:
            async with aiohttp.ClientSession() as s:
                if mode == 'IFSC':
                    result = await ifsc_lookup(s, query)
                elif mode == 'GST':
                    result = await gst_lookup(s, query)
                elif mode == 'PAK':
                    result = await pakistan_lookup(s, query)
                else:
                    result = f"<blockquote>{E_CROSS}\n\n{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>"
            
            if result and f"{E_CROSS}" not in str(result) and "unavailable" not in str(result).lower():
                use_credit(event.sender_id)
                credit_deducted = True
        
        user = get_user(event.sender_id)
        
        if f"{E_POWERED}" not in str(result):
            final = f"{result}\n\n{E_CREDIT} {'Credits: '+str(user.get('credits',0)) if credit_deducted else 'No credit deducted'} | {E_CLOCK} {AUTO_DELETE_TIME}s\n\n{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}"
        else:
            final = result
        
        sent = await edit_html(st, final)
        asyncio.create_task(schedule_delete(sent))
    except Exception as e:
        logger.error(f"Query error: {e}")
        try:
            await edit_html(st, f"<blockquote>{E_WARN} Error\n\n{E_POWERED} ᴘᴏᴡᴇʀᴇᴅ ʙʏ @HeX_CiPhEr {E_STAR}</blockquote>")
        except:
            pass

# --- 🚀 START ---

async def main():
    print("Hex OSINT Bot ULTIMATE EDITION")
    print("Premium UI with Unique Emojis")
    print("All features working!")
    print("Group Mode: Only users who /start the bot will get responses")
    print("Welcome message auto-deletes after 60 seconds")
    print("Buttons work without /start - just click and use!")
    print("Double message issue FIXED with Async Lock!")
    if GEN_AVAILABLE:
        print("Guest Generator integrated - click Fғ Gᴜᴇsᴛ Gᴇɴ!")
    else:
        print("WARNING: Guest Generator disabled - gen.py not found or missing dependencies.")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "requests", "beautifulsoup4", "pycryptodome"], capture_output=True, timeout=30)
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