# iguc/plugins/broadcast.py
COMMAND = "broadcast"

def handle(cl, from_user_id, args, context):
    sender_username = cl.username_from_user_id(from_user_id)
    if sender_username not in context["AUTHORIZED_USERS"]:
        cl.direct_send("Not authorized.", [from_user_id])
        return
    if len(args) < 2:
        cl.direct_send("Usage: .broadcast <msg>", [from_user_id])
        return

    msg = " ".join(args[1:])
    followers = cl.user_followers(cl.user_id)
    for uid in followers.keys():
        try:
            cl.direct_send(msg, [uid])
        except Exception as e:
            print("Broadcast error:", e)
