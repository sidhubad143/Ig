# iguc/plugins/animations.py
# Instagram "animation" style plugin
# Note: IG me edit nahi hota, isliye multiple messages bhejne padte hain

import time

COMMANDS = ["plane", "music", "snake", "gm", "gn"]

def handle(cl, from_user_id, args, context):
    if not args:
        cl.direct_send("Usage: .plane | .music | .snake | .gm | .gn", [from_user_id])
        return

    cmd = args[0].lower()

    if cmd == "plane":
        frames = [
            "✈-------------","-✈------------","--✈-----------","---✈----------",
            "----✈---------","-----✈--------","------✈-------","-------✈------",
            "--------✈-----","---------✈----","----------✈---","-----------✈--",
            "------------✈-","-------------✈"
        ]
        cl.direct_send("Wait for plane...", [from_user_id])
        for f in frames:
            time.sleep(0.5)
            cl.direct_send(f, [from_user_id])

    elif cmd == "music":
        frames = [
            "🎶 Now Playing: Shape of You\n00:00 ▱▱▱▱▱ 00:10",
            "🎶 Now Playing: Shape of You\n00:01 ▰▱▱▱▱ 00:10",
            "🎶 Now Playing: Shape of You\n00:02 ▰▰▱▱▱ 00:10",
            "🎶 Now Playing: Shape of You\n00:03 ▰▰▰▱▱ 00:10",
            "🎶 Now Playing: Shape of You\n00:04 ▰▰▰▰▱ 00:10",
            "🎶 Now Playing: Shape of You\n00:05 ▰▰▰▰▰ 00:10 ✅"
        ]
        cl.direct_send("Starting music player...", [from_user_id])
        for f in frames:
            time.sleep(1)
            cl.direct_send(f, [from_user_id])

    elif cmd == "snake":
        frames = [
            "◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
            "◻️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
            "◻️◻️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
            "◻️◻️◻️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
            "◻️◻️◻️◻️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️",
            "◻️◻️◻️◻️◻️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️\n◼️◼️◼️◼️◼️"
        ]
        cl.direct_send("Snake game starting...", [from_user_id])
        for f in frames:
            time.sleep(0.3)
            cl.direct_send(f, [from_user_id])

    elif cmd == "gm":
        text = (
            "｡♥｡･ﾟ♡ﾟ･｡♥｡･｡･｡･｡♥｡･\n"
            "╭━┳━┳━┳╯┃╭━┳╋╋━┫╰┫╰╮\n"
            "┃╋┃╋┃╋┃╋┃┃┃┃┃┃╋┃┃┃╭┫\n"
            "┣╮┣━┻━┻━╯╰┻━┻╋╮┣┻┻━╯\n"
            "╰━╯╱╱╱╱╱╱╱╱╱╱╰━╯\n"
            "｡♥｡･ﾟ♡ﾟ･｡♥° ♥｡･ﾟ♡ﾟ･"
        )
        cl.direct_send("Good Morning 🌞", [from_user_id])
        cl.direct_send(text, [from_user_id])

    elif cmd == "gn":
        text = (
            "｡♥｡･ﾟ♡ﾟ･｡♥｡･｡･｡･｡♥｡･｡♥｡･ﾟ♡ﾟ･\n"
            "╭━┳━┳━┳╯┃╭━━┳━┳┳┳━┳╋╋━┳┳━╮\n"
            "┃╋┃╋┃╋┃╋┃┃┃┃┃╋┃╭┫┃┃┃┃┃┃┃╋┃\n"
            "┣╮┣━┻━┻━╯╰┻┻┻━┻╯╰┻━┻┻┻━╋╮┃\n"
            "╰━╯╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╰━╯\n"
            "｡♥｡･ﾟ♡ﾟ･｡♥｡･｡･｡･｡♥｡･｡♥｡･ﾟ♡ﾟ･"
        )
        cl.direct_send("Good Night 🌙", [from_user_id])
        cl.direct_send(text, [from_user_id])

    else:
        cl.direct_send("Unknown animation command.", [from_user_id])
