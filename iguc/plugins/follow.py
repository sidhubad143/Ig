# iguc/plugins/follow.py
COMMAND = "follow"

def handle(cl, from_user_id, args, context):
    sender_username = cl.username_from_user_id(from_user_id)
    if sender_username not in context["AUTHORIZED_USERS"]:
        cl.direct_send("Not authorized.", [from_user_id])
        return
    if len(args) < 2:
        cl.direct_send("Usage: .follow <username>", [from_user_id])
        return
    try:
        uid = cl.user_id_from_username(args[1])
        cl.user_follow(uid)
        cl.direct_send(f"✅ Followed {args[1]}", [from_user_id])
    except Exception as e:
        cl.direct_send("Error following.", [from_user_id])
        print("follow error:", e)
