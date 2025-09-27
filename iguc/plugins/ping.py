# iguc/plugins/ping.py

COMMANDS = ["ping", "alive"]

def handle(cl, from_user_id, args, context):
    try:
        if args[0].lower() == "ping":
            msgs = [
                "🏓 Ping...",
                "Pong! ✅",
                "Ping → Pong → Ping → Pong 🤹"
            ]
            for m in msgs:
                cl.direct_send(m, [from_user_id])

        elif args[0].lower() == "alive":
            cl.direct_send(
                "✅ Abhi UC IG Bot is **Alive & Running!** 🚀\n\n"
                "Use `.help` to see available commands.",
                [from_user_id]
            )

    except Exception as e:
        print("[!] Error in ping/alive:", e)
