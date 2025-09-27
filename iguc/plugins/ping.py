# iguc/plugins/ping.py
COMMAND = "ping"

def handle(cl, from_user_id, args, context):
    # reply pong
    try:
        cl.direct_send("pong", [from_user_id])
    except Exception:
        pass
