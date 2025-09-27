# iguc/plugins/help.py
COMMAND = "help"

def handle(cl, from_user_id, args, context):
    auth_list = context.get("auth_users", [])
    spam_enabled = context.get("spam_enabled", False)
    max_spam = context.get("max_spam", 2)
    max_likes = context.get("max_likes", 3)
    daily_like = context.get("daily_like_limit", 10)

    help_text = (
        "Safe Demo Bot commands:\n"
        ".ping - check bot is alive (everyone)\n"
        ".help - show this message (everyone)\n"
        f".like <username> <n> - only authorized (n <= {max_likes}, per day <= {daily_like})\n"
    )
    if spam_enabled:
        help_text += f".spam <count> <text> - only authorized (count <= {max_spam})\n"

    try:
        cl.direct_send(help_text, [from_user_id])
    except Exception:
        pass
