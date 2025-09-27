# iguc/plugins/help.py
COMMAND = "help"

def handle(cl, from_user_id, args, context):
    auth_list = context.get("auth_users", [])
    spam_enabled = context.get("spam_enabled", False)
    max_spam = context.get("max_spam", 2)
    max_likes = context.get("max_likes", 3)
    daily_like = context.get("daily_like_limit", 10)

    help_text = "📖 **IGUC Bot Commands**\n\n"

    # Open Commands (everyone can use)
    help_text += (
        "🔹 **Open Commands (sab ke liye)**\n"
        ".ping - check bot alive\n"
        ".help - show this help\n"
        ".userinfo <username> - user info (name, bio, followers)\n"
        ".dp <username> - get profile picture\n"
        ".post <username> - get latest post\n"
        ".story <username> - fetch active stories\n"
        ".reel <url> - get reel (risky)\n"
        ".time - current time/date\n"
        ".id - show your IG ID\n"
        ".whoami - your username + full name + id\n"
        ".8ball <question> - magic 8-ball answer\n\n"
    )

    # Authorized Commands
    help_text += "🔒 **Authorized Users Only**\n"
    help_text += f".like <username> <n> - like posts (n <= {max_likes}, daily <= {daily_like})\n"
    if spam_enabled:
        help_text += f".spam <count> <text> - spam messages (count <= {max_spam})\n"
    help_text += (
        ".broadcast <msg> - send msg to all followers (risky)\n"
        ".followers <username> - get follower count\n"
        ".follow <username> - follow a user\n"
        ".unfollow <username> - unfollow a user\n\n"
    )

    # Security Note
    help_text += "⚠️ Use demo accounts only (risk of IG restrictions!)"

    try:
        cl.direct_send(help_text, [from_user_id])
    except Exception as e:
        print("help error:", e)
