# iguc/plugins/dp.py
COMMAND = "dp"

def handle(cl, from_user_id, args, context):
    if len(args) < 2:
        cl.direct_send("Usage: .dp <username>", [from_user_id])
        return
    username = args[1]
    try:
        uid = cl.user_id_from_username(username)
        info = cl.user_info(uid)
        cl.direct_send(info.profile_pic_url, [from_user_id])
    except Exception as e:
        cl.direct_send("Error fetching DP.", [from_user_id])
        print("dp error:", e)
