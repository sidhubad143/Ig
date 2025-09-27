# iguc/plugins/whoami.py
COMMAND = "whoami"

def handle(cl, from_user_id, args, context):
    try:
        user = cl.user_info(from_user_id)
        msg = (
            f"👤 You are:\n"
            f"Username: {user.username}\n"
            f"Full Name: {user.full_name}\n"
            f"ID: {user.pk}"
        )
        cl.direct_send(msg, [from_user_id])
    except Exception as e:
        cl.direct_send("Error fetching profile.", [from_user_id])
        print("whoami error:", e)
