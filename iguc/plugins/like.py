# iguc/plugins/like.py
COMMAND = "like"

import time
import random
import json
import os
from datetime import date

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
    except Exception:
        pass

def reset_like_history_if_needed(path, history):
    today = str(date.today())
    if history.get("date") != today:
        history["date"] = today
        history["count"] = 0
        save_json(path, history)
    return history

def handle(cl, from_user_id, args, context):
    # only authorized users
    auth = context.get("auth_users", [])
    try:
        sender = cl.username_from_user_id(from_user_id)
    except Exception:
        sender = str(from_user_id)
    if sender not in auth:
        try:
            cl.direct_send("You are not authorized to run this command.", [from_user_id])
        except Exception:
            pass
        return

    if len(args) < 2:
        try:
            cl.direct_send("Usage: .like <username> <n>", [from_user_id])
        except Exception:
            pass
        return

    target = args[0]
    try:
        n = int(args[1])
    except ValueError:
        try:
            cl.direct_send("n must be a number.", [from_user_id])
        except Exception:
            pass
        return

    max_likes = int(context.get("max_likes", 3))
    if n < 1 or n > max_likes:
        try:
            cl.direct_send(f"n out of range (1..{max_likes})", [from_user_id])
        except Exception:
            pass
        return

    like_history_file = context.get("like_history_file")
    history = load_json(like_history_file, {"date": str(date.today()), "count": 0})
    history = reset_like_history_if_needed(like_history_file, history)

    daily_cap = int(context.get("daily_like_limit", 10))
    if history.get("count", 0) >= daily_cap:
        try:
            cl.direct_send(f"Daily like cap reached ({daily_cap}).", [from_user_id])
        except Exception:
            pass
        return

    # resolve target and fetch medias
    try:
        uid = cl.user_id_from_username(target)
        medias = cl.user_medias(uid, amount=n)
    except Exception as e:
        try:
            cl.direct_send(f"Error fetching {target}'s posts.", [from_user_id])
        except Exception:
            pass
        return

    liked = 0
    like_delay_min = int(context.get("like_delay_min", 10))
    like_delay_max = int(context.get("like_delay_max", 30))

    for m in medias:
        if history.get("count", 0) >= daily_cap:
            try:
                cl.direct_send(f"Daily like cap reached ({daily_cap}). Stopped.", [from_user_id])
            except Exception:
                pass
            break
        try:
            ok = cl.media_like(m.pk)
            if ok:
                liked += 1
                history["count"] = history.get("count", 0) + 1
                save_json(like_history_file, history)
                # delay after like
                delay = random.uniform(like_delay_min, like_delay_max)
                time.sleep(delay)
        except Exception:
            pass
        # small randomized pause between iterations to reduce pattern
        time.sleep(random.uniform(3, 8))

    try:
        cl.direct_send(f"Attempted likes: {liked}/{len(medias)} (today {history.get('count',0)}/{daily_cap})", [from_user_id])
    except Exception:
        pass
