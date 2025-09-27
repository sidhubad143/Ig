# iguc/plugins/ping.py

COMMAND = "ping"   # main command

def handle(cl, from_user_id, args, context):
    try:
        # .ping
        msgs = [
            "🏓 Ping...",
            "Pong! ✅",
            "Ping → Pong → Ping → Pong 🤹"
        ]
        for m in msgs:
            cl.direct_send(m, [from_user_id])

    except Exception as e:
        print("[!] Error in ping:", e)
