# iguc/plugins/fun.py
# Instagram "animation-like" fun commands
import time
import random

COMMANDS = ["love", "rain", "bomb", "brain", "call"]

def handle(cl, from_user_id, args, context):
    if not args:
        cl.direct_send("Usage: .fun <love|rain|bomb|brain|call>", [from_user_id])
        return

    cmd = args[0].lower()

    if cmd == "love":
        frames = [
            "❤️ I",
            "❤️ I Love",
            "❤️ I Love You",
            "❤️ I Love You <3"
        ]
        cl.direct_send("Starting love animation...", [from_user_id])
        for f in frames:
            time.sleep(1)
            cl.direct_send(f, [from_user_id])

    elif cmd == "rain":
        frames = ["🌬","☁️","🌩","🌨","🌧","🌦","🌨🌩🌦🌥⛅🌤"]
        cl.direct_send("Rain animation...", [from_user_id])
        for f in frames:
            time.sleep(0.7)
            cl.direct_send(f, [from_user_id])

    elif cmd == "bomb":
        frames = [
            "▪️▪️▪️▪️\n▪️▪️▪️▪️\n▪️▪️▪️▪️\n▪️▪️▪️▪️",
            "💣💣💣💣",
            "▪️▪️▪️▪️\n💣💣💣💣",
            "💣💣💣💣\n💣💣💣💣",
            "💥💥💥💥",
            "😵😵😵😵",
            "`RIP PLOXXX...`"
        ]
        cl.direct_send("Bomb dropping...", [from_user_id])
        for f in frames:
            time.sleep(1)
            cl.direct_send(f, [from_user_id])

    elif cmd == "brain":
        frames = [
            "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠         <(^_^ <)🗑",
            "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠       <(^_^ <)  🗑",
            "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠     <(^_^ <)    🗑",
            "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n🧠   <(^_^ <)      🗑",
            "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n(> ^_^)>🧠         🗑",
            "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n  (> ^_^)>🧠       🗑",
            "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n          (> ^_^)>🧠🗑",
            "YOᑌᖇ ᗷᖇᗩIᑎ ➡️ 🧠\n\n           (< ^_^ <)🗑",
        ]
        cl.direct_send("Brain loading...", [from_user_id])
        for f in frames:
            time.sleep(0.8)
            cl.direct_send(f, [from_user_id])

    elif cmd == "call":
        frames = [
            "`Connecting To Instagram HQ...`",
            "`Call Connected.`",
            "`Instagram: Hello, who is this?`",
            "`Me: Yo, this is DEMO BOT user 😎`",
            "`User Authorized.`",
            "`Calling Adam Mosseri (CEO IG)...`",
            "`Private Call Connected...`",
            "`Me: Please fix Reels algo 😂`",
            "`CEO: OMG long time no see! I'll handle it.`",
            "`Private Call Disconnected.`"
        ]
        cl.direct_send("☎️ Calling animation...", [from_user_id])
        for f in frames:
            time.sleep(2)
            cl.direct_send(f, [from_user_id])

    else:
        cl.direct_send("Unknown fun command. Use: .fun love/rain/bomb/brain/call", [from_user_id])
