"""
Instagram DM Command Bot (demo)
- Responds to DM commands starting with '.'
- .ping / .help => open for everyone
- .spam / .like => only AUTHORIZED_USERS
- For testing/demo purposes only (risk of IG restrictions!)

pip install instagrapi
python3 bot.py
"""

import time
import random
import json
import os
from datetime import datetime
from instagrapi import Client

# -------------- CONFIG --------------
USERNAME = "abhi_9_8__"        # apna demo username
PASSWORD = "abhi@50"           # apna demo password
SESSION_FILE = "session.json"
PROCESSED_FILE = "processed_msgs.json"

POLL_INTERVAL = 12             # seconds between inbox polls
AUTHORIZED_USERS = [           # allowed usernames (without @)
    "abhi_9_8__"
]

MAX_SPAM = 5                   # max messages allowed for .spam
MAX_LIKES = 3                  # max likes per .like
# -------------------------------------

def human_sleep(min_s=2, max_s=6):
    t = random.uniform(min_s, max_s)
    time.sleep(t)

def load_processed():
    if os.path.exists(PROCESSED_FILE):
        try:
            with open(PROCESSED_FILE, "r") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()

def save_processed(s):
    try:
        with open(PROCESSED_FILE, "w") as f:
            json.dump(list(s), f)
    except Exception as e:
        print("Warning: failed to save processed file:", e)

def login_or_load_session():
    cl = Client()
    if os.path.exists(SESSION_FILE):
        try:
            cl.load_settings(SESSION_FILE)
            cl.login(USERNAME, PASSWORD)
            print("[*] Logged in (session loaded).")
        except Exception as e:
            print("[!] Session load/login failed:", e)
            cl = Client()
            cl.login(USERNAME, PASSWORD)
            print("[*] Logged in (fresh).")
    else:
        cl.login(USERNAME, PASSWORD)
        print("[*] Logged in (fresh).")

    try:
        cl.dump_settings(SESSION_FILE)
        print(f"[*] Session saved -> {SESSION_FILE}")
    except Exception as e:
        print("[!] Couldn't save session:", e)
    return cl

def process_command(cl, text, from_user_id, processed_set):
    parts = text.strip().split()
    cmd = parts[0].lower()

    try:
        sender_username = cl.username_from_user_id(from_user_id)
    except Exception:
        sender_username = str(from_user_id)

    print(f"[{datetime.now().isoformat()}] Command from {sender_username}: {text.strip()}")

    # -------- OPEN COMMANDS (sab ke liye) --------
    if cmd == ".ping":
        try:
            cl.direct_send("pong", [from_user_id])
            print(f"[+] Pong sent to {sender_username}")
        except Exception as e:
            print("Error replying ping:", e)
        return

    if cmd == ".help":
        help_text = (
            "Demo bot commands:\n"
            ".ping - check bot is alive (everyone)\n"
            ".help - show this message (everyone)\n"
            f".spam <count> <text> - only authorized (count <= {MAX_SPAM})\n"
            f".like <username> <n> - only authorized (n <= {MAX_LIKES})\n"
        )
        try:
            cl.direct_send(help_text, [from_user_id])
        except Exception as e:
            print("Error sending help:", e)
        return

    # -------- CONTROL COMMANDS (sirf authorized) --------
    if sender_username not in AUTHORIZED_USERS:
        cl.direct_send("You are not authorized to run this command.", [from_user_id])
        print(f"[!] Unauthorized attempt by {sender_username}")
        return

    # .spam
    if cmd == ".spam":
        if len(parts) < 3:
            cl.direct_send("Usage: .spam <count> <text>", [from_user_id])
            return
        try:
            count = int(parts[1])
        except ValueError:
            cl.direct_send("Count must be a number.", [from_user_id])
            return
        if count < 1 or count > MAX_SPAM:
            cl.direct_send(f"Count out of range (1..{MAX_SPAM})", [from_user_id])
            return
        message = " ".join(parts[2:])
        for i in range(count):
            try:
                cl.direct_send(message, [from_user_id])
                print(f"[+] Spam sent ({i+1}/{count})")
            except Exception as e:
                print("Error during spam send:", e)
                break
            human_sleep(2, 5)
        return

    # .like
    if cmd == ".like":
        if len(parts) < 3:
            cl.direct_send("Usage: .like <username> <n>", [from_user_id])
            return
        target = parts[1]
        try:
            n = int(parts[2])
        except ValueError:
            cl.direct_send("n must be a number.", [from_user_id])
            return
        if n < 1 or n > MAX_LIKES:
            cl.direct_send(f"n out of range (1..{MAX_LIKES})", [from_user_id])
            return
        try:
            uid = cl.user_id_from_username(target)
            medias = cl.user_medias(uid, amount=n)
        except Exception as e:
            cl.direct_send(f"Error fetching {target}'s posts.", [from_user_id])
            print("Lookup error:", e)
            return
        liked = 0
        for m in medias:
            try:
                if cl.media_like(m.pk):
                    liked += 1
                    print(f"[+] Liked {m.pk}")
            except Exception as e:
                print("Error liking:", e)
            human_sleep(3, 8)
        cl.direct_send(f"Liked {liked}/{len(medias)} posts of {target}.", [from_user_id])
        return

    # Unknown
    cl.direct_send("Unknown command. Send .help", [from_user_id])

def poll_inbox_and_handle(cl):
    processed = load_processed()
    print(f"[*] Loaded {len(processed)} processed message IDs.")
    while True:
        try:
            threads = cl.direct_threads(amount=5)
            for thread in threads:
                msgs = getattr(thread, "messages", []) or getattr(thread, "items", [])
                for msg in msgs:
                    msg_id = getattr(msg, "id", None)
                    if not msg_id or msg_id in processed:
                        continue

                    text = getattr(msg, "text", None)
                    user_id = getattr(msg, "user_id", None) or getattr(msg, "sender_id", None)

                    if text and text.strip().startswith("."):
                        process_command(cl, text, user_id, processed)

                    processed.add(msg_id)

            save_processed(processed)
        except Exception as e:
            print("[!] Inbox polling error:", e)

        time.sleep(POLL_INTERVAL + random.uniform(0, 3))

def main():
    print("=== Instagram DM command-bot (demo) ===")
    cl = login_or_load_session()
    human_sleep(1, 3)
    print("[*] Starting inbox polling. Press Ctrl+C to stop.")
    try:
        poll_inbox_and_handle(cl)
    except KeyboardInterrupt:
        print("\nExiting (keyboard interrupt).")
    except Exception as e:
        print("Fatal error:", e)

if __name__ == "__main__":
    main()
