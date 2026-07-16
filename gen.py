# gen.py - FF Guest Account Generator (Ultra Speed)

import hmac
import hashlib
import requests
import string
import random
import json
import codecs
import time
import os
import sys
import base64
import threading
import re
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ========== HIDDEN CONSTANTS ==========
_H1 = "VkVSV1NGRlZVVlZFVk5WQQ=="
_H2 = "UkdWeFVGRkZWRVZGVlJRVkE9PQ=="
_H3 = "VkZSU1RVRkZWREVGRlJXUUE9PQ=="
_XOR = [0x42, 0x59, 0x5F, 0x42, 0x49, 0x47, 0x42, 0x55, 0x4C, 0x4C, 0x5F]

def _get_hidden():
    try:
        s1 = base64.b64decode(_H3).decode()
        s2 = s1[::-1]
        s3 = base64.b64decode(s2).decode()
        return ''.join(chr(ord(s3[i]) ^ _XOR[i % len(_XOR)]) for i in range(len(s3)))
    except:
        return base64.b64decode("SkFISURfWF9FTVBJUkU=").decode()

_HIDDEN = _get_hidden()

# ========== CONFIGURATION ==========
REGION_LANG = {"ME":"ar","IND":"hi","ID":"id","VN":"vi","TH":"th","BD":"bn","PK":"ur","TW":"zh","CIS":"ru","SAC":"es","BR":"pt"}
HEX_KEY = bytes.fromhex("32656534343831396539623435393838343531343130363762323831363231383734643064356437616639643866376530306331653534373135623764316533")

EXIT_FLAG = False
SUCCESS_COUNTER = 0
RARE_COUNTER = 0
COUPLES_COUNTER = 0
RARITY_SCORE_THRESHOLD = 8
LOCK = threading.Lock()
CURRENT_REGION = "IND"
CURRENT_NAME_PREFIX = "JXE"
CURRENT_PASSWORD_PREFIX = "JXE2026"
CURRENT_TOTAL = 10
CURRENT_THREADS = 100
IS_GHOST = False
CURRENT_ACCOUNTS = []

# ========== RARITY CHECK ==========
PATTERNS = {
    "R4": [r"(\d)\1{3,}", 3], "R3": [r"(\d)\1\1(\d)\2\2", 2],
    "S5": [r"(12345|23456|34567|45678|56789)", 4], "S4": [r"(0123|1234|2345|3456|4567|4568|5678|6789|9876|8765|7654|6543|5432|4321|3210)", 3],
    "P6": [r"^(\d)(\d)(\d)\3\2\1$", 5], "P4": [r"^(\d)(\d)\2\1$", 3],
    "SPH": [r"(69|420|1337|007)", 4], "SPM": [r"(100|200|300|400|500|666|777|888|999)", 2],
    "QD": [r"(1111|2222|3333|4444|5555|6666|7777|8888|9999|0000)", 4],
    "MH": [r"^(\d{2,3})\1$", 3], "MM": [r"(\d{2})0\1", 2], "GD": [r"1618|0618", 3]
}

COMPILED_PATTERNS = {}
for ptype, (pattern, points) in PATTERNS.items():
    COMPILED_PATTERNS[ptype] = (re.compile(pattern), points)

COUPLES_DATA = {}
COUPLES_LOCK = threading.Lock()

def check_rarity(account_data):
    account_id = account_data.get("account_id", "")
    if not account_id or account_id == "N/A":
        return False, None, None, 0
    score = 0
    patterns_found = []
    for ptype, (pattern, pts) in COMPILED_PATTERNS.items():
        if pattern.search(account_id):
            score += pts
            patterns_found.append(ptype)
    digits = [int(d) for d in account_id if d.isdigit()]
    if len(set(digits)) == 1 and len(digits) >= 4:
        score += 5
        patterns_found.append("UNIFORM")
    if len(digits) >= 4:
        diffs = [digits[i+1] - digits[i] for i in range(len(digits)-1)]
        if len(set(diffs)) == 1:
            score += 4
            patterns_found.append("ARITHMETIC")
    if len(account_id) <= 8 and account_id.isdigit() and int(account_id) < 1000000:
        score += 3
        patterns_found.append("LOW_ID")
    if score >= RARITY_SCORE_THRESHOLD:
        reason = f"ID:{account_id} | Score:{score} | {','.join(patterns_found)}"
        return True, "RARE", reason, score
    return False, None, None, score

def check_couple(account_data, thread_id):
    account_id = account_data.get("account_id", "")
    if not account_id or account_id == "N/A":
        return False, None, None
    with COUPLES_LOCK:
        for stored_id, stored in list(COUPLES_DATA.items()):
            stored_aid = stored.get('account_id', '')
            if stored_aid and abs(int(account_id) - int(stored_aid)) == 1:
                partner = stored
                del COUPLES_DATA[stored_id]
                return True, f"Sequential: {account_id} & {stored_aid}", partner
            if stored_aid and account_id == stored_aid[::-1]:
                partner = stored
                del COUPLES_DATA[stored_id]
                return True, f"Mirror: {account_id} & {stored_aid}", partner
        COUPLES_DATA[account_id] = {
            'uid': account_data.get('uid', ''),
            'account_id': account_id,
            'name': account_data.get('name', ''),
            'password': account_data.get('password', ''),
            'region': account_data.get('region', ''),
            'thread_id': thread_id,
            'timestamp': datetime.now().isoformat()
        }
    return False, None, None

# ========== NETWORK & CRYPTO ==========
def encode_varint(n):
    if n < 0:
        return b''
    result = []
    while True:
        byte = n & 0x7F
        n >>= 7
        if n:
            byte |= 0x80
        result.append(byte)
        if not n:
            break
    return bytes(result)

def create_proto_field(field_num, value):
    if isinstance(value, dict):
        nested = create_proto_field(field_num, value)
        header = (field_num << 3) | 2
        return encode_varint(header) + encode_varint(len(nested)) + nested
    elif isinstance(value, int):
        header = (field_num << 3) | 0
        return encode_varint(header) + encode_varint(value)
    elif isinstance(value, (str, bytes)):
        encoded_val = value.encode() if isinstance(value, str) else value
        header = (field_num << 3) | 2
        return encode_varint(header) + encode_varint(len(encoded_val)) + encoded_val
    return b''

def build_proto(fields):
    return b''.join(create_proto_field(k, v) for k, v in fields.items())

def aes_encrypt(hex_data):
    data = bytes.fromhex(hex_data)
    aes_key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(data, AES.block_size))

def encrypt_api(plain_hex):
    plain = bytes.fromhex(plain_hex)
    aes_key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(plain, AES.block_size)).hex()

def generate_exponent():
    exp_digits = {'0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹'}
    num = random.randint(1, 9999)
    return ''.join(exp_digits[d] for d in f"{num:04d}")

WRAPPING_PAIRS = [
    ('꧁', '꧂'), ('『', '』'), ('【', '】'), ('《', '》'), ('〈', '〉'),
    ('〔', '〕'), ('〖', '〗'), ('〘', '〙'), ('〚', '〛'), ('❬', '❭'),
    ('❮', '❯'), ('⦅', '⦆'), ('⟦', '⟧'), ('⟨', '⟩'), ('⫷', '⫸')
]

SINGLE_SYMBOLS = [
    '☆', '★', '✧', '✦', '✩', '✪', '✫', '✬', '✭', '✮', '✯', '✰',
    '♡', '♥', '❤', '❥', '❦', '❧', 'ゝ', '々', '〆', '⁂', '※', '⁑',
    '†', '‡', '•', '‣', '❀', '❁', '❃', '❄', '❅', '❆', '❇', '❈', '❉', '❊', '❋',
    '→', '←', '↑', '↓', '↔', '↕', '➔', '➙', '➛', '➜', '➝', '➞', '➟', '➠', '➡',
    '〽', '〰', '〜', '～', '≈', '∞', '♪', '♫', '♬', '♩'
]

def generate_random_name(base):
    exponent = generate_exponent()
    rand = random.random()
    if rand < 0.4:
        left, right = random.choice(WRAPPING_PAIRS)
        return f"{left}{base}{right}_{exponent}"
    elif rand < 0.7:
        sym = random.choice(SINGLE_SYMBOLS)
        return f"{base}{sym}_{exponent}"
    else:
        return f"{base}_{exponent}"

def generate_custom_password(user_prefix):
    random_part = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(8))
    return f"{user_prefix}_{_HIDDEN}_{random_part}"

# ========== GLOBAL SESSION ==========
GLOBAL_SESSION = None
SESSION_LOCK = threading.Lock()

def get_session():
    global GLOBAL_SESSION
    if GLOBAL_SESSION is None:
        with SESSION_LOCK:
            if GLOBAL_SESSION is None:
                session = requests.Session()
                session.verify = False
                adapter = requests.adapters.HTTPAdapter(
                    pool_connections=500,
                    pool_maxsize=1000,
                    max_retries=0,
                    pool_block=False
                )
                session.mount('https://', adapter)
                GLOBAL_SESSION = session
    return GLOBAL_SESSION

# ========== ACCOUNT CREATION ==========
def create_account(region, account_name, password_prefix, is_ghost=False):
    if EXIT_FLAG:
        return None
    session = get_session()
    try:
        password = generate_custom_password(password_prefix)
        url = "https://100067.connect.garena.com/api/v2/oauth/guest:register"
        payload = {"app_id": 100067, "client_type": 2, "password": password, "source": 2}
        headers = {
            "User-Agent": "GarenaMSDK/4.0.39(SM-A325M;Android 13;en;HK;)",
            "Accept": "application/json", "Content-Type": "application/json; charset=utf-8",
            "Accept-Encoding": "gzip", "Connection": "Keep-Alive"
        }
        response = session.post(url, headers=headers, json=payload, timeout=1.0)
        response.raise_for_status()
        res_json = response.json()
        if "data" in res_json and "uid" in res_json["data"]:
            uid = res_json["data"]["uid"]
            return get_token(uid, password, region, account_name, password_prefix, is_ghost)
    except:
        pass
    return None

def get_token(uid, password, region, account_name, password_prefix, is_ghost=False):
    if EXIT_FLAG:
        return None
    session = get_session()
    try:
        url = "https://100067.connect.garena.com/oauth/guest/token/grant"
        headers = {
            "Accept-Encoding": "gzip", "Connection": "Keep-Alive",
            "Content-Type": "application/x-www-form-urlencoded", "Host": "100067.connect.garena.com",
            "User-Agent": "GarenaMSDK/4.0.19P8(ASUS_Z01QD ;Android 12;en;US;)",
        }
        body = {"uid": uid, "password": password, "response_type": "token", "client_type": "2", "client_secret": HEX_KEY, "client_id": "100067"}
        response = session.post(url, headers=headers, data=body, timeout=1.0)
        response.raise_for_status()
        if 'open_id' in response.json():
            open_id = response.json()['open_id']
            access_token = response.json()["access_token"]
            keystream = [0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30]
            encoded = ""
            for i in range(len(open_id)):
                encoded += chr(ord(open_id[i]) ^ keystream[i % len(keystream)])
            field = codecs.decode(''.join(c if 32 <= ord(c) <= 126 else f'\\u{ord(c):04x}' for c in encoded), 'unicode_escape').encode('latin1')
            return major_register(access_token, open_id, field, uid, password, region, account_name, password_prefix, is_ghost)
    except:
        pass
    return None

def major_register(access_token, open_id, field, uid, password, region, account_name, password_prefix, is_ghost=False):
    if EXIT_FLAG:
        return None
    session = get_session()
    try:
        if is_ghost:
            url = "https://loginbp.ggblueshark.com/MajorRegister"
        elif region.upper() in ["ME", "TH"]:
            url = "https://loginbp.common.ggbluefox.com/MajorRegister"
        else:
            url = "https://loginbp.ggblueshark.com/MajorRegister"
        name = generate_random_name(account_name)
        
        headers = {
            "Accept-Encoding": "gzip", "Authorization": "Bearer", "Connection": "Keep-Alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "loginbp.ggblueshark.com" if is_ghost or region.upper() not in ["ME","TH"] else "loginbp.common.ggbluefox.com",
            "ReleaseVersion": "OB54", "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)",
            "X-GA": "v1 1", "X-Unity-Version": "2018.4."
        }
        lang_code = "pt" if is_ghost else REGION_LANG.get(region.upper(), "en")
        payload = {1: name, 2: access_token, 3: open_id, 5: 102000007, 6: 4, 7: 1, 13: 1, 14: field, 15: lang_code, 16: 1, 17: 1}
        payload_bytes = build_proto(payload)
        encrypted_payload = aes_encrypt(payload_bytes.hex())
        session.post(url, headers=headers, data=encrypted_payload, timeout=1.0)
        login_result = major_login(uid, password, access_token, open_id, region, is_ghost)
        account_id = login_result.get("account_id", "N/A")
        jwt_token = login_result.get("jwt_token", "")
        if account_id != "N/A":
            if not is_ghost and jwt_token and region.upper() != "BR":
                try:
                    force_region_bind(region, jwt_token)
                except:
                    pass
            return {
                "uid": uid, "password": password, "name": name,
                "region": "GHOST" if is_ghost else region, "status": "success",
                "account_id": account_id, "jwt_token": jwt_token
            }
    except:
        pass
    return None

def major_login(uid, password, access_token, open_id, region, is_ghost=False):
    try:
        lang = "pt" if is_ghost else REGION_LANG.get(region.upper(), "en")
        payload_parts = [
            b'\x1a\x132025-08-30 05:19:21"\tfree fire(\x01:\x081.114.13B2Android OS 9 / API-28 (PI/rel.cjw.20220518.114133)J\x08HandheldR\nATM MobilsZ\x04WIFI`\xb6\nh\xee\x05r\x03300z\x1fARMv7 VFPv3 NEON VMH | 2400 | 2\x80\x01\xc9\x0f\x8a\x01\x0fAdreno (TM) 640\x92\x01\rOpenGL ES 3.2\x9a\x01+Google|dfa4ab4b-9dc4-454e-8065-e70c733fa53f\xa2\x01\x0e105.235.139.91\xaa\x01\x02',
            lang.encode("ascii"),
            b'\xb2\x01 1d8ec0240ede109973f3321b9354b44d\xba\x01\x014\xc2\x01\x08Handheld\xca\x01\x10Asus ASUS_I005DA\xea\x01@afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390\xf0\x01\x01\xca\x02\nATM Mobils\xd2\x02\x04WIFI\xca\x03 7428b253defc164018c604a1ebbfebdf\xe0\x03\xa8\x81\x02\xe8\x03\xf6\xe5\x01\xf0\x03\xaf\x13\xf8\x03\x84\x07\x80\x04\xe7\xf0\x01\x88\x04\xa8\x81\x02\x90\x04\xe7\xf0\x01\x98\x04\xa8\x81\x02\xc8\x04\x01\xd2\x04=/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/lib/arm\xe0\x04\x01\xea\x04_2087f61c19f57f2af4e7feff0b24d9d9|/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/base.apk\xf0\x04\x03\xf8\x04\x01\x8a\x05\x0232\x9a\x05\n2019118692\xb2\x05\tOpenGLES2\xb8\x05\xff\x7f\xc0\x05\x04\xe0\x05\xf3F\xea\x05\x07android\xf2\x05pKqsHT5ZLWrYljNb5Vqh//yFRlaPHSO9NWSQsVvOmdhEEn7W+VHNUK+Q+fduA3ptNrGB0Ll0LRz3WW0jOwesLj6aiU7sZ40p8BfUE/FI/jzSTwRe2\xf8\x05\xfb\xe4\x06\x88\x06\x01\x90\x06\x01\x9a\x06\x014\xa2\x06\x014\xb2\x06"GQ@O\x00\x0e^\x00D\x06UA\x0ePM\r\x13hZ\x07T\x06\x0cm\\V\x0ejYV;\x0bU5'
        ]
        payload = b''.join(payload_parts)
        if is_ghost:
            url = "https://loginbp.ggblueshark.com/MajorLogin"
        elif region.upper() in ["ME", "TH"]:
            url = "https://loginbp.common.ggbluefox.com/MajorLogin"
        else:
            url = "https://loginbp.ggblueshark.com/MajorLogin"
        
        headers = {
            "Accept-Encoding": "gzip", "Authorization": "Bearer", "Connection": "Keep-Alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "loginbp.ggblueshark.com" if is_ghost or region.upper() not in ["ME","TH"] else "loginbp.common.ggbluefox.com",
            "ReleaseVersion": "OB54", "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)",
            "X-GA": "v1 1", "X-Unity-Version": "2018.4.11f1"
        }
        data = payload.replace(b'afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390', access_token.encode())
        data = data.replace(b'1d8ec0240ede109973f3321b9354b44d', open_id.encode())
        d = encrypt_api(data.hex())
        session = get_session()
        response = session.post(url, headers=headers, data=bytes.fromhex(d), timeout=1.0)
        if response.status_code == 200 and len(response.text) > 10:
            jwt_start = response.text.find("eyJ")
            if jwt_start != -1:
                jwt_token = response.text[jwt_start:]
                second_dot = jwt_token.find(".", jwt_token.find(".") + 1)
                if second_dot != -1:
                    jwt_token = jwt_token[:second_dot + 44]
                    try:
                        parts = jwt_token.split('.')
                        if len(parts) >= 2:
                            payload_part = parts[1]
                            padding = 4 - len(payload_part) % 4
                            if padding != 4:
                                payload_part += '=' * padding
                            decoded = base64.urlsafe_b64decode(payload_part)
                            data = json.loads(decoded)
                            account_id = data.get('account_id') or data.get('external_id')
                            if account_id:
                                return {"account_id": str(account_id), "jwt_token": jwt_token}
                    except:
                        pass
        return {"account_id": "N/A", "jwt_token": ""}
    except:
        return {"account_id": "N/A", "jwt_token": ""}

def force_region_bind(region, jwt_token):
    try:
        url = "https://loginbp.common.ggbluefox.com/ChooseRegion" if region.upper() in ["ME","TH"] else "https://loginbp.ggblueshark.com/ChooseRegion"
        region_code = "RU" if region.upper() == "CIS" else region.upper()
        proto_data = build_proto({1: region_code})
        encrypted_data = encrypt_api(proto_data.hex())
        payload = bytes.fromhex(encrypted_data)
        headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 12; M2101K7AG Build/SKQ1.210908.001)",
            'Connection': "Keep-Alive", 'Accept-Encoding': "gzip",
            'Content-Type': "application/x-www-form-urlencoded",
            'Authorization': f"Bearer {jwt_token}", 'X-Unity-Version': "2018.4.11f1",
            'X-GA': "v1 1", 'ReleaseVersion': "OB54"
        }
        session = get_session()
        session.post(url, data=payload, headers=headers, timeout=1.0)
    except:
        pass

# ========== GENERATION WORKER ==========
def worker_thread(region, account_name, password_prefix, total_accounts, thread_id, is_ghost, progress_callback=None):
    global SUCCESS_COUNTER, CURRENT_ACCOUNTS
    while not EXIT_FLAG:
        with LOCK:
            if SUCCESS_COUNTER >= total_accounts:
                break
        generate_single_account(region, account_name, password_prefix, total_accounts, thread_id, is_ghost, progress_callback)

def generate_single_account(region, account_name, password_prefix, total_accounts, thread_id, is_ghost, progress_callback=None):
    global SUCCESS_COUNTER, RARE_COUNTER, COUPLES_COUNTER, CURRENT_ACCOUNTS
    if EXIT_FLAG:
        return None
    with LOCK:
        if SUCCESS_COUNTER >= total_accounts:
            return None
    account_result = create_account(region, account_name, password_prefix, is_ghost)
    if not account_result or account_result.get("account_id", "N/A") == "N/A":
        return None
    account_result['thread_id'] = thread_id
    with LOCK:
        SUCCESS_COUNTER += 1
        current = SUCCESS_COUNTER
        CURRENT_ACCOUNTS.append(account_result)
    
    is_rare, rtype, reason, rscore = check_rarity(account_result)
    if is_rare:
        with LOCK:
            RARE_COUNTER += 1
        account_result['rarity_score'] = rscore
        account_result['rarity_reason'] = reason
    
    is_couple, creason, partner = check_couple(account_result, thread_id)
    if is_couple and partner:
        with LOCK:
            COUPLES_COUNTER += 1
    
    if progress_callback:
        progress_callback(account_result, is_rare, is_couple, reason if is_rare else (creason if is_couple else None), partner)

# ========== MAIN GENERATOR FUNCTION ==========
def generate_accounts(region, name_prefix, password_prefix, total, is_ghost=False, progress_callback=None):
    """
    Generate guest accounts.
    Yields accounts as they are generated if progress_callback is provided.
    """
    global EXIT_FLAG, SUCCESS_COUNTER, RARE_COUNTER, COUPLES_COUNTER, CURRENT_ACCOUNTS
    EXIT_FLAG = False
    SUCCESS_COUNTER = 0
    RARE_COUNTER = 0
    COUPLES_COUNTER = 0
    CURRENT_ACCOUNTS = []
    
    threads = []
    for i in range(CURRENT_THREADS):
        t = threading.Thread(
            target=worker_thread,
            args=(region, name_prefix, password_prefix, total, i+1, is_ghost, progress_callback)
        )
        t.daemon = True
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    
    return CURRENT_ACCOUNTS