# iguc/plugins/followers.py
COMMAND = "followers"

def handle(cl, from_user_id, args, context):
    if len(args) < 2:
        cl.direct_send("Usage: .followers <username>", [from_user_id])
        return
    username = args[1]
    try:
        uid = cl.user_id_from_username(username)
        info = cl.user_info(uid)
        cl.direct_send(f"👥 {username} has {info.follower_count} followers.", [from_user_id])
    except Exception as e:
        cl.direct_send("Error fetching follower count.", [from_user_id])
        print("followers error:", e)
