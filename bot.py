import os
import json
import random
import string
import re
import subprocess
import sys
import asyncio
import aiohttp
import socket
import logging
from datetime import datetime, timedelta
from telethon import TelegramClient, events, types, functions
from telethon.tl.types import (
    KeyboardButton, KeyboardButtonRow, ReplyKeyboardMarkup,
    KeyboardButtonStyle, InlineKeyboardButton, InlineKeyboardMarkup
)
from telethon.tl.functions.messages import SendMessageRequest
from telethon.errors import FloodWaitError

# --- ⚙️ CONFIGURATION ---
API_ID = int(os.environ.get('API_ID', 37996037))
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

# --- ✨ PREMIUM EMOJI IDs (ONLY PREMIUM) ---
class PE:
    WARN = 6267039884016358504
    CHECK = 6267008582294705964
    CROSS = 6267000941547885720
    LOCK = 5316522278056399236
    CROWN = 6267128480601741166
    DIAMOND = 6264791387032523779
    STAR = 6266969287638913443
    GIFT = 5203996991054432397
    FIRE = 6264785189394717307
    SEARCH = 5231012545799666522
    PHONE = 5947494995798789024
    BANK = 5264895611517300926
    LINK = 5271604874419647061
    CAR = 5253752975997803460
    CARD = 5260561650213220533
    USER = 5249053508681883137
    INDIA = 6284779941489812433
    PAK = 5913705895375672082
    PHONE2 = 5406809207947142040
    INVITE = 5244933196230972438
    TICKET = 5285515895534278367
    CREDIT = 6267068789146260253
    REFRESH = 5375338737028841420
    CLOCK = 5382194935057372936
    BOLT = 6284971355297290197
    GREEN = 5386367538735104399
    BLACK = 5116476703002068797
    SPARKLE = 5467683093693354332
    ROCKET = 5195033767969839232
    TOOLS = 5462921117423384478
    DISABLED = 5373165973203348165
    FATHER = 6147864334077794239
    LOCATION = 5391032818111363540
    HOME = 5280955052582785391
    STATE = 5388927107315283144
    NETWORK = 5321141214735508486
    SIGNAL = 6147892053796725336
    SIM = 5800717980266403037
    CHART = 6093382540784046658
    GEAR = 5262134534896436357
    MAIL = 5297816573556689764
    COIN = 5307077157342543949
    BADGE = 5349477894550511516
    BILL = 5265601992776937247
    DOC = 5289314750013930927
    FOLDER = 5368497354294036643
    ID = 5238076457718436745
    KEY = 5291968206369912314
    LAMP = 5354337745946281263
    MAP = 5300053950136136756
    MEDAL = 5355423384075428120
    MIC = 5319820620225375107
    NOTE = 5275739058930435436
    PENCIL = 5259654107486588105
    PIN = 5271793367066998890
    PLUG = 5288517004034893602
    SAFETY = 5270697957290760927
    SCREEN = 5286838831749281457
    SHIELD = 5305997404020861726
    STOP = 5268825774288158927
    TAG = 5326060413402520055
    TARGET = 5230028571960305539
    TERMINAL = 5236113873541560391
    TOGGLE = 5307214073187705107
    TRASH = 5343056267305822928
    UNLOCK = 5346959239569121175
    WALLET = 5269430531761766871
    WIFI = 5376112708136611090
    ZAP = 5293105696191372779
    ZOOM = 5254451205458872103

# --- 📱 Color Button Styles ---
class ButtonStyles:
    @staticmethod
    def primary(text, icon=None):
        return KeyboardButton(
            text=text,
            style=KeyboardButtonStyle(bg_primary=True, icon=icon)
        )
    
    @staticmethod
    def success(text, icon=None):
        return KeyboardButton(
            text=text,
            style=KeyboardButtonStyle(bg_success=True, icon=icon)
        )
    
    @staticmethod
    def danger(text, icon=None):
        return KeyboardButton(
            text=text,
            style=KeyboardButtonStyle(bg_danger=True, icon=icon)
        )
    
    @staticmethod
    def secondary(text, icon=None):
        return KeyboardButton(
            text=text,
            style=KeyboardButtonStyle(bg_secondary=True, icon=icon)
        )

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
            "invite_code": f"HEX-{''.join(random.choices(string.ascii_uppercase + string.digits, k=8))}",
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
    code = f"HEX-{''.join(random.choices(string.ascii_uppercase + string.digits, k=10))}"
    codes = load_json(REDEEM_FILE)
    codes[code] = {
        "credits": credits,
        "used": False,
        "created": datetime.now().isoformat()
    }
    save_json(REDEEM_FILE, codes)
    return code

def redeem_code(uid, code):
    codes = load_json(REDEEM_FILE)
    code = code.upper().strip()
    if code not in codes:
        return False, "❌ ɪɴᴠᴀʟɪᴅ ᴄᴏᴅᴇ"
    if codes[code].get("used"):
        return False, "❌ ᴀʟʀᴇᴀᴅʏ ᴜꜱᴇᴅ"
    cr = codes[code]["credits"]
    codes[code]["used"] = True
    codes[code]["used_by"] = str(uid)
    save_json(REDEEM_FILE, codes)
    bal = add_credits(uid, cr)
    return True, f"✅ +{cr} ᴄʀᴇᴅɪᴛꜱ ᴀᴅᴅᴇᴅ!\n💰 ʙᴀʟᴀɴᴄᴇ: {bal}"

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
            d[f"maint_msg_{k}"] = f"🛠️ {k} is under maintenance."
            d[f"maint_{k}"] = False
        save_json(SETTINGS_FILE, d)
        return d

def save_settings(data):
    save_json(SETTINGS_FILE, data)

# --- 🔍 VERIFY ---
async def check_channels(uid, client):
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

async def delete_after(msg, delay=AUTO_DELETE_TIME):
    await asyncio.sleep(delay)
    try:
        await msg.delete()
    except:
        pass

async def send_with_delete(client, chat_id, text, **kwargs):
    try:
        msg = await client.send_message(chat_id, text, **kwargs)
        asyncio.create_task(delete_after(msg, AUTO_DELETE_TIME))
        return msg
    except Exception as e:
        return None

def format_text_with_emoji(text, emoji_id, fallback=""):
    return f'<tg-emoji emoji-id="{emoji_id}">{fallback}</tg-emoji> {text}'

def emoji_text(emoji_id, fallback=""):
    return f'<tg-emoji emoji-id="{emoji_id}">{fallback}</tg-emoji>'

# --- 🎨 Premium Reply Keyboard Builder ---
class PremiumKeyboard:
    @staticmethod
    def build_main_menu(user, is_admin=False):
        s = get_settings()
        buttons = []
        
        # Row 1: TG ID & IFSC
        row1 = []
        if s.get("tgid_enabled", True):
            row1.append(ButtonStyles.primary(
                "📱 ᴛɢ ɪᴅ ➜ 📞 ɴᴜᴍʙᴇʀ",
                icon=PE.PHONE
            ))
        if s.get("ifsc_enabled", True):
            row1.append(ButtonStyles.success(
                "🏦 ɪꜰꜱᴄ ɪɴꜰᴏ",
                icon=PE.BANK
            ))
        if row1:
            buttons.append(KeyboardButtonRow(buttons=row1))
        
        # Row 2: Link Bypass
        if s.get("bypass_enabled", True):
            buttons.append(KeyboardButtonRow(buttons=[
                ButtonStyles.secondary(
                    "🔗 ʟɪɴᴋ ʙʏᴘᴀꜱꜱ",
                    icon=PE.LINK
                )
            ]))
        
        # Row 3: Aadhaar & India Number
        row3 = []
        if s.get("aadhaar_enabled", True):
            row3.append(ButtonStyles.primary(
                "🪪 ᴀᴀᴅʜᴀʀ ɪɴꜰᴏ",
                icon=PE.CARD
            ))
        if s.get("mobile_enabled", True):
            row3.append(ButtonStyles.success(
                "🇮🇳 ɪɴᴅ ɴᴜᴍʙᴇʀ",
                icon=PE.INDIA
            ))
        if row3:
            buttons.append(KeyboardButtonRow(buttons=row3))
        
        # Row 4: RC & GST
        row4 = []
        if s.get("rc_enabled", True):
            row4.append(ButtonStyles.secondary(
                "🚘 ʀᴄ ᴅᴇᴛᴀɪʟꜱ",
                icon=PE.CAR
            ))
        if s.get("gst_enabled", True):
            row4.append(ButtonStyles.danger(
                "📋 ɢꜱᴛ ʟᴏᴏᴋᴜᴘ",
                icon=PE.DOC
            ))
        if row4:
            buttons.append(KeyboardButtonRow(buttons=row4))
        
        # Row 5: Pakistan & India Num 2
        row5 = []
        if s.get("pak_enabled", True):
            row5.append(ButtonStyles.primary(
                "🇵🇰 ᴘᴀᴋ ɴᴜᴍʙᴇʀ",
                icon=PE.PAK
            ))
        if s.get("indnum_enabled", True):
            row5.append(ButtonStyles.success(
                "📲 ɪɴᴅ ɴᴜᴍ ɪɴꜰᴏ 𝟸",
                icon=PE.PHONE2
            ))
        if row5:
            buttons.append(KeyboardButtonRow(buttons=row5))
        
        # Row 6: India Number 3
        if s.get("indnum3_enabled", True):
            buttons.append(KeyboardButtonRow(buttons=[
                ButtonStyles.danger(
                    "🇮🇳 ɪɴᴅ ɴᴜᴍʙᴇʀ 𝟹",
                    icon=PE.SEARCH
                )
            ]))
        
        # Row 7: Invite & Redeem
        buttons.append(KeyboardButtonRow(buttons=[
            ButtonStyles.secondary(
                "👥 ɪɴᴠɪᴛᴇ & ᴇᴀʀɴ",
                icon=PE.INVITE
            ),
            ButtonStyles.success(
                "🎫 ʀᴇᴅᴇᴇᴍ",
                icon=PE.TICKET
            )
        ]))
        
        # Row 8: Admin Panel (if admin)
        if is_admin:
            buttons.append(KeyboardButtonRow(buttons=[
                ButtonStyles.danger(
                    "👑 ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ",
                    icon=PE.CROWN
                )
            ]))
        
        return ReplyKeyboardMarkup(rows=buttons, resize=True)

    @staticmethod
    def build_verification_buttons():
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    text="📢 ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ 𝟷",
                    url=LINK_1
                )
            ],
            [
                InlineKeyboardButton(
                    text="📢 ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ 𝟸",
                    url=LINK_2
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ ɪ'ᴠᴇ ᴊᴏɪɴᴇᴅ - ᴠᴇʀɪꜰʏ",
                    callback_data="verify"
                )
            ]
        ])

    @staticmethod
    def build_admin_panel(s):
        ms = lambda key: "🔴" if s.get(f"maint_{key}") else "🟢"
        
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🎫 ɢᴇɴ ᴄᴏᴅᴇ", callback_data="ad_gen"),
                InlineKeyboardButton("📋 ᴄᴏᴅᴇꜱ", callback_data="ad_codes")
            ],
            [
                InlineKeyboardButton("🎁 ᴀᴅᴅ ᴄʀ", callback_data="ad_credit"),
                InlineKeyboardButton("📢 ʙᴄᴀꜱᴛ", callback_data="ad_bcast")
            ],
            [
                InlineKeyboardButton(
                    f"{'🔴' if s.get('maintenance_mode') else '🟢'} ɢʟᴏʙᴀʟ",
                    callback_data="ad_maint"
                )
            ],
            [
                InlineKeyboardButton(
                    f"{'🟢' if s.get('tgid_enabled', True) else '🔴'} ᴛɢ",
                    callback_data="ad_tgid"
                ),
                InlineKeyboardButton(
                    f"{ms('tgid')} ᴍ",
                    callback_data="ad_maint_tgid"
                )
            ],
            [
                InlineKeyboardButton(
                    f"{'🟢' if s.get('ifsc_enabled', True) else '🔴'} ɪꜰ",
                    callback_data="ad_ifsc"
                ),
                InlineKeyboardButton(
                    f"{ms('ifsc')} ᴍ",
                    callback_data="ad_maint_ifsc"
                )
            ],
            [
                InlineKeyboardButton(
                    f"{'🟢' if s.get('bypass_enabled', True) else '🔴'} ʙʏ",
                    callback_data="ad_bypass_toggle"
                ),
                InlineKeyboardButton(
                    f"{ms('bypass')} ᴍ",
                    callback_data="ad_maint_bypass"
                )
            ],
            [
                InlineKeyboardButton(
                    f"{'🟢' if s.get('mobile_enabled', True) else '🔴'} ᴍᴏ",
                    callback_data="ad_mobile"
                ),
                InlineKeyboardButton(
                    f"{ms('mobile')} ᴍ",
                    callback_data="ad_maint_mobile"
                )
            ],
            [
                InlineKeyboardButton(
                    f"{'🟢' if s.get('aadhaar_enabled', True) else '🔴'} ᴀᴀ",
                    callback_data="ad_aadhaar"
                ),
                InlineKeyboardButton(
                    f"{ms('aadhaar')} ᴍ",
                    callback_data="ad_maint_aadhaar"
                )
            ],
            [
                InlineKeyboardButton(
                    f"{'🟢' if s.get('rc_enabled', True) else '🔴'} ʀᴄ",
                    callback_data="ad_rc"
                ),
                InlineKeyboardButton(
                    f"{ms('rc')} ᴍ",
                    callback_data="ad_maint_rc"
                )
            ],
            [
                InlineKeyboardButton(
                    f"{'🟢' if s.get('gst_enabled', True) else '🔴'} ɢꜱ",
                    callback_data="ad_gst"
                ),
                InlineKeyboardButton(
                    f"{ms('gst')} ᴍ",
                    callback_data="ad_maint_gst"
                )
            ],
            [
                InlineKeyboardButton(
                    f"{'🟢' if s.get('pak_enabled', True) else '🔴'} ᴘᴀ",
                    callback_data="ad_pak"
                ),
                InlineKeyboardButton(
                    f"{ms('pak')} ᴍ",
                    callback_data="ad_maint_pak"
                )
            ],
            [
                InlineKeyboardButton(
                    f"{'🟢' if s.get('indnum_enabled', True) else '🔴'} ɪɴ2",
                    callback_data="ad_indnum"
                ),
                InlineKeyboardButton(
                    f"{ms('indnum')} ᴍ",
                    callback_data="ad_maint_indnum"
                )
            ],
            [
                InlineKeyboardButton(
                    f"{'🟢' if s.get('indnum3_enabled', True) else '🔴'} ɪɴ3",
                    callback_data="ad_indnum3"
                ),
                InlineKeyboardButton(
                    f"{ms('indnum3')} ᴍ",
                    callback_data="ad_maint_indnum3"
                )
            ],
            [
                InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ", callback_data="ad_close")
            ]
        ])

# --- 🔗 API Functions ---
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
        return "❌ ꜱᴇʀᴠɪᴄᴇ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ"
    if isinstance(data, dict) and not data.get("raw_text") and data.get("success"):
        d = data.get("data", data)
        if isinstance(d, dict):
            result = "✨ 📞 ᴛᴇʟᴇɢʀᴀᴍ ɪᴅ ɪɴꜰᴏ ✨\n"
            if d.get('chat_id') or d.get('userid'):
                result += f"🔍 ᴄʜᴀᴛ ɪᴅ: <code>{d.get('chat_id', d.get('userid', query))}</code>\n"
            if d.get('number'):
                result += f"📲 ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ: <code>{d['number']}</code>\n"
            if d.get('name'):
                result += f"👤 ᴘʀᴏꜰɪʟᴇ ɴᴀᴍᴇ: <code>{d['name']}</code>\n"
            return result
    return "❌ ɴᴏᴛ ꜰᴏᴜɴᴅ"

async def ifsc_lookup(session, code):
    data = await safe_api_fetch(session, f"{IFSC_API}{code.upper()}")
    if not data or isinstance(data, dict) and data.get("raw_text"):
        return "❌ ꜱᴇʀᴠɪᴄᴇ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ"
    if isinstance(data, dict):
        return (
            f"✨ 🏦 ʙᴀɴᴋ ɪꜰꜱᴄ ᴅᴇᴛᴀɪʟꜱ ✨\n"
            f"🏦 ʙᴀɴᴋ ɴᴀᴍᴇ: <code>{data.get('BANK', 'N/A')}</code>\n"
            f"📍 ʙʀᴀɴᴄʜ: <code>{data.get('BRANCH', 'N/A')}</code>\n"
            f"🪪 ɪꜰꜱᴄ ᴄᴏᴅᴇ: <code>{data.get('IFSC', code.upper())}</code>\n"
            f"📍 ᴀᴅᴅʀᴇꜱꜱ: <code>{data.get('ADDRESS', 'N/A')}</code>"
        )
    return "❌ ɪɴᴠᴀʟɪᴅ ᴄᴏᴅᴇ"

async def bypass_lookup(session, link):
    s = get_settings()
    if s.get("bypass_maintenance", False):
        return "🛠️ ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ"
    data = await safe_api_fetch(session, f"{SHORTLINK_API}{link}", timeout=20)
    if not data or isinstance(data, dict) and data.get("raw_text"):
        return "❌ ꜱᴇʀᴠɪᴄᴇ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ"
    if isinstance(data, dict):
        r = data.get('bypassed_url') or data.get('url') or str(data)
        return f"✨ 🔗 ʟɪɴᴋ ʙʏᴘᴀꜱꜱᴇᴅ ✨\n🔗 ᴏʀɪɢɪɴᴀʟ ᴜʀʟ: <code>{str(r)}</code>"
    return f"🔗 ʀᴇꜱᴜʟᴛ: <code>{str(data)}</code>"

async def gst_lookup(session, gst_number):
    data = await safe_api_fetch(session, f"{GST_API}{gst_number.upper()}", timeout=20)
    if not data or isinstance(data, dict) and data.get("raw_text"):
        return "❌ ꜱᴇʀᴠɪᴄᴇ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ"
    if isinstance(data, dict) and data.get("status") == "success" and data.get("data"):
        d = data["data"]
        result = "✨ 🪪 ɢꜱᴛ ʙᴜꜱɪɴᴇꜱꜱ ɪɴꜰᴏ ✨\n"
        if d.get('TradeName'):
            result += f"🏦 ʙᴜꜱɪɴᴇꜱꜱ ɴᴀᴍᴇ: <code>{d['TradeName']}</code>\n"
        if d.get('Gstin'):
            result += f"🪪 ɢꜱᴛ ɴᴜᴍʙᴇʀ: <code>{d['Gstin']}</code>\n"
        return result
    return "❌ ɪɴᴠᴀʟɪᴅ ɢꜱᴛ"

async def pakistan_lookup(session, number):
    try:
        data = await safe_api_fetch(session, f"{PAK_API}{number}", timeout=20)
        if not data or isinstance(data, dict) and data.get("raw_text"):
            return "❌ ꜱᴇʀᴠɪᴄᴇ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ"
        if isinstance(data, dict) and data.get("success") and data.get("data"):
            valid = [r for r in data["data"] if isinstance(r, dict) and any(r.get(k) for k in ['name', 'number', 'cnic', 'address'])]
            if not valid:
                return "❌ ɴᴏ ᴅᴀᴛᴀ"
            result = "✨ 🇵🇰 ᴘᴀᴋɪꜱᴛᴀɴ ɴᴜᴍʙᴇʀ ɪɴꜰᴏ ✨\n"
            for i, r in enumerate(valid[:3], 1):
                if len(valid) > 1:
                    result += f"\n━━ 👤 ʀᴇᴄᴏʀᴅ {i} ━━\n"
                if r.get('number'):
                    result += f"📲 ᴘʜᴏɴᴇ: <code>{r['number']}</code>\n"
                if r.get('name'):
                    result += f"👤 ɴᴀᴍᴇ: <code>{r['name']}</code>\n"
                if r.get('cnic'):
                    result += f"🪪 ᴄɴɪᴄ: <code>{r['cnic']}</code>\n"
                if r.get('address'):
                    result += f"📍 ᴀᴅᴅʀᴇꜱꜱ: <code>{r['address'][:200]}</code>\n"
            return result
        return "❌ ɴᴏ ᴅᴀᴛᴀ"
    except:
        return "❌ ᴇʀʀᴏʀ"

async def indnum_lookup(session, number):
    for attempt in range(3):
        data = await safe_api_fetch(session, f"{IND_NUM_API}{number}", timeout=30)
        if data and isinstance(data, dict) and not data.get("raw_text") and data.get("results"):
            break
        if attempt < 2:
            await asyncio.sleep(2)
    if not data or isinstance(data, dict) and data.get("raw_text"):
        return "❌ ꜱᴇʀᴠɪᴄᴇ ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ"
    results = data.get("results", {})
    if not results:
        return "❌ ɴᴏ ʀᴇꜱᴜʟᴛꜱ"
    result = "✨ 📲 ɪɴᴅɪᴀɴ ɴᴜᴍʙᴇʀ ᴀᴅᴠᴀɴᴄᴇᴅ ✨\n📲 ɴᴜᴍʙᴇʀ: <code>{number}</code>\n"
    found = False
    s3 = results.get("source_3", {}).get("data", {})
    if isinstance(s3, dict):
        for k, e in [("SIM card", "💳"), ("Connection", "📶"), ("Mobile State", "📍"), ("Hometown", "🏠")]:
            if s3.get(k):
                result += f"{e} {k}: <code>{str(s3[k])[:200]}</code>\n"
                found = True
    s4 = results.get("source_4", {}).get("data", {})
    if isinstance(s4, dict) and s4.get("carrier"):
        result += f"📡 ᴄᴀʀʀɪᴇʀ: <code>{s4['carrier']}</code>\n"
        found = True
    return result if found else "❌ ɴᴏ ᴅᴀᴛᴀ"

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
                return "❌ ᴇᴍᴘᴛʏ ʀᴇꜱᴘᴏɴꜱᴇ"
            try:
                data = json.loads(text)
                if isinstance(data, dict):
                    result = "✨ 🇮🇳 ɪɴᴅɪᴀɴ ɴᴜᴍʙᴇʀ ᴛʀᴀᴄᴋɪɴɢ ✨\n📲 ɴᴜᴍʙᴇʀ: <code>{number}</code>\n"
                    for k, v in data.items():
                        if v and str(v).strip():
                            result += f"🔍 {k}: <code>{str(v)[:200]}</code>\n"
                    return result
            except:
                pass
            clean = re.sub(r'<[^>]+>', '\n', text)
            lines = [l.strip() for l in clean.split('\n') if l.strip() and len(l.strip()) > 1]
            result = "✨ 🇮🇳 ɪɴᴅɪᴀɴ ɴᴜᴍʙᴇʀ ᴛʀᴀᴄᴋɪɴɢ ✨\n📲 ɴᴜᴍʙᴇʀ: <code>{number}</code>\n"
            found = 0
            for line in lines[:20]:
                if ':' in line:
                    parts = line.split(':', 1)
                    key, val = parts[0].strip(), parts[1].strip() if len(parts) > 1 else ''
                    if val:
                        e = "👤" if any(w in key.lower() for w in ['name', 'nama']) else "📡" if any(w in key.lower() for w in ['carrier', 'operator', 'network', 'sim']) else "📍" if any(w in key.lower() for w in ['location', 'address', 'city', 'state', 'area']) else "📲" if any(w in key.lower() for w in ['phone', 'mobile', 'number', 'no']) else "🔍"
                        result += f"{e} {key}: <code>{val[:200]}</code>\n"
                        found += 1
            if found == 0:
                result += f"🪪 ʀᴀᴡ ᴅᴀᴛᴀ: <code>{clean[:500]}</code>\n"
            return result
    except:
        return "❌ ᴛɪᴍᴇᴏᴜᴛ"

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
            'Name': '👤 ɴᴀᴍᴇ',
            "Father's Name": '👨 ꜰᴀᴛʜᴇʀ',
            'Mobile': '📲 ᴍᴏʙɪʟᴇ',
            'Address': '📍 ᴀᴅᴅʀᴇꜱꜱ',
            'Circle': '📡 ᴄɪʀᴄʟᴇ',
            'State': '🏛 ꜱᴛᴀᴛᴇ'
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
        return "❌ ɴᴏ ʀᴇᴄᴏʀᴅꜱ ꜰᴏᴜɴᴅ"
    title = {
        'aadhaar': '🪪 ᴀᴀᴅʜᴀʀ',
        'mobile': '🇮🇳 ɪɴᴅ ɴᴜᴍʙᴇʀ',
        'vehicle': '🚘 ᴠᴇʜɪᴄʟᴇ'
    }.get(search_type, '📊 ʀᴇꜱᴜʟᴛ')
    result = f"✨ {title} ✨\n📊 ᴛᴏᴛᴀʟ ʀᴇᴄᴏʀᴅꜱ: {len(records)}\n"
    for i, record in enumerate(records, 1):
        if len(records) > 1:
            result += f"\n━━ 👤 ʀᴇᴄᴏʀᴅ {i} ━━\n"
        for key, value in record.items():
            result += f"{key}: <code>{value}</code>\n"
    return result

# --- 🚀 BOT HANDLERS ---
class HexTerminalBot:
    def __init__(self):
        self.client = TelegramClient('bot', API_ID, API_HASH)
        self.user_states = {}
        self.admin_states = {}

    async def start(self):
        await self.client.start(bot_token=BOT_TOKEN)
        self.client.add_event_handler(self.start_handler, events.NewMessage(pattern='/start'))
        self.client.add_event_handler(self.callback_handler, events.CallbackQuery)
        self.client.add_event_handler(self.message_handler, events.NewMessage)
        self.client.add_event_handler(self.button_handler, events.NewMessage)
        
        print("✨ Hex Terminal Premium Bot Started!")
        print("🎨 Using Premium Emojis & Colored Buttons")
        print("📱 Bot is running...")
        await self.client.run_until_disconnected()

    async def start_handler(self, event):
        try:
            uid = event.sender_id
            args = event.message.message.split()
            if len(args) > 1 and args[1].startswith("HEX-"):
                users = load_json(USERS_FILE)
                for inviter, data in users.items():
                    if data.get("invite_code") == args[1] and inviter != str(uid):
                        cr = process_invite(inviter, uid)
                        try:
                            await self.client.send_message(
                                int(inviter),
                                f"🎁 +{cr} ᴄʀᴇᴅɪᴛꜱ! ɴᴇᴡ ᴜꜱᴇʀ ᴊᴏɪɴᴇᴅ!"
                            )
                        except:
                            pass
                        break
            
            user = get_user(uid)
            if not user.get("verified"):
                if await check_channels(uid, self.client):
                    user["verified"] = True
                    save_user(uid, user)
                    await self.show_main_menu(event)
                    return
                await self.show_verification_page(event)
                return
            await self.show_main_menu(event)
        except Exception as e:
            logging.error(f"Start error: {e}")

    async def show_verification_page(self, event):
        try:
            bot_user = await self.client.get_me()
            caption = (
                f"💎 {BOT_NAME} 💎\n"
                f"@{BOT_USERNAME}\n\n"
                f"🔒 ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ʀᴇQᴜɪʀᴇᴅ\n"
                f"ᴊᴏɪɴ ʙᴏᴛʜ ᴄʜᴀɴɴᴇʟꜱ ᴛᴏ ᴜɴʟᴏᴄᴋ\n\n"
                f"⚠️ ɢᴜɪᴅᴇʟɪɴᴇꜱ:\n"
                f"• ᴇᴅᴜᴄᴀᴛɪᴏɴᴀʟ ᴘᴜʀᴘᴏꜱᴇꜱ ᴏɴʟʏ\n"
                f"• ᴜꜱᴇ ᴏɴ ʏᴏᴜʀ ᴏᴡɴ ᴅᴀᴛᴀ\n"
                f"• ʀᴇꜱᴘᴇᴄᴛ ᴘʀɪᴠᴀᴄʏ ʟᴀᴡꜱ\n\n"
                f"🎁 +{DAILY_FREE_CREDITS} ᴅᴀɪʟʏ ⭐\n"
                f"👥 +{INVITE_CREDITS} ᴘᴇʀ ɪɴᴠɪᴛᴇ\n"
                f"⏱ {AUTO_DELETE_TIME}ꜱ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ\n\n"
                f"👑 ᴏᴡɴᴇʀ: @Hexh4ckerOFC\n"
                f"⚠️ ᴍɪꜱᴜꜱᴇ ᴍᴀʏ ʟᴇᴀᴅ ᴛᴏ ʟᴇɢᴀʟ ᴀᴄᴛɪᴏɴ"
            )
            
            photos = await self.client.get_profile_photos(bot_user.id)
            if photos:
                await event.reply(
                    caption,
                    file=photos[0],
                    buttons=PremiumKeyboard.build_verification_buttons()
                )
            else:
                await event.reply(
                    caption,
                    buttons=PremiumKeyboard.build_verification_buttons()
                )
        except Exception as e:
            logging.error(f"Verification page error: {e}")

    async def show_main_menu(self, event):
        try:
            uid = event.sender_id
            is_admin = uid == ADMIN_ID
            user = get_user(uid)
            
            markup = PremiumKeyboard.build_main_menu(user, is_admin)
            
            credits = user.get("credits", 0)
            text = (
                f"💎 ᴘʀᴇᴍɪᴜᴍ ʜᴜʙ 💎\n"
                f"👤 ᴡᴇʟᴄᴏᴍᴇ ʙᴀᴄᴋ, <code>{event.sender.first_name}</code>\n\n"
                f"📊 ʏᴏᴜʀ ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ:\n"
                f"┃ 💰 ᴄʀᴇᴅɪᴛꜱ: {credits}\n"
                f"┃ 🔍 Qᴜᴇʀɪᴇꜱ: {user.get('total_queries', 0)}\n"
                f"┃ 👥 ɪɴᴠɪᴛᴇꜱ: {user.get('invites', 0)}\n\n"
                f"🎁 ʀᴇᴡᴀʀᴅꜱ:\n"
                f"🔄 +{DAILY_FREE_CREDITS} ᴅᴀɪʟʏ ꜰʀᴇᴇ\n"
                f"👥 +{INVITE_CREDITS} ᴘᴇʀ ɪɴᴠɪᴛᴇ\n"
                f"⏱ {AUTO_DELETE_TIME}ꜱ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ\n\n"
                f"⭐ ꜱᴇʟᴇᴄᴛ ᴀ ꜱᴇʀᴠɪᴄᴇ ʙᴇʟᴏᴡ ⭐"
            )
            
            msg = await self.client.send_message(
                event.chat_id,
                text,
                reply_markup=markup,
                parse_mode='html'
            )
            asyncio.create_task(delete_after(msg, AUTO_DELETE_TIME))
        except Exception as e:
            logging.error(f"Main menu error: {e}")

    async def callback_handler(self, event):
        try:
            uid = event.sender_id
            data = event.data.decode('utf-8')
            
            if data == "verify":
                if await check_channels(uid, self.client):
                    user = get_user(uid)
                    user["verified"] = True
                    save_user(uid, user)
                    await event.answer("✅ Verified!")
                    try:
                        await event.message.delete()
                    except:
                        pass
                    await self.show_main_menu(event)
                else:
                    await event.answer("❌ Join both channels!", alert=True)
                return
            
            if uid != ADMIN_ID:
                await event.answer("❌", alert=True)
                return
            
            s = get_settings()
            
            if data == "ad_close":
                await event.message.delete()
                return
            
            elif data == "ad_codes":
                codes = load_json(REDEEM_FILE)
                text = f"🎫 ᴄᴏᴅᴇꜱ: {len(codes)}\n"
                for c, v in list(codes.items())[-15:]:
                    text += f"{'✅' if not v.get('used') else '❌'} <code>{c}</code> | {v.get('credits')}cr\n"
                await event.edit(
                    text,
                    buttons=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🔄 ʙᴀᴄᴋ", callback_data="ad_back")]
                    ]),
                    parse_mode='html'
                )
                return
            
            elif data == "ad_gen":
                self.admin_states[uid] = "gen"
                await event.edit(
                    f"🎫 ᴇɴᴛᴇʀ ᴄʀᴇᴅɪᴛꜱ:\n<i>100</i>",
                    buttons=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🔄 ʙᴀᴄᴋ", callback_data="ad_back")]
                    ]),
                    parse_mode='html'
                )
                return
            
            elif data == "ad_credit":
                self.admin_states[uid] = "credit"
                await event.edit(
                    f"🎁 ᴇɴᴛᴇʀ ɪᴅ ᴀᴍᴏᴜɴᴛ:\n<i>123456789 50</i>",
                    buttons=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🔄 ʙᴀᴄᴋ", callback_data="ad_back")]
                    ]),
                    parse_mode='html'
                )
                return
            
            elif data == "ad_bcast":
                self.admin_states[uid] = "bcast"
                await event.edit(
                    f"⚡ ᴇɴᴛᴇʀ ᴍᴇꜱꜱᴀɢᴇ:",
                    buttons=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🔄 ʙᴀᴄᴋ", callback_data="ad_back")]
                    ]),
                    parse_mode='html'
                )
                return
            
            elif data == "ad_maint":
                s["maintenance_mode"] = not s.get("maintenance_mode", False)
                save_settings(s)
                await event.answer(f"Global: {'ON' if s['maintenance_mode'] else 'OFF'}", alert=True)
                await self.show_admin_panel(event)
                return
            
            elif data.startswith("ad_maint_"):
                f = data.replace("ad_maint_", "")
                s[f"maint_{f}"] = not s.get(f"maint_{f}", False)
                save_settings(s)
                await event.answer(f"{f}: {'ON' if s[f'maint_{f}'] else 'OFF'}", alert=True)
                await self.show_admin_panel(event)
                return
            
            elif data.startswith("ad_"):
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
                if data in toggle_map:
                    k = toggle_map[data]
                    s[k] = not s.get(k, True)
                    save_settings(s)
                    await event.answer(f"{k}: {'ON' if s[k] else 'OFF'}", alert=True)
                await self.show_admin_panel(event)
                return
            
            elif data == "ad_back":
                await self.show_admin_panel(event)
                return
            
            await event.answer()
        except Exception as e:
            logging.error(f"Callback error: {e}")

    async def show_admin_panel(self, event):
        s = get_settings()
        text = (
            f"👑 ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ 👑\n"
            f"👥 ᴜꜱᴇʀꜱ: {len(load_json(USERS_FILE))} | 🎫 ᴄᴏᴅᴇꜱ: {len(load_json(REDEEM_FILE))}"
        )
        await event.edit(
            text,
            buttons=PremiumKeyboard.build_admin_panel(s),
            parse_mode='html'
        )

    async def button_handler(self, event):
        """Handle button clicks from reply keyboard"""
        try:
            uid = event.sender_id
            text = event.message.text
            
            # Handle admin panel button
            if text == "👑 ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ":
                if uid == ADMIN_ID:
                    await self.show_admin_panel(event)
                return
            
            # Handle redeem code
            if text.startswith("HEX-"):
                success, msg = redeem_code(uid, text)
                await send_with_delete(
                    self.client,
                    event.chat_id,
                    f"{msg}",
                    parse_mode='html'
                )
                return
            
            # Handle other buttons based on text
            if text == "📱 ᴛɢ ɪᴅ ➜ 📞 ɴᴜᴍʙᴇʀ":
                self.user_states[uid] = "TG"
                await send_with_delete(
                    self.client,
                    event.chat_id,
                    f"📞 ᴛᴇʟᴇɢʀᴀᴍ ɪᴅ ᴛᴏ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ\n<i>7123181749, 6884112825</i>",
                    parse_mode='html',
                    buttons=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🤖 @ChatIdInfoBot", url="https://t.me/ChatIdInfoBot")]
                    ])
                )
            
            elif text == "🏦 ɪꜰꜱᴄ ɪɴꜰᴏ":
                self.user_states[uid] = "IFSC"
                await send_with_delete(
                    self.client,
                    event.chat_id,
                    f"🏦 ʙᴀɴᴋ ɪꜰꜱᴄ ᴄᴏᴅᴇ\n<i>SBIN0001234, HDFC0001234</i>",
                    parse_mode='html'
                )
            
            elif text == "🔗 ʟɪɴᴋ ʙʏᴘᴀꜱꜱ":
                self.user_states[uid] = "SHORTLINK"
                await send_with_delete(
                    self.client,
                    event.chat_id,
                    f"🔗 ʟɪɴᴋ ʙʏᴘᴀꜱꜱ\n<i>https://indianshortner.in/xxxx</i>",
                    parse_mode='html'
                )
            
            elif text == "🇮🇳 ɪɴᴅ ɴᴜᴍʙᴇʀ":
                self.user_states[uid] = "MOBILE"
                await send_with_delete(
                    self.client,
                    event.chat_id,
                    f"🇮🇳 ɪɴᴅɪᴀɴ ᴍᴏʙɪʟᴇ ɴᴜᴍʙᴇʀ\n<i>9876543210, 8123456789</i>",
                    parse_mode='html'
                )
            
            elif text == "🪪 ᴀᴀᴅʜᴀʀ ɪɴꜰᴏ":
                self.user_states[uid] = "AADHAAR"
                await send_with_delete(
                    self.client,
                    event.chat_id,
                    f"🪪 ᴀᴀᴅʜᴀʀ ɴᴜᴍʙᴇʀ\n<i>123456789012</i>",
                    parse_mode='html'
                )
            
            elif text == "🚘 ʀᴄ ᴅᴇᴛᴀɪʟꜱ":
                self.user_states[uid] = "VEHICLE"
                await send_with_delete(
                    self.client,
                    event.chat_id,
                    f"🚘 ᴠᴇʜɪᴄʟᴇ ɴᴜᴍʙᴇʀ\n<i>KA01AB3256, DL1CX1234</i>",
                    parse_mode='html'
                )
            
            elif text == "📋 ɢꜱᴛ ʟᴏᴏᴋᴜᴘ":
                self.user_states[uid] = "GST"
                await send_with_delete(
                    self.client,
                    event.chat_id,
                    f"🪪 ɢꜱᴛ ɴᴜᴍʙᴇʀ\n<i>19BOKPS7056D1ZI</i>",
                    parse_mode='html'
                )
            
            elif text == "🇵🇰 ᴘᴀᴋ ɴᴜᴍʙᴇʀ":
                self.user_states[uid] = "PAK"
                await send_with_delete(
                    self.client,
                    event.chat_id,
                    f"🇵🇰 ᴘᴀᴋɪꜱᴛᴀɴ ɴᴜᴍʙᴇʀ\n<i>923078750447</i>",
                    parse_mode='html'
                )
            
            elif text == "📲 ɪɴᴅ ɴᴜᴍ ɪɴꜰᴏ 𝟸":
                self.user_states[uid] = "INDNUM"
                await send_with_delete(
                    self.client,
                    event.chat_id,
                    f"📲 ᴀᴅᴠᴀɴᴄᴇᴅ ɴᴜᴍʙᴇʀ\n<i>6363016966, 9876543210</i>",
                    parse_mode='html'
                )
            
            elif text == "🇮🇳 ɪɴᴅ ɴᴜᴍʙᴇʀ 𝟹":
                self.user_states[uid] = "INDNUM3"
                await send_with_delete(
                    self.client,
                    event.chat_id,
                    f"🇮🇳 ɪɴᴅɪᴀɴ ɴᴜᴍʙᴇʀ ᴛʀᴀᴄᴋɪɴɢ\n<i>6363016966, 9876543210</i>",
                    parse_mode='html'
                )
            
            elif text == "👥 ɪɴᴠɪᴛᴇ & ᴇᴀʀɴ":
                user = get_user(uid)
                bot_username = BOT_USERNAME
                link = f"https://t.me/{bot_username}?start={user['invite_code']}"
                await send_with_delete(
                    self.client,
                    event.chat_id,
                    f"👥 ɪɴᴠɪᴛᴇ (+{INVITE_CREDITS}ᴄʀ)\n<code>{link}</code>",
                    parse_mode='html'
                )
            
            elif text == "🎫 ʀᴇᴅᴇᴇᴍ":
                self.user_states[uid] = "REDEEM"
                await send_with_delete(
                    self.client,
                    event.chat_id,
                    f"🎫 ᴇɴᴛᴇʀ ʀᴇᴅᴇᴇᴍ ᴄᴏᴅᴇ:\n<i>HEX-XXXXXXXXXX</i>",
                    parse_mode='html'
                )
            
        except Exception as e:
            logging.error(f"Button handler error: {e}")

    async def message_handler(self, event):
        try:
            uid = event.sender_id
            text = event.message.text
            
            # Skip if it's a command or button (handled by other handlers)
            if text.startswith('/') or text.startswith('HEX-'):
                return
            
            # Check for admin states
            if uid == ADMIN_ID and uid in self.admin_states:
                state = self.admin_states.pop(uid)
                if state == "gen":
                    try:
                        cr = int(text)
                        code = generate_redeem_code(cr)
                        await send_with_delete(
                            self.client,
                            event.chat_id,
                            f"✅ <code>{code}</code> | 💰 {cr}cr",
                            parse_mode='html'
                        )
                    except:
                        await send_with_delete(
                            self.client,
                            event.chat_id,
                            f"❌ ɪɴᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ",
                            parse_mode='html'
                        )
                    return
                
                elif state == "credit":
                    parts = text.split()
                    if len(parts) >= 2:
                        bal = add_credits(parts[0], int(parts[1]))
                        await send_with_delete(
                            self.client,
                            event.chat_id,
                            f"✅ +{parts[1]} | {bal}",
                            parse_mode='html'
                        )
                    else:
                        await send_with_delete(
                            self.client,
                            event.chat_id,
                            f"❌ Format: ID AMOUNT",
                            parse_mode='html'
                        )
                    return
                
                elif state == "bcast":
                    users = load_json(USERS_FILE)
                    cnt = 0
                    for u in users:
                        try:
                            await self.client.send_message(int(u), f"⚡ {text}")
                            cnt += 1
                        except:
                            pass
                    await send_with_delete(
                        self.client,
                        event.chat_id,
                        f"✅ Sent: {cnt}",
                        parse_mode='html'
                    )
                    return
            
            # Check for user state (query mode)
            if uid in self.user_states:
                mode = self.user_states.pop(uid)
                
                # Handle redeem mode
                if mode == "REDEEM":
                    if text.upper().startswith("HEX-"):
                        success, msg = redeem_code(uid, text)
                        await send_with_delete(
                            self.client,
                            event.chat_id,
                            msg,
                            parse_mode='html'
                        )
                    else:
                        await send_with_delete(
                            self.client,
                            event.chat_id,
                            f"❌ ɪɴᴠᴀʟɪᴅ ᴄᴏᴅᴇ",
                            parse_mode='html'
                        )
                    return
                
                # Check credits
                user = get_user(uid)
                if user.get("credits", 0) <= 0:
                    await send_with_delete(
                        self.client,
                        event.chat_id,
                        f"❌ ɴᴏ ᴄʀᴇᴅɪᴛꜱ! +10 ᴅᴀɪʟʏ | +3 ɪɴᴠɪᴛᴇ",
                        parse_mode='html'
                    )
                    return
                
                # Run the query
                await self.run_query(event, mode, text)
            
        except Exception as e:
            logging.error(f"Message handler error: {e}")

    async def run_query(self, event, mode, query):
        try:
            if not await net_ok():
                await send_with_delete(
                    self.client,
                    event.chat_id,
                    f"❌ ɴᴏ ɪɴᴛᴇʀɴᴇᴛ",
                    parse_mode='html'
                )
                return
            
            # Send loading message
            loading_msg = await self.client.send_message(
                event.chat_id,
                "🟩 ꜱᴇᴀʀᴄʜɪɴɢ..."
            )
            
            credit_deducted = False
            
            async with aiohttp.ClientSession() as session:
                if mode in ['AADHAAR', 'MOBILE', 'VEHICLE']:
                    choice_map = {'AADHAAR': '2', 'MOBILE': '1', 'VEHICLE': '4'}
                    raw = run_india_script(choice_map[mode], query)
                    if raw:
                        records = parse_all_india_records(raw)
                        result = format_records_result(records, {'AADHAAR': 'aadhaar', 'MOBILE': 'mobile', 'VEHICLE': 'vehicle'}[mode])
                        if records and "❌" not in str(result):
                            use_credit(event.sender_id)
                            credit_deducted = True
                    else:
                        result = "❌ ꜱᴄʀɪᴘᴛ ꜰᴀɪʟᴇᴅ"
                else:
                    if mode == 'TG':
                        result = await chatid_lookup(session, query)
                    elif mode == 'IFSC':
                        result = await ifsc_lookup(session, query)
                    elif mode == 'SHORTLINK':
                        result = await bypass_lookup(session, query)
                    elif mode == 'GST':
                        result = await gst_lookup(session, query)
                    elif mode == 'PAK':
                        result = await pakistan_lookup(session, query)
                    elif mode == 'INDNUM':
                        result = await indnum_lookup(session, query)
                    elif mode == 'INDNUM3':
                        result = await indnum3_lookup(session, query)
                    else:
                        result = "❌"
                    
                    if result and "❌" not in str(result) and "unavailable" not in str(result).lower():
                        use_credit(event.sender_id)
                        credit_deducted = True
            
            # Get updated user data
            user = get_user(event.sender_id)
            
            # Build final response
            final = (
                f"{result}\n"
                f"{SEP}\n"
                f"💰 {'ᴄʀ: '+str(user.get('credits',0)) if credit_deducted else 'ɴᴏ ᴄʀ ᴅᴇᴅᴜᴄᴛᴇᴅ'} | ⏱ {AUTO_DELETE_TIME}ꜱ"
                f"{FOOTER}"
            )
            
            await loading_msg.delete()
            await send_with_delete(
                self.client,
                event.chat_id,
                final,
                parse_mode='html'
            )
            
        except Exception as e:
            logging.error(f"Run query error: {e}")
            await send_with_delete(
                self.client,
                event.chat_id,
                f"⚠️ ᴇʀʀᴏʀ: {str(e)}",
                parse_mode='html'
            )

# --- 🚀 MAIN ---
async def main():
    bot = HexTerminalBot()
    await bot.start()

if __name__ == '__main__':
    asyncio.run(main())