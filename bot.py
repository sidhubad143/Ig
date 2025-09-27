"""
instabot_command_bot.py
Demo Instagram "userbot" that responds to DM commands (prefix '.').
USE ONLY ON A TEST/DEMO ACCOUNT.

pip install instagrapi
python instabot_command_bot.py
"""

import time
import random
import json
import os
from datetime import datetime
from instagrapi import Client

# -------------- CONFIG --------------
USERNAME = "abhi_9_8__"
PASSWORD = "abhi@50"
SESSION_FILE = "session.json"
PROCESSED_FILE = "processed_msgs.json"

POLL_INTERVAL = 12          # seconds between inbox polls (increase to be safer)
AUTHORIZED_USERS = [        # usernames allowed to control the bot
    "abhi_9_8__"
]

MAX_SPAM = 5                # absolute maximum messages allowed for .spam
MAX_LIKES = 3               # absolute maximum likes per .like command
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
    # try to reuse previous settings/session
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

def username_allowed(cl, user_id):
    try:
        uname = cl.username_from_user_id(user_id)
        return uname in AUTHORIZED_USERS
    except Exception:
        return False

def process_command(cl, text, from_user_id, thread_id, processed_set):
    # commands must start with dot
    if not text or not text.strip().startswith("."):
        return

    parts = text.strip().split()
    cmd = parts[0].lower()

    # Map user_id -> username (safe attempt)
    try:
        sender_username = cl.username_from_user_id(from_user_id)
    except Exception:
        sender_username = str(from_user_id)

    print(f"[{datetime.now().isoformat()}] Command from {sender_username}: {text.strip()}")

    # SECURITY: only allow commands from authorized usernames
    if sender_username not in AUTHORIZED_USERS:
        print(f"[!] Unauthorized command attempt by {sender_username} — ignoring.")
        try:
            cl.direct_send(text="You are not authorized to control this bot.", user_ids=[from_user_id])
        except Exception:
            pass
        return

    # .ping
    if cmd == ".ping":
        t0 = time.time()
        try:
            cl.direct_send(text="pong", user_ids=[from_user_id])
            latency = (time.time() - t0) * 1000.0
            print(f"[+] Replied pong ({int(latency)} ms)")
        except Exception as e:
            print("Error replying ping:", e)
        return

    # .help
    if cmd == ".help":
        help_text = (
            "Demo bot commands:\n"
            ".ping - check bot is alive\n"
            ".spam <count> <text> - send <text> <count> times (count<=%d)\n"
            ".like <username> <n> - like <n> recent posts of <username> (n<=%d)\n"
            ".help - show this message\n"
            "NOTE: Use responsibly on a test account only."
        ) % (MAX_SPAM, MAX_LIKES)
        try:
            cl.direct_send(text=help_text, user_ids=[from_user_id])
        except Exception as e:
            print("Error sending help:", e)
        return

    # .spam
    if cmd == ".spam":
        if len(parts) < 3:
            try:
                cl.direct_send(text="Usage: .spam <count> <text>", user_ids=[from_user_id])
            except Exception:
                pass
            return
        try:
            count = int(parts[1])
        except ValueError:
            try:
                cl.direct_send(text="Count must be a number.", user_ids=[from_user_id])
            except Exception:
                pass
            return
        if count < 1 or count > MAX_SPAM:
            try:
                cl.direct_send(text=f"Count out of allowed range (1..{MAX_SPAM}).", user_ids=[from_user_id])
            except Exception:
                pass
            return
        message = " ".join(parts[2:])
        for i in range(count):
            try:
                cl.direct_send(text=message, user_ids=[from_user_id])
                print(f"[+] Spam sent ({i+1}/{count})")
            except Exception as e:
                print("Error during spam send:", e)
                break
            human_sleep(2, 5)
        return

    # .like
    if cmd == ".like":
        if len(parts) < 3:
            try:
                cl.direct_send(text="Usage: .like <username> <n>", user_ids=[from_user_id])
            except Exception:
                pass
            return
        target = parts[1]
        try:
            n = int(parts[2])
        except ValueError:
            try:
                cl.direct_send(text="n must be a number.", user_ids=[from_user_id])
            except Exception:
                pass
            return
        if n < 1 or n > MAX_LIKES:
            try:
                cl.direct_send(text=f"n out of allowed range (1..{MAX_LIKES}).", user_ids=[from_user_id])
            except Exception:
                pass
            return
        try:
            uid = cl.user_id_from_username(target)
        except Exception as e:
            try:
                cl.direct_send(text=f"Could not resolve user {target}.", user_ids=[from_user_id])
            except Exception:
                pass
            print("Lookup error:", e)
            return
        try:
            medias = cl.user_medias(uid, amount=n)
        except Exception as e:
            try:
                cl.direct_send(text=f"Could not fetch medias for {target}.", user_ids=[from_user_id])
            except Exception:
                pass
            print("Fetch medias error:", e)
            return
        liked = 0
        for m in medias:
            try:
                if cl.media_like(m.pk):
                    liked += 1
                    print(f"[+] Liked media {m.pk}")
                else:
                    print(f"[-] Already liked or failed for {m.pk}")
            except Exception as e:
                print("Error liking:", e)
            human_sleep(3, 8)
        try:
            cl.direct_send(text=f"Liked {liked}/{len(medias)} posts of {target}.", user_ids=[from_user_id])
        except Exception:
            pass
        return

    # Unknown command
    try:
        cl.direct_send(text="Unknown command. Send .help for list.", user_ids=[from_user_id])
    except Exception:
        pass

def poll_inbox_and_handle(cl):
    processed = load_processed()
    print(f"[*] Loaded {len(processed)} processed message IDs.")
    while True:
        try:
            # Fetch recent direct threads
            threads = cl.direct_threads()
            for thread in threads:
                # each thread may have `items` (messages)
                items = getattr(thread, "items", None) or getattr(thread, "items_v2", None) or []
                for item in items:
                    # attempt to get unique message id
                    msg_id = getattr(item, "id", None) or getattr(item, "item_id", None) or None
                    if not msg_id:
                        continue
                    if msg_id in processed:
                        continue

                    text = getattr(item, "text", None)
                    user_id = getattr(item, "user_id", None) or getattr(item, "sender_id", None) or getattr(item, "user", None)
                    # In some cases user object exists
                    if isinstance(user_id, dict):
                        user_id = user_id.get("pk") or user_id.get("id")

                    # Only process textual DMs starting with dot
                    if text and text.strip().startswith("."):
                        process_command(cl, text, user_id, thread.id, processed)

                    # mark processed regardless to avoid reprocessing
                    processed.add(msg_id)

            save_processed(processed)
        except Exception as e:
            print("[!] Inbox polling error:", e)

        # sleep between polls
        time.sleep(POLL_INTERVAL + random.uniform(0, 3))

def main():
    print("=== Instagram DM command-bot (demo) ===")
    cl = login_or_load_session()
    human_sleep(1,3)
    print("[*] Starting inbox polling. Press Ctrl+C to stop.")
    try:
        poll_inbox_and_handle(cl)
    except KeyboardInterrupt:
        print("\nExiting (keyboard interrupt).")
    except Exception as e:
        print("Fatal error:", e)

if __name__ == "__main__":
    main()
