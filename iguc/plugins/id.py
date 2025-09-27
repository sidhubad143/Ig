# iguc/plugins/id.py
COMMAND = "id"

def handle(cl, from_user_id, args, context):
    cl.direct_send(f"🆔 Your IG User ID: {from_user_id}", [from_user_id])
