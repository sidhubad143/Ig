# iguc/main.py
import os
import json
import time
import random
import importlib
import pkgutil
from datetime import date
from instagrapi import Client

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
PLUGINS_PACKAGE = "iguc.plugins"

# Ensure data dir exists
os.makedirs(DATA_DIR, exist_ok=True)

# Load config
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
with open(CONFIG_PATH, "r") as f:
    cfg = json.load(f)

# Shortcut variables from config
USERNAME = cfg.get("username")
PASSWORD = cfg.get("password")
SESSION_FILE = cfg.get("session_file", os.path.join(DATA_DIR, "session.json"))
PROCESSED_FILE = cfg.get("processed_file", os.path.join(DATA_DIR, "processed_msgs.json"))
LIKE_HISTORY_FILE = cfg.get("like_history_file", os.path.join(DATA_DIR, "like_history.json"))
POLL_INTERVAL = int(cfg.get("poll_interval", 60))
AUTHORIZED_USERS = cfg.get("authorized_users", [])
SPAM_ENABLED = bool(cfg.get("spam_enabled", False))
MAX_SPAM = int(cfg.get("max_spam", 2))
MAX_LIKES = int(cfg.get("max_likes_per_command", 3))
DAILY_LIKE_LIMIT = int(cfg.get("daily_like_limit", 10))
LIKE_DELAY_MIN = int(cfg.get("like_delay_min", 10))
LIKE_DELAY_MAX = int(cfg.get("like_delay_max", 30))

# Helper IO
def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception:
            return default
    return default

def save_json(path, data):
    try:
        with open(path, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print("[!] Failed to save", path, e)

# Processed messages set
processed = set(load_json(PROCESSED_FILE, []))

# Like history
like_history = load_json(LIKE_HISTORY_FILE, {"date": str(date.today()), "count": 0})
def reset_like_history_if_needed():
    global like_history
    today = str(date.today())
    if like_history.get("date") != today:
        like_history = {"date": today, "count": 0}
        save_json(LIKE_HISTORY_FILE, like_history)

# Login handling
def login_or_load_session():
    cl = Client()
    # ensure session dir exists
    os.makedirs(os.path.dirname(SESSION_FILE), exist_ok=True)
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

# Plugin loader: import all modules from iguc.plugins
def load_plugins():
    plugins = {}
    package = importlib.import_module(PLUGINS_PACKAGE)
    for finder, name, ispkg in pkgutil.iter_modules(package.__path__, package.__name__ + "."):
        try:
            mod = importlib.import_module(name)
            # plugin modules must expose: COMMAND (string) and handle(cl, from_user_id, args, context) function
            cmd = getattr(mod, "COMMAND", None)
            handler = getattr(mod, "handle", None)
            if cmd and callable(handler):
                plugins[cmd] = mod
                print(f"[*] Loaded plugin: {cmd} -> {name}")
        except Exception as e:
            print("[!] Failed loading plugin", name, e)
    return plugins

# Start
def main():
    print("=== IGUC bot starting ===")
    cl = login_or_load_session()
    plugins = load_plugins()

    print("[*] Starting inbox polling. Poll interval:", POLL_INTERVAL)
    try:
        while True:
            try:
                threads = cl.direct_threads(amount=10)
                for thread in threads:
                    msgs = getattr(thread, "messages", []) or getattr(thread, "items", [])
                    for msg in msgs:
                        msg_id = getattr(msg, "id", None)
                        if not msg_id or msg_id in processed:
                            continue
                        text = getattr(msg, "text", None)
                        user_id = getattr(msg, "user_id", None) or getattr(msg, "sender_id", None)
                        if text and text.strip().startswith("."):
                            parts = text.strip().split()
                            cmd = parts[0].lower().lstrip(".")
                            args = parts[1:]
                            plugin = plugins.get(cmd)
                            context = {
                                "config": cfg,
                                "processed_file": PROCESSED_FILE,
                                "like_history_file": LIKE_HISTORY_FILE,
                                "auth_users": AUTHORIZED_USERS,
                                "spam_enabled": SPAM_ENABLED,
                                "max_spam": MAX_SPAM,
                                "max_likes": MAX_LIKES,
                                "daily_like_limit": DAILY_LIKE_LIMIT,
                                "like_delay_min": LIKE_DELAY_MIN,
                                "like_delay_max": LIKE_DELAY_MAX
                            }
                            # if plugin exists - call it
                            if plugin:
                                try:
                                    plugin.handle(cl, user_id, args, context)
                                except Exception as e:
                                    print("[!] Plugin handler error for", cmd, e)
                            else:
                                # unknown commands: reply generic help
                                try:
                                    cl.direct_send("Unknown command. Send .help", [user_id])
                                except Exception:
                                    pass
                        # mark processed
                        processed.add(msg_id)
                # persist processed set
                save_json(PROCESSED_FILE, list(processed))
            except Exception as e:
                print("[!] Inbox polling error:", e)
                # cooldown on error
                time.sleep(120)
            time.sleep(POLL_INTERVAL + random.uniform(0, 5))
    except KeyboardInterrupt:
        print("\nExiting (keyboard interrupt).")

if __name__ == "__main__":
    main()
