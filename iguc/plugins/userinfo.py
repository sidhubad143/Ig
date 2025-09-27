# iguc/plugins/userinfo.py

COMMANDS = ["userinfo"]

def handle(cl, from_user_id, args, context):
    if len(args) < 2:
        cl.direct_send("Usage: .userinfo <username>", [from_user_id])
        return
    try:
        target = args[1]
        user = cl.user_info_by_username(target)
        text = (
            f"👤 **User Info:** {target}\n"
            f"• Full Name: {user.full_name}\n"
            f"• Bio: {user.biography or '—'}\n"
            f"• Followers: {user.follower_count}\n"
            f"• Following: {user.following_count}"
        )
        cl.direct_send(text, [from_user_id])
    except Exception as e:
        cl.direct_send("Error fetching user info.", [from_user_id])
        print("userinfo error:", e)
