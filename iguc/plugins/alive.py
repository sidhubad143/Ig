# iguc/plugins/alive.py

COMMAND = "alive"

def handle(cl, from_user_id, args, context):
    try:
        cl.direct_send(
            "✅ Abhi UC IG Bot is **Alive & Running!** 🚀\n\n"
            "Use `.help` to see available commands.",
            [from_user_id]
        )
    except Exception as e:
        print("[!] Error in alive:", e)
