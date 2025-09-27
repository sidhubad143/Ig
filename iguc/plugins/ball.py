# iguc/plugins/ball.py
import random

COMMAND = "8ball"

answers = [
    "Yes ✅", "No ❌", "Maybe 🤔", "Definitely 👍", "Never 🚫",
    "Ask later ⏳", "100% sure 🎯", "Doubtful 😬"
]

def handle(cl, from_user_id, args, context):
    if len(args) < 2:
        cl.direct_send("Usage: .8ball <question>", [from_user_id])
        return
    reply = random.choice(answers)
    cl.direct_send(f"🎱 {reply}", [from_user_id])
