# iguc/plugins/reel.py
COMMAND = "reel"

def handle(cl, from_user_id, args, context):
    if len(args) < 2:
        cl.direct_send("Usage: .reel <url>", [from_user_id])
        return
    url = args[1]
    try:
        media = cl.media_pk_from_url(url)
        info = cl.media_info(media)
        cl.direct_send(info.video_url, [from_user_id])
    except Exception as e:
        cl.direct_send("Error fetching reel (risky feature).", [from_user_id])
        print("reel error:", e)
