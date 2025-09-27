# iguc/plugins/post.py
COMMAND = "post"

def handle(cl, from_user_id, args, context):
    if len(args) < 2:
        cl.direct_send("Usage: .post <username>", [from_user_id])
        return
    username = args[1]
    try:
        uid = cl.user_id_from_username(username)
        medias = cl.user_medias(uid, amount=1)
        if medias:
            cl.direct_send(medias[0].thumbnail_url, [from_user_id])
        else:
            cl.direct_send("No posts found.", [from_user_id])
    except Exception as e:
        cl.direct_send("Error fetching post.", [from_user_id])
        print("post error:", e)
