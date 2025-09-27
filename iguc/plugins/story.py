# iguc/plugins/story.py
COMMAND = "story"

def handle(cl, from_user_id, args, context):
    if len(args) < 2:
        cl.direct_send("Usage: .story <username>", [from_user_id])
        return
    username = args[1]
    try:
        uid = cl.user_id_from_username(username)
        stories = cl.user_stories(uid)
        if not stories:
            cl.direct_send("No active stories.", [from_user_id])
        for s in stories:
            cl.direct_send(s.thumbnail_url, [from_user_id])
    except Exception as e:
        cl.direct_send("Error fetching stories.", [from_user_id])
        print("story error:", e)
