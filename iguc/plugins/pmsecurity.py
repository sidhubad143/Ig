# iguc/plugins/pm_security.py

COMMANDS = ["allow", "disallow"]

# PM Security state
pm_security = {
    "enabled": True,
    "allowed": set(),      # usernames allowed
    "warns": {}            # {username: warn_count}
}
MAX_WARNS = 3

def handle(cl, from_user_id, args, context):
    try:
        username = cl.username_from_user_id(from_user_id)

        # authorized control
        if username in context["AUTHORIZED_USERS"]:
            if args[0].lower() == "allow" and len(args) > 1:
                target = args[1]
                pm_security["allowed"].add(target)
                cl.direct_send(f"✅ {target} allowed in PM.", [from_user_id])
                return
            elif args[0].lower() == "disallow" and len(args) > 1:
                target = args[1]
                pm_security["allowed"].discard(target)
                cl.direct_send(f"⛔ {target} disallowed in PM.", [from_user_id])
                return

        # PM Security checks (normal messages)
        if not args[0].startswith("."):  # only for normal text
            if username not in pm_security["allowed"]:
                count = pm_security["warns"].get(username, 0) + 1
                pm_security["warns"][username] = count

                if count >= MAX_WARNS:
                    try:
                        uid = cl.user_id_from_username(username)
                        cl.user_block(uid)
                        cl.direct_send(f"🚫 {username} blocked after {MAX_WARNS} warns!", [from_user_id])
                    except Exception as e:
                        print("Block error:", e)
                else:
                    cl.direct_send(
                        f"⚠️ PM Security: Warning {count}/{MAX_WARNS}.\n"
                        "Reply `.allow <username>` to whitelist.",
                        [from_user_id]
                    )
                return

    except Exception as e:
        print("[!] PM Security error:", e)
